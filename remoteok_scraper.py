import requests

SOURCE = "remoteok"

def fetch_data():
    url = "https://remoteok.com/api"
    response = requests.get(url, timeout=10)

    data = response.json()
    return data

def is_valid_job(job):
    position = job.get("position")
    url = job.get("url")

    return (
        position and
        position.strip() and
        url
    )

def parse_salary(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0


def clean_job(job):
    url = job.get("url", "")
    if not url.startswith(("http://", "https://")):
        url = ""


    raw_date = job.get("date", "")
    date = raw_date[:10] if raw_date else ""

    return {
        "position": job.get("position", ""),
        "company": job.get("company", ""),
        "tags": job.get("tags", []),
        "salary_min": parse_salary(job.get("salary_min")),
        "salary_max": parse_salary(job.get("salary_max")),
        "url": url,
        "date": date,
        "source": SOURCE
    }


def get_remoteok_jobs():
    raw_jobs = fetch_data()
    result = []

    for job in raw_jobs:
        if not is_valid_job(job):
            continue

        else:
            cleaned = clean_job(job)
            result.append(cleaned)


    return result

