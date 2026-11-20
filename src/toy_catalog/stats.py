"""Summary statistics and search over the toy catalog."""

from __future__ import annotations

from collections import defaultdict


def search(products: list[dict], term: str) -> list[dict]:
    """Case-insensitive substring search on product name."""
    term = term.lower()
    return [p for p in products if term in p["name"].lower()]


def category_summary(products: list[dict]) -> dict[str, dict]:
    """Per-category count, average and max price."""
    groups: dict[str, list[float]] = defaultdict(list)
    for p in products:
        groups[p["category"]].append(p["price"])
    return {
        cat: {
            "count": len(prices),
            "avg_price": round(sum(prices) / len(prices), 2),
            "max_price": max(prices),
        }
        for cat, prices in sorted(groups.items())
    }


def format_summary(summary: dict[str, dict]) -> str:
    lines = [f"{'CATEGORY':<10}{'COUNT':>6}{'AVG':>9}{'MAX':>9}"]
    for cat, s in summary.items():
        lines.append(f"{cat:<10}{s['count']:>6}{'$' + format(s['avg_price'], '.2f'):>9}{'$' + format(s['max_price'], '.2f'):>9}")
    return "\n".join(lines)
