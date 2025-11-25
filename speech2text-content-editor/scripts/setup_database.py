import sqlite3
import os

DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "pipeline_database.db")

def create_connection():
    """Create a database connection to the SQLite database."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        print(f"SQLite DB created at {DB_PATH}")
    except sqlite3.Error as e:
        print(e)
    return conn

def create_tables(conn):
    """Create tables from the create_table_sql statements."""
    sql_create_drafts_table = """
    CREATE TABLE IF NOT EXISTS drafts (
        id INTEGER PRIMARY KEY,
        raw_text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    sql_create_pipelines_table = """
    CREATE TABLE IF NOT EXISTS pipelines (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        channel TEXT NOT NULL,
        language_avatar TEXT,
        user_persona TEXT,
        post_config TEXT
    );
    """
    sql_create_generated_posts_table = """
    CREATE TABLE IF NOT EXISTS generated_posts (
        id INTEGER PRIMARY KEY,
        draft_id INTEGER NOT NULL,
        pipeline_id INTEGER NOT NULL,
        final_text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (draft_id) REFERENCES drafts (id),
        FOREIGN KEY (pipeline_id) REFERENCES pipelines (id)
    );
    """
    try:
        c = conn.cursor()
        c.execute(sql_create_drafts_table)
        c.execute(sql_create_pipelines_table)
        c.execute(sql_create_generated_posts_table)
        print("Tables created successfully.")
    except sqlite3.Error as e:
        print(e)

def main():
    conn = create_connection()
    if conn is not None:
        create_tables(conn)
        conn.close()
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
