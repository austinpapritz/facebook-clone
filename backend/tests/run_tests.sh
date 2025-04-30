#!/bin/bash

# Run all tests
pytest

# Run only model tests
pytest -m model

# Run only route tests
pytest -m route

# Run only database tests
pytest -m db

# Generate coverage report
pytest --cov=app --cov-report=html