"""Command line interface: `toy-catalog generate|list`."""

from __future__ import annotations

import argparse

from .catalog import filter_by_category, format_catalog, load_products
from .generator import generate_products, save_products
from .discounts import apply_discount
from .stats import category_summary, format_summary, search

DEFAULT_FILE = "products.json"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="toy-catalog", description="Toy product catalog")
    sub = parser.add_subparsers(dest="command", required=True)

    gen = sub.add_parser("generate", help="generate random products into a JSON file")
    gen.add_argument("-n", "--count", type=int, default=10)
    gen.add_argument("--seed", type=int)
    gen.add_argument("-o", "--output", default=DEFAULT_FILE)

    lst = sub.add_parser("list", help="show the catalog")
    lst.add_argument("-f", "--file", default=DEFAULT_FILE)
    lst.add_argument("-c", "--category")

    srch = sub.add_parser("search", help="search products by name")
    srch.add_argument("term")
    srch.add_argument("-f", "--file", default=DEFAULT_FILE)

    stats = sub.add_parser("stats", help="per-category price summary")
    stats.add_argument("-f", "--file", default=DEFAULT_FILE)

    sale = sub.add_parser("sale", help="show the catalog with a discount applied")
    sale.add_argument("percent", type=float)
    sale.add_argument("-f", "--file", default=DEFAULT_FILE)
    sale.add_argument("-c", "--category")

    args = parser.parse_args(argv)
    if args.command == "generate":
        path = save_products(generate_products(args.count, args.seed), args.output)
        print(f"Wrote {args.count} products to {path}")
    elif args.command == "search":
        print(format_catalog(search(load_products(args.file), args.term)))
    elif args.command == "sale":
        print(format_catalog(apply_discount(load_products(args.file), args.percent, args.category)))
    elif args.command == "stats":
        print(format_summary(category_summary(load_products(args.file))))
    else:
        print(format_catalog(filter_by_category(load_products(args.file), args.category)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
