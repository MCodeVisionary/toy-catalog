"""Dummy wishlist helpers for the toy catalog."""

from __future__ import annotations

import json
from pathlib import Path


def add_to_wishlist(wishlist: list[int], product_id: int, products: list[dict]) -> list[int]:
    """Return a new wishlist with product_id added (must exist, no duplicates)."""
    if not any(p["id"] == product_id for p in products):
        raise KeyError(f"no product with id {product_id}")
    return wishlist if product_id in wishlist else [*wishlist, product_id]


def wishlist_total(wishlist: list[int], products: list[dict]) -> float:
    """Sum of prices of wishlisted products."""
    prices = {p["id"]: p["price"] for p in products}
    return round(sum(prices[i] for i in wishlist if i in prices), 2)


def load_wishlist(path: str | Path) -> list[int]:
    path = Path(path)
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


def save_wishlist(wishlist: list[int], path: str | Path) -> Path:
    path = Path(path)
    path.write_text(json.dumps(wishlist) + "\n", encoding="utf-8")
    return path
