"""Dummy inventory helpers for the toy catalog."""

from __future__ import annotations

import random


def add_stock(products: list[dict], seed: int | None = None, max_units: int = 50) -> list[dict]:
    """Return copies of products with a random `stock` count."""
    rng = random.Random(seed)
    return [{**p, "stock": rng.randint(0, max_units)} for p in products]


def low_stock(products: list[dict], threshold: int = 5) -> list[dict]:
    """Products whose stock is at or below `threshold`."""
    return [p for p in products if p.get("stock", 0) <= threshold]
