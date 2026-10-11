# Runbook: HighErrorRate alert

**Alert:** `HighErrorRate`
**Fires when:** more than 10% of requests return HTTP 500 for at least 30 seconds
**Severity:** critical
**Dashboard:** Grafana, "Service Health" (http://localhost:3000)

## What this means
Users are getting errors on a meaningful share of requests. Treat it as user-facing until proven otherwise.

## 1. Confirm it's real (2 minutes)
1. Open the Prometheus alerts page (http://localhost:9090/alerts) and confirm `HighErrorRate` is **Firing**.
2. Open the Grafana "Error rate" panel. Is the rate still above the red 10% line, or already dropping?
3. Check the other panels: did request rate, p95 latency, or queue depth change at the same time?

## 2. Check the basics
```
docker compose ps
docker compose logs app --tail 50
```
- Are all three services running?
- Do the app logs show errors or restarts?

## 3. Mitigate
Try the least risky action first:
1. If the app container is unhealthy: `docker compose restart app`
2. If a recent change was deployed: roll it back.
3. If errors continue after a restart: escalate (step 4).

## 4. Escalate
Escalate if the error rate is still above 10% after 15 minutes, or if you're unsure. Tell the on-call lead:
- When the alert started
- What you checked and what you saw
- What you tried

Asking for help early is expected, not a failure.

## 5. After the incident
- Note the start time, end time, and cause.
- Did the alert fire quickly enough? Was the threshold right?
- Update this runbook if any step was wrong or missing.

## Lab note
In the demo app, an incident is simulated for one minute of every 5-minute cycle, so this alert resolves on its own. A real incident would not.