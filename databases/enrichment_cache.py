import sqlite3
import json

from models.cached_enrichment import CachedEnrichment

class  JobEnrichmentCache:
    def __init__(self, database_path):
        self.database_path = database_path
        self._initialize_database()

    def _initialize_database(self):
        with sqlite3.connect(self.database_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS jobs_enrichment_cache (
                    id INTEGER PRIMARY KEY,
                    identifier TEXT UNIQUE NOT NULL,
                    ai_role TEXT,
                    ai_seniority TEXT,
                    ai_tags TEXT,
                    created_at TEXT
                )
                """
            )

    def get(self, identifier):
        with sqlite3.connect(self.database_path) as connection:
            connection.row_factory = sqlite3.Row

            result = connection.execute(
                """
                SELECT id, identifier, ai_role, ai_seniority, ai_tags, created_at
                FROM jobs_enrichment_cache
                WHERE identifier = ?
                """,
                (identifier,)
            )

            row = result.fetchone()
            if row is None:
                return None
            else:
                list_tags = json.loads(row["ai_tags"])

                enrichment = CachedEnrichment(
                    id = row["id"],
                    identifier = row["identifier"],
                    ai_role = row["ai_role"],
                    ai_seniority = row["ai_seniority"],
                    ai_tags = list_tags,
                    created_at = row ["created_at"]
                )


                return enrichment

    def save(self, enrichment):

        with sqlite3.connect(self.database_path) as connection:
            tags = json.dumps(enrichment.ai_tags)
            connection.execute(
                """
                INSERT INTO jobs_enrichment_cache (
                    identifier,
                    ai_role,
                    ai_seniority,
                    ai_tags,
                    created_at
                )
                 VALUES (?, ?, ?, ?, ?)
                """,
                (
                    enrichment.identifier,
                    enrichment.ai_role,
                    enrichment.ai_seniority,
                    tags,
                    enrichment.created_at)
                )

