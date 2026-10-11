import csv
import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).parent

# Common data format (our "contract"):
# record_id, source, timestamp (ISO 8601 UTC), customer_id,
# amount_usd (number), status (completed | pending | failed)
STATUS_MAP = {
    "paid": "done".,
    "completed": "completed",
    "pending": "pending",
    "failed": "failed",
}


def parse_money(value):
    return round(float(str(value).replace("$", "").replace(",", "")), 2)


def normalize_a(row):
    ts = datetime.strptime(row["order_date"], "%m/%d/%Y").replace(tzinfo=timezone.utc)
    return {
        "record_id": row["order_id"],
        "source": "finance_csv",
        "timestamp": ts.isoformat(),
        "customer_id": row["customer"].strip(),
        "amount_usd": parse_money(row["total"]),
        "status": STATUS_MAP[row["state"].strip().lower()],
    }


def normalize_b(item):
    ts = datetime.fromtimestamp(int(item["created"]), tz=timezone.utc)
    return {
        "record_id": item["id"],
        "source": "web_api",
        "timestamp": ts.isoformat(),
        "customer_id": item["customer_id"].strip(),
        "amount_usd": parse_money(item["amount"]),
        "status": STATUS_MAP[item["status"].strip().lower()],
    }


def validate(rec):
    errors = []
    if not rec["customer_id"]:
        errors.append("missing customer_id")
    if rec["amount_usd"] < 0:
        errors.append("negative amount")
    return errors


def process(records, normalizer, label, clean, rejected):
    for raw in records:
        try:
            rec = normalizer(raw)
            errors = validate(rec)
        except (ValueError, KeyError) as e:
            rejected.append({"source": label, "raw": raw, "reason": f"cannot parse: {e}"})
            continue
        if errors:
            rejected.append({"source": label, "raw": raw, "reason": "; ".join(errors)})
        else:
            clean.append(rec)


def main():
    clean, rejected = [], []

    with open(BASE / "data" / "source_a.csv", newline="") as f:
        process(csv.DictReader(f), normalize_a, "finance_csv", clean, rejected)

    with open(BASE / "data" / "source_b.json") as f:
        process(json.load(f), normalize_b, "web_api", clean, rejected)

    (BASE / "output" / "clean.json").write_text(json.dumps(clean, indent=2))
    (BASE / "output" / "rejected.json").write_text(json.dumps(rejected, indent=2))

    print(f"Clean records:    {len(clean)}")
    print(f"Rejected records: {len(rejected)}")
    for r in rejected:
        print(f"  - {r['raw'].get('order_id') or r['raw'].get('id')}: {r['reason']}")


if __name__ == "__main__":
    main()