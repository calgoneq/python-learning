import pytest
from fastapi.testclient import TestClient

import main
from main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_db(monkeypatch, tmp_path):
    d = tmp_path / "test_dir"
    d.mkdir()
    test_file = d / "test_transactions.json"
    test_file.write_text("[]")
    
    monkeypatch.setattr(main, "TRANSACTIONS_FILE", str(test_file))
    
def test_get_transaction():
    response = client.get("/transactions")
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.parametrize("sklep, kwota, kategoria, data, expected_status", [
    ("test_sklep", 10.2, "test_category", "2026-02-12", 201),
    ("test_sklep_incorrect_kwota", -10.2, "test_category_incorrect_kwota", "2026-02-12", 422),
    ("test_sklep_incorrect_kwota", 10.2, "test_category_incorrect_kwota", "abc", 422)
])

def test_post_transaction(sklep, kwota, kategoria, data, expected_status):
    body: dict = {
        "sklep": sklep,
        "kwota": kwota,
        "kategoria": kategoria,
        "data": data,
    }
    
    response = client.post("/transactions", json=body)
    assert response.status_code == expected_status

def test_get_after_new_transaction_returns_correct_json():
    new_transaction = {
        "sklep": "test_sklep",
        "kwota": 10.2,
        "kategoria": "test_category",
        "data": "2026-02-12",
    }
    client.post("/transactions", json=new_transaction)

    response = client.get("/transactions")
    data = response.json()

    assert response.status_code == 200
    assert any(t["sklep"] == "test_sklep" for t in data)

def test_get_with_kategoria_parameter_returns_correct_data():
    new_transactions = {
        "sklep": "test_sklep",
        "kwota": 10.2,
        "kategoria": "jedzenie",
        "data": "2026-02-12",
    }
    client.post("/transactions", json=new_transactions)

    response = client.get("/transactions?kategoria=jedzenie")
    data = response.json()
    assert response.status_code == 200
    assert any(t["kategoria"] == "jedzenie" for t in data)

def test_get_transaction_with_id_returns_only_transaction_with_correct_id():
    transaction_1: dict = {
        "sklep": "domino",
        "kwota": 18.5,
        "kategoria": "psy",
        "data": "2026-02-18",
    }

    transaction_2: dict = {
        "sklep": "niewiem",
        "kwota": 28.4,
        "kategoria": "zwierzęta",
        "data": "2026-02-15",
    }

    transaction_3: dict = {
        "sklep": "loco",
        "kwota": 12.7,
        "kategoria": "ludzie",
        "data": "2026-02-22",
    }

    client.post("/transactions", json=transaction_1)
    client.post("/transactions", json=transaction_2)
    client.post("/transactions", json=transaction_3)

    transaction_id = 1
    response = client.get(f"/transactions/{transaction_id}")
    data = response.json()

    assert response.status_code == 200
    assert "zwierzęta" in data["kategoria"]

def test_get_transaction_with_incorrect_id_returns_404():
    transaction_id = 200
    response = client.get(f"/transactions/{transaction_id}")

    assert response.status_code == 404
    data = response.json()
    assert str(transaction_id) in data["detail"]

def test_delete_transaction_removes_and_returns_200():
    transaction_to_delete = 1

    transaction_1: dict = {
        "sklep": "domino",
        "kwota": 18.5,
        "kategoria": "psy",
        "data": "2026-02-18",
    }

    transaction_2: dict = {
        "sklep": "niewiem",
        "kwota": 28.4,
        "kategoria": "zwierzęta",
        "data": "2026-02-15",
    }

    transaction_3: dict = {
        "sklep": "loco",
        "kwota": 12.7,
        "kategoria": "ludzie",
        "data": "2026-02-22",
    }

    client.post("/transactions", json=transaction_1)
    client.post("/transactions", json=transaction_2)
    client.post("/transactions", json=transaction_3)

    before_delete = client.get('/transactions')
    before_data = before_delete.json()

    response = client.delete(f"/transactions/{transaction_to_delete}")

    assert response.status_code == 200

    after_delete = client.get('/transactions')
    after_data = after_delete.json()

    assert len(before_data) > len(after_data)