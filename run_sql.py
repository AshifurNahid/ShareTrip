import sqlite3
import os

def run_sql_query(query):
    """Run a SQL query on the SQLite database"""
    if not os.path.exists('db.sqlite3'):
        print("Database file not found!")
        return
    
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)
        
        # If it's a SELECT query, fetch and display results
        if query.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()
            if results:
                # Get column names
                columns = [description[0] for description in cursor.description]
                print(f"Columns: {columns}")
                print("-" * 50)
                for row in results:
                    print(row)
            else:
                print("No results found.")
        else:
            # For INSERT, UPDATE, DELETE queries
            conn.commit()
            print(f"Query executed successfully. Rows affected: {cursor.rowcount}")
    
    except sqlite3.Error as e:
        print(f"SQL Error: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    # Interactive mode - uncomment to enter custom queries
    print("SQLite Query Runner")
    print("Available tables:")
    run_sql_query("SELECT name FROM sqlite_master WHERE type='table';")
    
    print("\n" + "="*50)
    
    # Quick examples - uncomment what you want to see
    # run_sql_query("SELECT * FROM users;")
    # run_sql_query("SELECT * FROM trips;")
    # run_sql_query("SELECT * FROM bookings;")
    
    # Interactive query input
    while True:
        query = input("\nEnter SQL query (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break
        if query.strip():
            run_sql_query(query)
