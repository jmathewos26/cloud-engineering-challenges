# Cloud Engineering Challenges: Project Repo

Hands-on solutions to five common cloud engineering team problems. Each folder is a small, runnable lab.

## What's in here

| Folder | Problem it addresses | What it does |
|---|---|---|
| `problem1-data-standardization` | Data source variability | Converts a CSV and a JSON feed into one standard format and rejects bad records with reasons |
| `problem2-monitoring` | Reactive monitoring | Prometheus + Grafana stack with a dashboard and an alert on error rate |
| `problem3-automation` | Resource constraints | Health-check script that runs automatically every 5 minutes |
| `docs` | Missing documentation | Runbook and onboarding guide |
| `.github/workflows` and `problem1-data-standardization/test_normalize.py` | Missing CI/CD | GitHub Actions pipeline that runs 7 unit tests, then validates and builds the monitoring app on every push |

## Prerequisites
- Windows with PowerShell (VS Code terminal works)
- Git, Python 3, and Docker Desktop (running)

## Quick start

Data standardization:
```
cd problem1-data-standardization
python normalize.py
```

Monitoring stack (Docker Desktop must be open):
```
cd problem2-monitoring
docker compose up -d
```
- Grafana: http://localhost:3000 (local lab login: admin / admin)
- Prometheus: http://localhost:9090
- Demo app metrics: http://localhost:8000

Health check (stack must be running):
```
cd problem3-automation
python health_check.py
```

## Documentation
- [Runbook: High error rate alert](docs/runbook-high-error-rate.md)
- [New teammate onboarding](docs/onboarding.md)

## Keeping docs current
- Every change to a lab updates its docs in the same commit.
- Docs are reviewed once a month.
- If a doc is wrong or confusing, fix it or open an issue. Don't work around it silently.