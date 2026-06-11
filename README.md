## CI Status
![Tests](https://github.com/HoJungjae/api-test-automation-framework/actions/workflows/tests.yml/badge.svg)

# API Test Automation Framework

## Overview
This project demonstrates a scalable API test automation framework built using Python and pytest. It simulates real-world SDET practices including modular design, data-driven testing, mocking, and CI/CD integration.

The framework targets [JSONPlaceholder](https://jsonplaceholder.typicode.com), a free fake REST API used for testing and prototyping.

## Why the Pivot

The original framework had a working test suite but everything was wired together in one style — live HTTP calls, a module-level client, and no separation between tests that need the network and tests that don't. That works fine locally, but it breaks down in two common real-world scenarios:

1. **CI environments without reliable network access** — if a live endpoint is slow or down, every test fails, including ones that have nothing to do with the network.
2. **Growing test suites** — as the number of tests scales, having no fixture layer or marker system makes it hard to run subsets (e.g., "just the fast tests before a deploy").

The pivot was to restructure the project around standard SDET practices without changing what the tests actually verify:

- A **session-scoped fixture** (`conftest.py`) replaces the module-level client, so the `APIClient` is created once and shared cleanly across all tests.
- **Markers** (`live`, `mocked`, `smoke`) let you run any subset in isolation — `pytest -m "not live"` skips all network calls.
- **Mocked tests** (`test_posts_mocked.py`, `test_posts_unittest.py`) cover the same logic as the live tests but with no network dependency, making them safe for CI and fast local feedback.
- **Unit tests for utilities** (`test_validators.py`) directly test the `validate_keys` helper, which was previously only exercised indirectly through live endpoint tests.
- **CI was updated** to run the mocked suite first (fast, always safe), then the full suite, and upload JUnit XML artifacts for result tracking.

The end result is a framework that demonstrates all the same capabilities as before, but with a clear separation of concerns and a test suite that's reliable in any environment.

## Features
- Custom API client abstraction for reusable request handling
- Session-scoped pytest fixture via `conftest.py`
- Data-driven testing using pytest parametrization
- Mocked tests using `@patch` from `unittest.mock` and `pytest-mock`'s `mocker` fixture (no network required)
- Explicit `FakeResponse` class as a test double — exposes only `status_code`, `json()`, and `raise_for_status()`, making unintended calls fail loudly instead of silently
- `unittest.TestCase`-style tests alongside native pytest tests
- Unit tests for utility functions
- Pytest markers (`live`, `mocked`, `smoke`) for filtering test runs — note these are labels only; the actual mocking is done by `@patch`
- Validation of REST endpoints (GET, POST, edge cases)
- CI/CD pipeline via GitHub Actions with staged test runs and artifact upload

## Tech Stack
- Python 3.12
- pytest
- pytest-mock
- requests
- GitHub Actions

## Project Structure
```
API-Test-Framework/
├── .github/
│   └── workflows/
│       └── tests.yml
├── data/
│   └── test_data.json
├── tests/
│   ├── conftest.py              # session-scoped api_client fixture
│   ├── test_posts.py            # live integration tests
│   ├── test_posts_mocked.py     # mocked tests (unittest.mock + pytest-mock)
│   ├── test_posts_unittest.py   # unittest.TestCase style
│   └── test_validators.py       # unit tests for validate_keys utility
├── utils/
│   ├── api_client.py
│   ├── logger.py
│   └── validators.py
├── pytest.ini
└── requirements.txt
```

## How to Run

Install dependencies:
```bash
pip install -r requirements.txt
```

Run all tests:
```bash
pytest -v
```

Run only mocked tests (no network required):
```bash
pytest -m "mocked" -v
```

Run only live integration tests:
```bash
pytest -m "live" -v
```

Skip live tests (safe for offline/CI use):
```bash
pytest -m "not live" -v
```

## Test Coverage
- Response status code validation
- Response schema and required field validation
- Data-driven API validation across multiple inputs (`test_data.json`)
- Edge case handling (invalid endpoints, empty responses)
- Network failure simulation via mocked `ConnectionError`
- Mocked POST requests with payload and ID verification
- Unit tests for `validate_keys`: normal, edge, failure, and parametrized cases

## Future Improvements
- Parallel test execution (pytest-xdist)
- Advanced reporting (Allure)
- Retry logic for flaky tests
- Environment-based configuration (dev/staging/prod)
