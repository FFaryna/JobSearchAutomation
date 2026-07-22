import ollama
from pathlib import Path
import json

PROMPT_DIR = Path(__file__).parent / "prompts" / "job_enrichment"


def load_prompts():
    user_prompt = Path(PROMPT_DIR / "user.md")
    system_prompt = Path(PROMPT_DIR / "system.md")

    user_prompt = user_prompt.read_text()
    system_prompt = system_prompt.read_text()

    return user_prompt, system_prompt


def create_user_prompt(user_prompt: str, job_description: str) -> str:
    user_prompt = user_prompt.replace("{{job_description}}", job_description)

    return user_prompt


def analyse_job(user_prompt:str, system_prompt:str) -> str:
    try:
        response = ollama.chat(
            model='llama3.2',
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            options={
                'temperature' : 0
            },
            format="json"
        )

    except ollama.ResponseError as e:
        print(e.error)

    return response.message.content


def output():
    dummy_description =  """
    Python developer required.
    Experience with AWS and SQL.
    """

    user_prompt, system_prompt = load_prompts()

    user_prompt = create_user_prompt(user_prompt=user_prompt, job_description=dummy_description)


    result = analyse_job(user_prompt, system_prompt)

    try:
        pretty_result = json.dumps(
            json.loads(result),
            indent=4
        )

        print(pretty_result)

    except json.JSONDecodeError:
        print(result)

output()