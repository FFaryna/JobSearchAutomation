from models.job import Job

def test_job_creation_with_required_fields():
    job = Job(
        title="Python Developer",
        company="Amazon",
        source="remoteok",
        url="https://example.com"
    )

    assert job.title == "Python Developer"
    assert job.company == "Amazon"
    assert job.source == "remoteok"
    assert job.url == "https://example.com"


def test_job_has_empty_tags_by_default():
    job = Job(
        title="Python Developer",
        company="Amazon",
        source="remoteok",
        url="https://example.com",
    )

    assert job.tags == []

def test_job_has_default_score_of_zero():
    job = Job(
        title="Python Developer",
        company="Amazon",
        source="remoteok",
        url="https://example.com",
    )

    assert job.score == 0