"""Command line interface: `toy-catalog generate|list`."""

from __future__ import annotations

import argparse

from .catalog import filter_by_category, format_catalog, load_products
from .generator import generate_products, save_products

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

    args = parser.parse_args(argv)
    if args.command == "generate":
        path = save_products(generate_products(args.count, args.seed), args.output)
        print(f"Wrote {args.count} products to {path}")
    else:
        print(format_catalog(filter_by_category(load_products(args.file), args.category)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
