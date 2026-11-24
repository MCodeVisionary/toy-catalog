"""Add, update and remove products in the catalog."""

from __future__ import annotations

from datetime import date

from .generator import CATEGORIES


def next_id(products: list[dict]) -> int:
    return max((p["id"] for p in products), default=0) + 1


def add_product(products: list[dict], name: str, price: float, category: str, published: str | None = None) -> list[dict]:
    """Return a new list with the product appended (id auto-assigned)."""
    category = category.lower()
    if category not in CATEGORIES:
        raise ValueError(f"unknown category '{category}', choose from: {', '.join(CATEGORIES)}")
    if price <= 0:
        raise ValueError("price must be positive")
    if not name.strip():
        raise ValueError("name is required")
    published = published or date.today().isoformat()
    date.fromisoformat(published)  # raises ValueError for a bad date
    return [
        *products,
        {"id": next_id(products), "name": name.strip(), "price": round(price, 2), "category": category, "published": published},
    ]


def remove_product(products: list[dict], product_id: int) -> list[dict]:
    if not any(p["id"] == product_id for p in products):
        raise KeyError(f"no product with id {product_id}")
    return [p for p in products if p["id"] != product_id]


def update_price(products: list[dict], product_id: int, price: float) -> list[dict]:
    if price <= 0:
        raise ValueError("price must be positive")
    if not any(p["id"] == product_id for p in products):
        raise KeyError(f"no product with id {product_id}")
    return [{**p, "price": round(price, 2)} if p["id"] == product_id else p for p in products]
