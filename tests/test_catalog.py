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
