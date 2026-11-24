from toy_catalog.catalog import filter_by_category, format_catalog
from toy_catalog.cli import main
from toy_catalog.generator import CATEGORIES, generate_products


def test_generate_shape():
    products = generate_products(20, seed=1)
    assert len(products) == 20
    for p in products:
        assert set(p) == {"id", "name", "price", "category", "published"}
        assert "2024-11-01" <= p["published"] <= "2026-11-01"
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


def test_inventory():
    from toy_catalog.inventory import add_stock, low_stock

    stocked = add_stock(generate_products(20, seed=1), seed=2)
    assert all(0 <= p["stock"] <= 50 for p in stocked)
    assert all(p["stock"] <= 5 for p in low_stock(stocked))
    assert add_stock(generate_products(3, seed=1), seed=9) == add_stock(generate_products(3, seed=1), seed=9)


def test_manage_products(tmp_path, capsys):
    import pytest

    from toy_catalog.manage import add_product, remove_product, update_price

    products = generate_products(3, seed=1)
    added = add_product(products, "Super Racer", 12.5, "CAR", "2026-05-01")
    assert added[-1] == {"id": 4, "name": "Super Racer", "price": 12.5, "category": "car", "published": "2026-05-01"}
    assert add_product(products, "Today Toy", 5, "car")[-1]["published"]
    assert len(products) == 3  # input not mutated
    assert len(remove_product(added, 4)) == 3
    assert update_price(added, 4, 9.99)[-1]["price"] == 9.99
    with pytest.raises(ValueError):
        add_product(products, "X", 5, "spaceship")
    with pytest.raises(KeyError):
        remove_product(products, 99)

    out = tmp_path / "p.json"
    main(["generate", "-n", "2", "--seed", "1", "-o", str(out)])
    assert main(["add", "Mega Truck", "19.99", "truck", "-f", str(out)]) == 0
    assert main(["set-price", "3", "5", "-f", str(out)]) == 0
    assert main(["remove", "1", "-f", str(out)]) == 0
    assert main(["remove", "99", "-f", str(out)]) == 1
    main(["list", "-f", str(out)])
    assert "Mega Truck" in capsys.readouterr().out


def test_wishlist(tmp_path, capsys):
    import pytest

    from toy_catalog.wishlist import add_to_wishlist, wishlist_total

    products = [{"id": 1, "name": "A", "price": 10.0, "category": "car"},
                {"id": 2, "name": "B", "price": 5.5, "category": "truck"}]
    wl = add_to_wishlist([], 1, products)
    wl = add_to_wishlist(wl, 2, products)
    assert add_to_wishlist(wl, 2, products) == [1, 2]  # no duplicates
    assert wishlist_total(wl, products) == 15.5
    with pytest.raises(KeyError):
        add_to_wishlist(wl, 9, products)

    out, wlf = tmp_path / "p.json", tmp_path / "w.json"
    main(["generate", "-n", "3", "--seed", "1", "-o", str(out)])
    assert main(["wish", "1", "-f", str(out), "-w", str(wlf)]) == 0
    assert main(["wish", "99", "-f", str(out), "-w", str(wlf)]) == 1
    assert "Wishlist: [1]" in capsys.readouterr().out


def test_published_since(tmp_path, capsys):
    from toy_catalog.catalog import published_since

    products = [{"id": 1, "name": "Old", "price": 1.0, "category": "car", "published": "2025-01-01"},
                {"id": 2, "name": "New", "price": 2.0, "category": "car", "published": "2026-06-01"},
                {"id": 3, "name": "Legacy", "price": 3.0, "category": "car"}]
    assert [p["id"] for p in published_since(products, "2026-01-01")] == [2]
    out = tmp_path / "p.json"
    main(["generate", "-n", "10", "--seed", "4", "-o", str(out)])
    assert main(["list", "-f", str(out), "--since", "2026-01-01"]) == 0
    assert "PUBLISHED" in capsys.readouterr().out
