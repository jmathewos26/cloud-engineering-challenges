# New teammate onboarding

Welcome. This guide gets you from zero to running the labs on your first day.

## Day 1 checklist
- [ ] Install Git, Python 3, Docker Desktop, and VS Code
- [ ] Clone or open the project folder in VS Code
- [ ] Read the README
- [ ] Run the data standardization lab and read `output\rejected.json`
- [ ] Start the monitoring stack and open the Grafana dashboard
- [ ] Run the health check script
- [ ] Read the runbook

## Verify your tools
```
git --version
python --version
docker --version
docker run hello-world
```

## Where things are
| Need | Location |
|---|---|
| What the project is | README.md |
| What to do when the alert fires | docs\runbook-high-error-rate.md |
| Alert rules | problem2-monitoring\prometheus\alerts.yml |
| Dashboard | Grafana, "Service Health" |
| Health check script | problem3-automation\health_check.py |

## Common problems
| Symptom | Likely cause | Fix |
|---|---|---|
| `docker` command errors with "cannot find the file" | Docker Desktop isn't running | Open Docker Desktop and wait for it to start |
| Script says "No such file or directory" | Wrong folder, or file not saved | Run `dir` to check; confirm the file size is above 0 |
| Grafana won't load | Containers not running | `docker compose ps`, then `docker compose up -d` |
| `git commit` says "Please tell me who you are" | Git identity not set | Run `git config --global user.name` and `user.email` |

## Working agreements
- Verify with evidence (`dir`, logs, dashboards) before assuming something is broken.
- Commit small changes with clear messages.
- Update docs in the same commit as the change.
- Ask questions early.