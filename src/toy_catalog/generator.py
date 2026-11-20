"""Generate random toy product data and persist it as JSON."""

from __future__ import annotations

import json
import random
from pathlib import Path

CATEGORIES = {
    "car": ["Racer", "Roadster", "Coupe", "Convertible", "Rally"],
    "truck": ["Dump Truck", "Fire Truck", "Tow Truck", "Pickup", "Cement Mixer"],
    "plane": ["Jet", "Biplane", "Glider", "Cargo Plane"],
    "train": ["Steam Engine", "Express", "Freight Train"],
    "robot": ["Bot", "Mech", "Droid"],
}
ADJECTIVES = ["Turbo", "Mighty", "Tiny", "Super", "Rapid", "Classic", "Mega", "Shiny"]


def generate_products(count: int = 10, seed: int | None = None) -> list[dict]:
    """Return `count` random products with id, name, price and category."""
    rng = random.Random(seed)
    products = []
    for i in range(1, count + 1):
        category = rng.choice(list(CATEGORIES))
        name = f"{rng.choice(ADJECTIVES)} {rng.choice(CATEGORIES[category])}"
        products.append(
            {
                "id": i,
                "name": name,
                "price": round(rng.uniform(4.99, 79.99), 2),
                "category": category,
            }
        )
    return products


def save_products(products: list[dict], path: str | Path) -> Path:
    path = Path(path)
    path.write_text(json.dumps(products, indent=2) + "\n", encoding="utf-8")
    return path
