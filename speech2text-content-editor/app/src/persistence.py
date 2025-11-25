import sqlite3
from typing import List, Optional

from . import domain

DB_PATH = "data/pipeline_database.db"

class Repository:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def _connect(self) -> sqlite3.Connection:
        """Creates a database connection."""
        return sqlite3.connect(self.db_path)

    def add_draft(self, raw_text: str) -> domain.Draft:
        """Adds a new draft to the database."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO drafts (raw_text) VALUES (?)", (raw_text,))
            conn.commit()
            draft_id = cursor.lastrowid
            return domain.Draft(id=draft_id, raw_text=raw_text)

    def get_all_drafts(self) -> List[domain.Draft]:
        """Retrieves all drafts from the database."""
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id, raw_text, created_at FROM drafts ORDER BY created_at DESC")
            rows = cursor.fetchall()
            return [domain.Draft(**row) for row in rows]

    def add_pipeline(self, pipeline: domain.Pipeline) -> domain.Pipeline:
        """Adds a new pipeline to the database."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO pipelines (name, channel, language_avatar, user_persona, post_config)
                VALUES (?, ?, ?, ?, ?)
                """,
                (pipeline.name, pipeline.channel, pipeline.language_avatar, pipeline.user_persona, pipeline.post_config)
            )
            conn.commit()
            pipeline.id = cursor.lastrowid
            return pipeline

    def get_all_pipelines(self) -> List[domain.Pipeline]:
        """Retrieves all pipelines from the database."""
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, channel, language_avatar, user_persona, post_config FROM pipelines")
            rows = cursor.fetchall()
            return [domain.Pipeline(**row) for row in rows]
