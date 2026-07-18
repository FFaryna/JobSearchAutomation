from pipeline import run_pipeline, clean_input

TOP_OFFERS_COUNTS = 15

is_on = True

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



    final_jobs_list = run_pipeline(
        keywords=user_keywords,
        tags=user_tags,
        minimum_sal=user_minimumSal,
        top_n=TOP_OFFERS_COUNTS)

    print(f"These are top jobs found: \n")
    for job in final_jobs_list:
        print(f"{job['position']} | {job['company']} | {job['salary_min']} | {job['url']}")