## CI Status
![Tests](https://github.com/HoJungjae/api-test-automation-framework/actions/workflows/tests.yml/badge.svg)

# API Test Automation Framework

## Overview
This project demonstrates a scalable API test automation framework built using Python and pytest. It simulates real-world SDET practices including modular design, data-driven testing, and CI/CD integration.

## Features
- Custom API client abstraction for reusable request handling
- Data-driven testing using pytest parametrization
- Validation of REST endpoints (GET, POST, edge cases)
- Modular utilities for response validation
- CI/CD pipeline via GitHub Actions (runs on every push)

## Tech Stack
- Python
- pytest
- requests
- GitHub Actions

## Project Structure
api-test-framework/
│── tests/
│── utils/
│── data/
│── .github/workflows/

## How to Run
pip install -r requirements.txt
pytest -v

## Example Test Coverage
- Validate response status codes
- Validate response schema and required fields
- Data-driven API validation across multiple inputs
- Edge case handling (invalid endpoints)

## Future Improvements
- Parallel test execution (pytest-xdist)
- Advanced reporting (Allure)
- Retry logic for flaky tests
- Environment-based configuration (dev/staging/prod)