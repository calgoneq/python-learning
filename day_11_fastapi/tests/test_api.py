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
    ("test_sklep_incorrect_kwota", -10.2, "test_category_incorrect_kwota", "2026-02-12", 422)
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