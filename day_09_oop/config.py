from pathlib import Path

HERE = Path(__file__).parent
TRANSACTIONS_FILE = HERE / "transactions.json"
PLANNED_FILE = HERE / "planned.json"

DNI_DANYCH: int = 3
LINE = "=" * 40
LINE_THIN = "-" * 40
SALDO: float = 3311.0