from models.job import Job
from pipeline import score_job

def test_tag_score_uses_source_and_ai_tags():
    job = Job(
        title="Automation Developer",
        company="Test Company",
        source="remoteok",
        url="https://example.com",
)

    job.tags = ["Python"]
    job.ai_tags = ["UiPath"]

    _, breakdown = score_job(
        job,
        keywords=[],
        wanted_tags=["python", "UiPath", "SQL"],
        minimum_sal=50000
    )

    assert breakdown["tags"] == 4

def test_keywords_score_use_source_and_ai_tags():
    job = Job(
        title="Automation Developer",
        company="Test Company",
        source="remoteok",
        url="https://example.com",
    )

    job.ai_role = "Intelligent RPA AI developer"

    _, breakdown = score_job(
        job,
        keywords=["RPA", "Automation"],
        wanted_tags=[],
        minimum_sal=5000
    )

    assert breakdown["keyword_role"] == 3


def test_salary_scoring_upper_threshold():
    job = Job(
        title="Automation Developer",
        company="Test Company",
        source="remoteok",
        url="https://example.com",
    )

    job.salary_min = 6000

    _, breakdown = score_job(
        job,
        keywords=[],
        wanted_tags=[],
        minimum_sal=5000
    )

    assert breakdown["salary"] == 2

def test_salary_scoring_lower_threshold():
    job = Job(
        title="Automation Developer",
        company="Test Company",
        source="remoteok",
        url="https://example.com",
    )

    job.salary_min = 5500

    _, breakdown = score_job(
        job,
        keywords=[],
        wanted_tags=[],
        minimum_sal=5000
    )

    assert breakdown["salary"] == 1


def test_total_score():
        job = Job(
            title="Automation Developer",
            company="Test Company",
            source="remoteok",
            url="https://example.com",
        )

        job.salary_min = 6000
        job.tags = ["Python"]
        job.ai_tags = ["UiPath"]
        job.ai_role = "Intelligent RPA AI developer"


        scored_job, breakdown = score_job(
            job,
            keywords=["RPA", "Automation"],
            wanted_tags=["python", "UiPath", "SQL"],
            minimum_sal=5000
        )

        assert breakdown["keyword_role"] == 3
        assert breakdown["tags"] == 4
        assert breakdown["salary"] == 2
        assert breakdown["total"] == 9
        assert scored_job.score == 9