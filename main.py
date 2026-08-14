from pipeline import run_pipeline, clean_input
from reports.report_writer import save_report

TOP_OFFERS_COUNTS = 15

is_on = True

def print_pipeline_summary(report):
    print("\n=== PIPELINE SUMMARY ===")
    print(f"Remotive jobs: {report.extraction['remotive']}")
    print(f"RemoteOK jobs: {report.extraction['remoteok']}")
    print(f"After deduplication: {report.deduplication['after']}")
    print(f"After filtering: {report.filtering['after']}")
    print(f"AI analyses performed: {report.ai_enrichment['LLM_attempts']}")
    print(f"Previous analyses reused: {report.ai_enrichment['previous_analyses_reused']}")
    print(f"Successful enrichments: {report.ai_enrichment['successful_enrichments']}")
    print(f"Failed enrichments: {report.ai_enrichment['failed_enrichments']}")
    print(f"After role filtering: {report.role_filtering['after']}")
    print(f"Roles rejected: {report.role_filtering['removed']}")

def print_top_jobs_results(final_jobs_list):
    print("\nThese are top jobs found:\n")
    for n, job in enumerate(final_jobs_list, start=1):
        print(
            f"=================================================\n"
            f"#{n} {job.title} - {job.company}\n"
            f"Salary: {job.salary_min}\n"
            f"AI Role: {job.ai_role}\n"
            f"Seniority: {job.ai_seniority}\n"
            f"AI Skills: {', '.join(job.ai_tags) if job.ai_tags else 'None'}\n"
            f"Score: {job.score}\n"
            f"URL: {job.url}\n"
            f"=================================================\n"
            f"\n"
        )


while is_on:
    user_tags_input = input("Provide me with the list of Tags you want to see within jobs\n")
    user_tags = clean_input(user_tags_input)

    user_keywords_input = input("Provide me with a list of keywords in searched jobs\n")
    user_keywords = clean_input(user_keywords_input)

    try:
        user_minimumSal = int(input("Provide me with a minimum acceptable salary\n"))
        is_on = False
    except ValueError:
        print("Provided value is not an integer, please correct")



    final_jobs_list, report = run_pipeline(
        keywords=user_keywords,
        tags=user_tags,
        minimum_sal=user_minimumSal,
        top_n=TOP_OFFERS_COUNTS)


    print_pipeline_summary(report)
    print_top_jobs_results(final_jobs_list)

    saved_file = save_report(report)
    print(f"Report saved: {saved_file}")