from scrapers.remotivecom_scraper import normalise_salary

def test_missing_salary_returns_empty_list():
    result = normalise_salary(None)

    assert result == []

def test_invalid_salary_returns_empty_list():
    result = normalise_salary("Unknown")

    assert result == []

def test_salary_as_string():
    result = normalise_salary("50000")

    assert result == [50000]

def test_salary_conversion_from_k_format():
    result = normalise_salary("50k")

    assert result == [50000]

def test_salary_range_conversion():
    result = normalise_salary("50k-70k")

    assert result == [50000, 70000]

def test_salary_as_integer():
    result = normalise_salary(50000)

    assert result == [50000]

def test_hourly_rate():
    result = normalise_salary("$40/hr")

    assert result == [6400]

def test_range_hourly_rate():
    result = normalise_salary("40$/hr - 60$/hr")

    assert result == [6400, 9600]
