from dataclasses import dataclass

@dataclass
class Job:
    title: str
    company: str
    description: str | None
    tags: list[str]
    salary_min: int | None
    salary_max: int | None
    url: str
    date_posted: str | None
    source: str

