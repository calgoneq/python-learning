from pathlib import Path

from storage import delete_transaction

HERE = Path(__file__).parent
TRANSACTION_FILE = HERE / "transactions.json"

transaction: dict = {"data": "2026-04-24", "sklep": "TEST", "kwota": 100.00,  "kategoria": "TESTY"}

delete_transaction(transaction=transaction, path=TRANSACTION_FILE)