from ai.job_enrichment import create_user_prompt, validate_enrichment, fallback_llm_output, enrich_job
from models.job import Job

def test_create_user_prompt_replace_description():
    template = """
    Analyse:

    {{job_description}}
    """

    result = create_user_prompt(
        template,
        "Python Developer with Aws experience"
    )

    assert "{{job_description}}" not in result
    assert "Python Developer with Aws experience" in result


def test_valid_enrichment_response():
    data = {
        "skills": [
            "Python",
            "AWS",
            "SQL"
        ],
        "role": "Backend Developer",
        "seniority": "Junior"
    }

    assert validate_enrichment(data) is True

def test_invalid_enrichment_response():
    data = {
        "skills": [
            "Python",
            "AWS",
            "SQL"
    ]}

    assert validate_enrichment(data) is False


def test_fallback_output():

    result = fallback_llm_output()

    assert result["skills"] == []
    assert result["role"] == "unknown"
    assert result["seniority"] == "unknown"


def test_job_enrichment(mocker):

    fake_response = {
        "skills": [
            "Python",
            "AWS"
        ],
        "role": "Backend Developer",
        "seniority": "Junior"
    }

    mocker.patch(
        "ai.job_enrichment.extract_job_metadata",
        return_value = fake_response,
    )

    job = Job(
        title="Python Developer",
        company="Amazon",
        source="remoteok",
        url="https://example.com",
        description="Python developer using AWS"
    )


    result = enrich_job(job)

    assert result.ai_tags == [
        "Python",
        "AWS"
    ]

    assert result.ai_role == "Backend Developer"
    assert result.ai_seniority == "Junior"

def test_job_without_description_is_not_enriched():

    job = Job(
        title="Python Developer",
        company="Amazon",
        source="remoteok",
        url="https://example.com"
    )


    result = enrich_job(job)


    assert result.ai_tags == []
    assert result.ai_role is None
    assert result.ai_seniority is None