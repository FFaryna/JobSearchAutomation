from dataclasses import dataclass, field

@dataclass
class Job:
    title: str
    company: str
    source: str
    url: str

    description: str | None = None
    tags: list[str] = field(default_factory=list)
    salary_min: int | None = None
    salary_max: int | None = None
    date_posted: str | None = None
    score: float = 0

