import sqlite3

def run_sql_query(sql_query: str) -> str:
    """Executes a SQL query against company.db and returns results or error."""
    try:
        conn = sqlite3.connect("company.db")
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        conn.close()
        return f"Success: {str(results)}"
    except Exception as e:
        # Crucial for agents: Return the exact error message so it can learn
        return f"Error: {str(e)}"
