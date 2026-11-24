"""Load and display the toy catalog."""

from __future__ import annotations

import json
from pathlib import Path


def load_products(path: str | Path) -> list[dict]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def filter_by_category(products: list[dict], category: str | None) -> list[dict]:
    if not category:
        return products
    return [p for p in products if p["category"] == category.lower()]


def published_since(products: list[dict], since: str) -> list[dict]:
    """Products published on or after `since` (ISO date, e.g. 2026-01-01)."""
    return [p for p in products if p.get("published", "") >= since]


def format_catalog(products: list[dict]) -> str:
    """Render products as a fixed-width table."""
    header = f"{'ID':<4}{'NAME':<24}{'CATEGORY':<10}{'PUBLISHED':<12}{'PRICE':>8}"
    lines = [header, "-" * len(header)]
    for p in products:
        lines.append(
            f"{p['id']:<4}{p['name']:<24}{p['category']:<10}{p.get('published', '-'):<12}"
            f"{'$' + format(p['price'], '.2f'):>8}"
        )
    lines.append(f"\n{len(products)} item(s)")
    return "\n".join(lines)
