import sqlite3
import os

DB_NAME = "budget.db"

class DatabaseManager:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
        self.initialize_db()

    def get_connection(self):
        """Returns a connection to the SQLite database."""
        try:
            conn = sqlite3.connect(self.db_name)
            conn.row_factory = sqlite3.Row  # Access columns by name
            return conn
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            return None

    def initialize_db(self):
        """Creates tables if they do not exist."""
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                # Create Accounts Table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS accounts (
                        id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        balance REAL DEFAULT 0.0
                    )
                """)
                
                # Create Transactions Table (Planned for Phase 3, but good to have prepared)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS transactions (
                        id TEXT PRIMARY KEY,
                        account_id TEXT NOT NULL,
                        date TEXT NOT NULL,
                        amount REAL NOT NULL,
                        category TEXT,
                        type TEXT,
                        note TEXT,
                        FOREIGN KEY (account_id) REFERENCES accounts (id) ON DELETE CASCADE
                    )
                """)
                
                conn.commit()
            except sqlite3.Error as e:
                print(f"Database initialization error: {e}")
            finally:
                conn.close()

    def execute_query(self, query, params=()):
        """Executes a query (INSERT, UPDATE, DELETE) and commits changes."""
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"Query execution error: {e}")
                return False
            finally:
                conn.close()
        return False

    def fetch_all(self, query, params=()):
        """Fetches all results from a SELECT query."""
        conn = self.get_connection()
        results = []
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query, params)
                results = [dict(row) for row in cursor.fetchall()]
            except sqlite3.Error as e:
                print(f"Fetch error: {e}")
            finally:
                conn.close()
        return results

    def fetch_one(self, query, params=()):
        """Fetches a single result from a SELECT query."""
        conn = self.get_connection()
        result = None
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query, params)
                row = cursor.fetchone()
                if row:
                    result = dict(row)
            except sqlite3.Error as e:
                print(f"Fetch one error: {e}")
            finally:
                conn.close()
        return result
