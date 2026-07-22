import ollama
from pathlib import Path
import json

PROMPT_DIR = Path(__file__).parent / "prompts" / "job_enrichment"
LLM_MODEL = "llama3.2"

def load_prompts():
    user_prompt = Path(PROMPT_DIR / "user.md")
    system_prompt = Path(PROMPT_DIR / "system.md")

    user_prompt = user_prompt.read_text()
    system_prompt = system_prompt.read_text()

    return user_prompt, system_prompt


def create_user_prompt(user_prompt: str, job_description: str) -> str:
    user_prompt = user_prompt.replace("{{job_description}}", job_description)

    return user_prompt

def validate_enrichment(data: dict) -> bool:

    required =[
        "skills",
        "role",
        "seniority"
    ]

    return all(
        field in data for field in required
    )

def fallback_llm_output() -> dict:
    return {
        "skills": [],
        "role": "unknown",
        "seniority": "unknown",
    }

def extract_job_metadata(user_prompt: str, system_prompt: str) -> dict:
    try:
        response = ollama.chat(
            model=LLM_MODEL,
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
        return fallback_llm_output()

    except Exception as e:
        print(e)
        return fallback_llm_output()

    try:
        parsed_response = json.loads(response.message.content)

        if validate_enrichment(parsed_response):
            return parsed_response

        return fallback_llm_output()

    except json.JSONDecodeError:
        return fallback_llm_output()


def output():
    dummy_description =  """
    Python developer required.
    Experience with AWS and SQL.
    """

    user_prompt, system_prompt = load_prompts()

    user_prompt = create_user_prompt(user_prompt=user_prompt, job_description=dummy_description)


    result = extract_job_metadata(user_prompt, system_prompt)

    pretty_result = json.dumps(result, indent=4)
    print(pretty_result)


output()