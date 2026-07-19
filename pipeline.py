import re
from scrapers.remoteok_scraper import get_remoteok_jobs
from scrapers.remotivecom_scraper import get_remotive_jobs

TOP_VALUES = 10
SOURCE_WEIGHTS = {
    "remoteok": 1.0,
    "remotive": 0.7
}

## Used to clean user's input
def duplicate_quality_score(job):
    score = 0

    if job.salary_min:
        score += 1

    tags = job.tags or []
    if tags:
        score += len(job.tags) * 0.5

    if job.company:
        score += 1

    if job.title:
        score += 1

    return score

def clean_input(text): ### removes all special characters from the input [sentence] -> provides with the list of output
    cleaned_list = re.sub(r"[^\w]+", " ", text).lower().split()
    return cleaned_list

def deduplicate_job_listings(jobs_list, **kwargs):
    unique_jobs = {}

    for job in jobs_list:
        key = f"{job.title}|{job.company}"

        if key not in unique_jobs:
            unique_jobs[key] = job

        else:
            existing_job = unique_jobs[key]

            current_score = duplicate_quality_score(job)
            existing_score = duplicate_quality_score(existing_job)

            if current_score > existing_score:
                unique_jobs[key] = job

    return list(unique_jobs.values()) ## allows to retrieve the values from the dictionary created above, where each key is a concat of position + company. In this way, the final list can be used in the main.py

def filtering_jobs(jobs_list, keywords, tags, minimum_sal):
    print(f"Total jobs before filtering: {len(jobs_list)}")
    print(f"TAGS RAW: {tags}")
    filtered_jobs = []

    for job in jobs_list:
        position_text = job.title.lower()
        position_exists = any(key.lower() in position_text for key in keywords)

        tags_exist = False
        job_tags = [t.lower() for t in job.tags or []]
        for tag in tags:
            if tag.lower() in job_tags:
                tags_exist = True
                break

        salary_check = (job.salary_min or 0) > minimum_sal

        if (position_exists or tags_exist) and salary_check:
            filtered_jobs.append(job)

    return filtered_jobs

def score_job(job, keywords, tags, minimum_sal):
    score = 0
    source_weight = SOURCE_WEIGHTS.get(job.source, 1.0)
    position = (job.title or "").lower()
    job_tags = [t.lower() for t in (job.tags or [])]

    for key in keywords:
        if key.lower() in position:
            score += 3

    for tag in tags:
        if tag.lower() in job_tags:
            score += 1.25 * source_weight

    salary_min = job.salary_min or 0

    if salary_min > minimum_sal * 1.2:
        score += 4
    elif salary_min > minimum_sal:
        score += 2

    job.score = score

    return job

def return_highest_matches(count, jobs):
    sorted_jobs = sorted(jobs, key=lambda job: job.score, reverse=True)
    return sorted_jobs[:count]

def run_pipeline(keywords, tags, minimum_sal, top_n):

    report = PipelineRunReport(
        timestamp=TIMESTAMP,
        user_input={
            "keywords": keywords,
            "tags": tags,
            "salary": minimum_sal
        }
    )

    # 1. EXTRACT
    jobs = get_remotive_jobs() + get_remoteok_jobs()

    # 2. Deduplicate
    jobs = deduplicate_job_listings(jobs)

    # 3. FILTER
    filtered_jobs = filtering_jobs(
        jobs_list = jobs,
        keywords=keywords,
        tags=tags,
        minimum_sal=minimum_sal
    )

    # 4. SCORE
    for job in filtered_jobs:
        score_job(
            job,
            tags=tags,
            keywords=keywords,
            minimum_sal=minimum_sal
        )

    # 5. SORT + SELECT
    final_jobs = return_highest_matches(
        count=top_n,
        jobs=filtered_jobs
    )

    return final_jobs





