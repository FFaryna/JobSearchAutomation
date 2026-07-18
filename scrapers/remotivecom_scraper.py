import requests
import os
import json
import re
from models.job import Job

DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
SOURCE = "remotive.com"
NOISE_WORDS = {
    "senior", "junior", "lead", "remote", "fully",
    "part-time", "full-time", "developer", "engineer",
    "software", "job", "hiring"
}



def fetch_data():
    url = "https://remotive.com/api/remote-jobs"
    response = requests.get(url, timeout=10)
    data = response.json()
    return data['jobs']


def is_valid_job(job):
    position = job.get("title")
    url = job.get("url")

    return (
        position and
        position.strip() and
        url
    )

def normalise_salary(value): ## determine min and max salary, if any -> still requires some improvement for more complex wording cases. Possible extension of regex to handle such cases
    try:
        clean_range = value.strip().lower()
        parts = clean_range.split("-")

        for i in range(len(parts)):
            p = parts[i].strip()

            if "k" in p:
                num = float(p.replace("k", "").replace("$", ""))
                new_value = num*1000
                parts[i] = new_value
            else:
                num = float(p.replace("$", ""))
                new_value = num*160
                parts[i] = new_value

        return parts

    except ValueError:
        return []

def extract_tags(text):
    if not text:
        return []

    text = text.lower()
    text = re.sub(r"[^\w]+", " ", text) #removes punctuation/splitters etc

    words = text.split()

    tags = []
    for w in words:
        if w not in NOISE_WORDS and len(w) > 2:
            tags.append(w)

    return list(set(tags))

def clean_job(job):
    title = job.get("title", "")
    description = job.get("description", "")

    url = job.get("url", "")
    if not url.startswith(("http://", "https://")):
        url = ""

    raw_date = job.get("publication_date", "")
    date = raw_date[:10] if raw_date else ""

    raw_salary = job.get('salary', "")

    salary = normalise_salary(raw_salary)
    if not salary:
        salary_min = 0
        salary_max = 0

    elif len(salary) >1:
        salary_min = salary[0]
        salary_max = salary[1]
    else:
        salary_min = salary[0]
        salary_max = salary[0]

    return Job(
        title = title,
        company= job.get("company_name", ""),
        description=description,
        tags= [],
        salary_min=salary_min,
        salary_max=salary_max,
        url=url,
        date_posted=date,
        source=SOURCE
    )


def get_remotive_jobs():
    if DEBUG_MODE:
        with open(file="../remotive_raw.json", mode="r") as file:
            raw_jobs = json.load(file)
    else:
        raw_jobs = fetch_data()

    result = []

    for job in raw_jobs:
        if not is_valid_job(job):
            continue
        else:
            cleaned = clean_job(job)
            result.append(cleaned)

    return result

