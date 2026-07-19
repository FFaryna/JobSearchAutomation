from dataclasses import dataclass, field

@dataclass
class PipelineRunReport:
    timestamp: str
    user_input: dict[str, str]
    extraction: dict | None = None
    # deduplication: dict | None = None
    # filtering: dict[str,str] | None = None
    # scoring: dict[str,str] | None = None