import re
from scrapers.remoteok_scraper import get_remoteok_jobs
from scrapers.remotivecom_scraper import get_remotive_jobs
from models.pipeline_run_report import PipelineRunReport
from datetime import datetime



TIMESTAMP = datetime.now().strftime("%d/%m %H:%M:%S")

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
    duplicates = []

    for job in jobs_list:
        key = f"{job.title}|{job.company}"

        if key not in unique_jobs:
            unique_jobs[key] = job

        else:
            existing_job = unique_jobs[key]

            duplicates.append({
                "duplicate": job.title,
                "company": job.company,
            })

            current_score = duplicate_quality_score(job)
            existing_score = duplicate_quality_score(existing_job)

            if current_score > existing_score:
                unique_jobs[key] = job

    #### ============== REPORTING PART ==============
    deduplication_report = {
        "before": len(jobs_list),
        "after": len(unique_jobs),
        "removed": len(jobs_list) - len(unique_jobs),
        "examples": duplicates[:5]
    }

    return list(unique_jobs.values()), deduplication_report ## allows to retrieve the values from the dictionary created above, where each key is a concat of position + company. In this way, the final list can be used in the main.py

def filtering_jobs(jobs_list, keywords, tags, minimum_sal):
    jobs_before = len(jobs_list)


    print(f"Total jobs before filtering: {jobs_before}")
    print(f"TAGS RAW: {tags}")
    filtered_jobs = []

    salary_removed = 0
    no_match_removed = 0

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

        else:
            if not salary_check:
                salary_removed += 1

            elif not position_exists and not tags_exist:
                no_match_removed += 1

    ### =================== reporting =====================

    filtering_report = {
        "before": jobs_before,
        "after": len(filtered_jobs),
        "removed": jobs_before - len(filtered_jobs),
        "reasons":{
            "salary": salary_removed,
            "no_match": no_match_removed
        }
    }



    return filtered_jobs, filtering_report

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
    remotive_jobs = get_remotive_jobs()
    remoteok_jobs = get_remoteok_jobs()
    jobs = remoteok_jobs + remotive_jobs

    report.extraction = {
        "remotive": len(remotive_jobs),
        "remoteok": len(remoteok_jobs)
    }


    # 2. Deduplicate
    jobs, deduplication_report = deduplicate_job_listings(jobs)
    report.deduplication = deduplication_report

    # 3. FILTER
    filtered_jobs, filtering_report = filtering_jobs(
        jobs_list = jobs,
        keywords=keywords,
        tags=tags,
        minimum_sal=minimum_sal
    )

    report.filtering = filtering_report

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





