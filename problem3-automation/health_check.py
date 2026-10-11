import shutil
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).parent
LOG_DIR = BASE / "logs"
LOG_DIR.mkdir(exist_ok=True)

CHECKS = {
    "Prometheus": "http://localhost:9090/-/healthy",
    "Grafana": "http://localhost:3000/api/health",
    "Demo app metrics": "http://localhost:8000",
}
MIN_FREE_PERCENT = 10


def check_url(name, url):
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            ok = resp.status == 200
            return ok, f"HTTP {resp.status}"
    except Exception as e:
        return False, f"unreachable ({type(e).__name__})"


def check_disk():
    usage = shutil.disk_usage("C:\\")
    free_pct = usage.free / usage.total * 100
    return free_pct >= MIN_FREE_PERCENT, f"{free_pct:.1f}% free"


def main():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [f"=== Health check {now} ==="]
    failures = 0

    for name, url in CHECKS.items():
        ok, detail = check_url(name, url)
        lines.append(f"[{'OK' if ok else 'FAIL'}] {name}: {detail}")
        failures += 0 if ok else 1

    ok, detail = check_disk()
    lines.append(f"[{'OK' if ok else 'FAIL'}] Disk C: {detail}")
    failures += 0 if ok else 1

    lines.append(f"Result: {'ALL HEALTHY' if failures == 0 else str(failures) + ' CHECK(S) FAILED'}")
    report = "\n".join(lines)

    print(report)
    with open(LOG_DIR / "health_report.log", "a") as f:
        f.write(report + "\n\n")

    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()