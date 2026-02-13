.PHONY: help install dev test lint format clean run docker-build docker-run

help:
	@echo "Catholic Network Tools - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install        Install dependencies"
	@echo "  make install-dev    Install dev dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make dev            Run development server"
	@echo "  make lint           Run linting checks"
	@echo "  make format         Format code (black + isort)"
	@echo "  make test           Run tests with coverage"
	@echo "  make security       Run security checks"
	@echo ""
	@echo "Deployment:"
	@echo "  make docker-build   Build Docker image"
	@echo "  make docker-run     Run Docker container"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean          Remove build artifacts"
	@echo "  make docs           Build documentation"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev,offline,sms,postgres]"

dev:
	uvicorn catholic_network_tools.api.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest --cov=catholic_network_tools --cov-report=html --cov-report=term-missing

lint:
	ruff check .
	mypy catholic_network_tools

format:
	ruff check . --fix
	black catholic_network_tools
	isort catholic_network_tools

security:
	ruff check . --select S

clean:
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov

run:
	python -m catholic_network_tools.api.main

docker-build:
	docker build -t catholic-network-tools:latest .

docker-run:
	docker run --env-file .env -v ./data:/app/data -p 8000:8000 catholic-network-tools:latest

offline-test:
	pytest -k offline --cov=catholic_network_tools.resilience

sms-test:
	pytest -k sms --cov=catholic_network_tools.resilience

sync-test:
	pytest -k sync --cov=catholic_network_tools.coordination

smoke-test:
	pytest tests/smoke/ -v

