"""Dummy sale/discount helpers for the toy catalog."""

from __future__ import annotations


def apply_discount(products: list[dict], percent: float, category: str | None = None) -> list[dict]:
    """Return copies of products with `percent` off (optionally for one category)."""
    if not 0 <= percent <= 100:
        raise ValueError("percent must be between 0 and 100")
    out = []
    for p in products:
        q = dict(p)
        if category is None or p["category"] == category.lower():
            q["price"] = round(p["price"] * (1 - percent / 100), 2)
        out.append(q)
    return out
