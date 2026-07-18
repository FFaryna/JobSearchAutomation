import requests
from models.job import Job

SOURCE_NAME = "remoteok"

def fetch_data() -> list[dict]:
    url = "https://remoteok.com/api"
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()
    return data

def is_valid_job(job: dict) -> bool:
    position = job.get("position")
    url = job.get("url")

    return (
        position
        and position.strip()
        and url
        and url.startswith(("http://", "https://"))
    )

def parse_salary(value: str | int | None) -> int | None:
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return None


def normalize_job(job: dict) -> Job:
    url = job.get("url", "")
    if not url.startswith(("http://", "https://")):
        url = ""


    raw_date = job.get("date", "")
    date = raw_date[:10] if raw_date else ""

    return Job(
        title=job.get("position", ""),
        company= job.get("company", ""),
        description=job.get("description"),
        tags=job.get("tags") or [],
        salary_min= parse_salary(job.get("salary_min")),
        salary_max= parse_salary(job.get("salary_max")),
        url= url,
        date_posted = date,
        source= SOURCE_NAME
    )


def get_remoteok_jobs() -> list[Job]:
    raw_jobs = fetch_data()
    result = []

    for job in raw_jobs:
        if is_valid_job(job):
            result.append(normalize_job(job))


    return result

