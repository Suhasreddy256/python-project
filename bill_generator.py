from datetime import datetime
from collections import defaultdict
from calendar import monthrange

def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")

def get_month_start_end(target_month):
    year, month = map(int, target_month.split("-"))
    start = datetime(year, month, 1)
    end = datetime(year, month, monthrange(year, month)[1])
    return start, end

def days_overlap(start1, end1, start2, end2):
    latest_start = max(start1, start2)
    earliest_end = min(end1, end2)
    delta = (earliest_end - latest_start).days + 1
    return max(0, delta), latest_start, earliest_end

def clean_item(item):
    item["rate"] = float(item["rate"])
    item["qty"] = int(item["qty"])
    item["amount"] = float(item["amount"])
    item["start_date"] = parse_date(item["start_date"])
    item["stop_date"] = parse_date(item["stop_date"])
    return item

def generate_monthly_bill(item_list: list, target_month: str) -> dict:
    start_of_month, end_of_month = get_month_start_end(target_month)
    total_days_in_month = (end_of_month - start_of_month).days + 1

    grouped = defaultdict(lambda: {"qty": 0, "amount": 0.0})

    for item in item_list:
        item = clean_item(item)
        active_days, bill_start, bill_end = days_overlap(
            item["start_date"], item["stop_date"], start_of_month, end_of_month
        )

        if active_days > 0:
            billing_period = f"{bill_start.strftime('%Y-%m-%d')} to {bill_end.strftime('%Y-%m-%d')}"
            daily_rate = item["rate"] / total_days_in_month
            amount = round(daily_rate * active_days * item["qty"], 2)

            key = (item["item_code"], item["rate"], billing_period)
            grouped[key]["qty"] += item["qty"]
            grouped[key]["amount"] += amount

    line_items = []
    total_revenue = 0.0

    for (item_code, rate, billing_period), data in grouped.items():
        amount = round(data["amount"], 2)
        total_revenue += amount
        line_items.append({
            "item_code": item_code,
            "rate": rate,
            "qty": data["qty"],
            "amount": amount,
            "billing_period": billing_period
        })

    return {
        "line_items": line_items,
        "total_revenue": round(total_revenue, 2)
    }
