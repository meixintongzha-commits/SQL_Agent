import os
import sqlite3
from openai import OpenAI
from agent_memory import get_relevant_schema
from tools import run_sql_query

# 1. Initialize the cloud client pointing to Groq's fast Llama 3 engine
# Get a free API key at: https://groq.com
# The OpenAI SDK automatically appends '/chat/completions' to the base URL
client = OpenAI(
    base_url="https://api.groq.com/openai/v1", 
    api_key="put_api_key_here"
)

SYSTEM_PROMPT = """You are an autonomous data agent. You have access to a SQL database tool.
To answer user questions, you must think step-by-step using this exact format:

Thought: Reason about what steps to take.
Action: Write ONLY the SQL query you want to run.
Observation: The system will give you the database response here.

Once you have the final answer, output:
Final Answer: [Your final summary response to the user]

Do not output code blocks like ```sql inside your Action block. Just output the raw query string."""

def query_llm(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            # Switch to Qwen to bypass native tool validation errors
            model="qwen/qwen3.6-27b",  
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        
        if hasattr(response, 'choices') and len(response.choices) > 0:
            choice = response.choices[0]
            if isinstance(choice, dict):
                return choice["message"]["content"]
            else:
                return choice.message.content
                
        return "Final Answer: Error - Blank response received from API."
        
    except Exception as e:
        return f"Final Answer: Cloud API Error occurred: {str(e)}"


def run_agent(user_question: str):
    print(f"\n[User]: {user_question}")
    
    # Step 1: Use PyTorch Memory to select the relevant table
    matched_table = get_relevant_schema(user_question)
    print(f"[Memory]: Selected table context -> '{matched_table}'")
    
    # Construct initial prompt history
    context_prompt = f"{SYSTEM_PROMPT}\n\nContext: You are querying table '{matched_table}'.\nUser Question: {user_question}\n"
    
    # Step 2: Run the execution loop (Allow up to 3 self-correction iterations)
    for iteration in range(3):
        llm_output = query_llm(context_prompt)
        print(f"\n[Agent Iteration {iteration + 1}]:\n{llm_output}")
        
        if "Final Answer:" in llm_output:
            break
            
        # Parse Action out of LLM text block
        if "Action:" in llm_output:
            sql_query = llm_output.split("Action:")[1].strip().split("\n")[0]
            
            # Execute tool
            observation = run_sql_query(sql_query)
            print(f"[Tool Observation]: {observation}")
            
            # Feed the observation back into the prompt history loop
            context_prompt += f"\n{llm_output}\nObservation: {observation}\n"

if __name__ == "__main__":
    # Test Question
    run_agent("How much money did Alice Smith spend in total?")
