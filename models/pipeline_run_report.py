from dataclasses import dataclass, field
from typing import Any

@dataclass
class PipelineRunReport:
        timestamp: str
        user_input: dict[str, Any]
        extraction: dict[str, Any] | None = None
        deduplication: dict[str, Any] | None = None
        filtering: dict[str, Any] | None = None
        scoring: dict[str, Any] | None = None