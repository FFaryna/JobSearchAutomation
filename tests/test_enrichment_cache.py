import pytest

from databases.enrichment_cache import JobEnrichmentCache
from models.cached_enrichment import CachedEnrichment


def test_get_returns_none_for_missing_identifier(tmp_path):
    database_path = tmp_path / "test_cache.db"
    cache = JobEnrichmentCache(database_path)

    result = cache.get("does-not-exist")

    assert result is None


def test_save_and_get_enrichment(tmp_path):
    database_path = tmp_path / "test_cache.db"
    cache = JobEnrichmentCache(database_path)

    enrichment = CachedEnrichment(
        id=0,
        identifier="job-123",
        ai_role="RPA Developer",
        ai_seniority="Mid",
        ai_tags=["Python", "UiPath"],
        created_at="2026-08-11 23:45:00"
    )

    cache.save(enrichment)
    result = cache.get("job-123")

    assert result.identifier == enrichment.identifier
    assert result.ai_role == enrichment.ai_role
    assert result.ai_seniority == enrichment.ai_seniority
    assert result.ai_tags == enrichment.ai_tags
    assert result.created_at == enrichment.created_at


def test_save_duplicate_identifier_raises_error(tmp_path):
    database_path = tmp_path / "test_cache.db"
    cache = JobEnrichmentCache(database_path)

    enrichment = CachedEnrichment(
        id=0,
        identifier="job-123",
        ai_role="RPA Developer",
        ai_seniority="Mid",
        ai_tags=["Python"],
        created_at="2026-08-11 23:45:00"
    )

    cache.save(enrichment)

    with pytest.raises(Exception):
        cache.save(enrichment)