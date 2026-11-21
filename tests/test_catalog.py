from toy_catalog.catalog import filter_by_category, format_catalog
from toy_catalog.cli import main
from toy_catalog.generator import CATEGORIES, generate_products


def test_generate_shape():
    products = generate_products(20, seed=1)
    assert len(products) == 20
    for p in products:
        assert set(p) == {"id", "name", "price", "category"}
        assert p["category"] in CATEGORIES
        assert 4.99 <= p["price"] <= 79.99


def test_seed_is_deterministic():
    assert generate_products(5, seed=7) == generate_products(5, seed=7)


def test_filter_and_format():
    products = generate_products(30, seed=3)
    cars = filter_by_category(products, "car")
    assert all(p["category"] == "car" for p in cars)
    assert "item(s)" in format_catalog(cars)


def test_cli_roundtrip(tmp_path, capsys):
    out = tmp_path / "p.json"
    assert main(["generate", "-n", "5", "--seed", "1", "-o", str(out)]) == 0
    assert main(["list", "-f", str(out)]) == 0
    assert "5 item(s)" in capsys.readouterr().out


def test_search_and_stats(tmp_path, capsys):
    from toy_catalog.stats import category_summary, search

    products = generate_products(40, seed=5)
    hits = search(products, "TURBO")
    assert all("turbo" in p["name"].lower() for p in hits)
    summary = category_summary(products)
    assert sum(v["count"] for v in summary.values()) == 40

    out = tmp_path / "p.json"
    main(["generate", "-n", "10", "--seed", "2", "-o", str(out)])
    assert main(["stats", "-f", str(out)]) == 0
    assert "CATEGORY" in capsys.readouterr().out


def test_discount():
    import pytest

    from toy_catalog.discounts import apply_discount

    products = [{"id": 1, "name": "A", "price": 10.0, "category": "car"},
                {"id": 2, "name": "B", "price": 20.0, "category": "truck"}]
    assert apply_discount(products, 50)[0]["price"] == 5.0
    sale = apply_discount(products, 50, "truck")
    assert sale[0]["price"] == 10.0 and sale[1]["price"] == 10.0
    with pytest.raises(ValueError):
        apply_discount(products, 150)
