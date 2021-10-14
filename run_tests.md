# Tests

How to run the tests:
* python setup.py pytest
* pytest tests/
* pytest --cov-report term --cov=sara/core tests/

How to check the test coverage with HTML report:
* pytest --cov-report=html --cov=sara/core tests/

Requirements:
- pytest
- pytest-cov
