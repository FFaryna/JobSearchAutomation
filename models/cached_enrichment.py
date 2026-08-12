from dataclasses import dataclass

@dataclass
class CachedEnrichment:
    id: int | None
    identifier: str
    ai_role: str
    ai_seniority: str
    ai_tags: list[str]
    created_at: str