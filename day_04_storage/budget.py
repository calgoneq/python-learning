from pathlib import Path
from storage import load_json, backup_json

HERE = Path(__file__).parent
TRANSACTIONS_FILE = HERE / "transactions.json"
PLANNED_FILE = HERE / "planned.json"

LINE = "=" * 40
LINE_THIN = "-" * 40
SALDO: float = 3311.0

def sum_by_category(transactions: list[dict]) -> dict[str, float]:
    """Suma kwot per kategoria. Pure."""
    kategorie_suma: dict = {}

    for item in transactions:
        kat = item.get('kategoria', "BRAK")
        kategorie_suma[kat] = kategorie_suma.get(kat, 0.0) + item['kwota']
    
    return kategorie_suma

def total_amount(items: list[dict], key: str = "kwota") -> float:
    """Suma wybranego klucza ze wszystkich dictów w liście. Pure."""
    amount: float = 0.00
    for item in items:
        amount += item[key]
    return amount

def calculate_runway(balance: float, monthly_burn: float) -> int:
    """Ile miesięcy wytrzyma `balance` przy `monthly_burn`."""
    months = 0
    while balance > 0:
        balance -= monthly_burn
        months += 1
    return months

def format_transaction_line(t: dict, index: int) -> str:
    """Jeden rekord transakcji. Pure."""
    transaction = f"{index:>3}. {t['data']} | {t['sklep']:<10} | {t['kwota']:>7.2f} zł | {t['kategoria']}"

    return transaction

def format_planned_line(p: dict) -> str:
    """Jeden rekod zobowiązań. Pure."""
    planned = f"- {p['opis']:<17} | {p['kwota']:>10.2f} zł | do {p['deadline']}"

    return planned


def print_report(balance: float, transactions: list[dict], planned: list[dict]) -> None:
    """Orchestrator — wywołuje funkcje wyżej i printuje raport. Impure."""
   
    print(f"""{LINE}
💰 BUDGET v3 — breakdown
{LINE}
Saldo startowe: {balance:.2f} zł\n
📋 Transakcje ({len(transactions)}):""")
 
    for i, item in enumerate(transactions, start=1):
        transaction = format_transaction_line(item, i)
        print(transaction)

    print(f"""{LINE_THIN}\n📊 Podsumowanie kategorii:""")
    
    summed_categories = sum_by_category(transactions)
    
    for key, value in summed_categories.items():
        print(f"{key:<9}:{value:>7.2f} zł")

    spent = total_amount(transactions)

    print(f"""
💸 {"Łącznie wydane:":<20}{spent:.2f} zł
💰 {"Saldo po wydatkach: ":<20}{balance-spent:.2f} zł
{LINE_THIN}""")

    zaplanowane = total_amount(planned)

    print(f"🎯 Zobowiązania ({zaplanowane:.2f} zł):")

    for item in planned:
        planned_expense = format_planned_line(item)
        print(planned_expense)

    print(f"""
💰 Saldo po zobowiązaniach: {balance - spent - zaplanowane:.2f} zł
{LINE_THIN}""")

    avg: float = spent / 3
    monthly_burn: float = avg * 30
    b_start     = calculate_runway(balance, monthly_burn)
    b_spend     = calculate_runway(balance - spent, monthly_burn)
    b_obligated = calculate_runway(balance - spent - zaplanowane, monthly_burn)

    print(f"""🔮 Runway (3 scenariusze):
  Od salda startowego:        {b_start} mies
  Od salda po wydatkach:      {b_spend} mies
  Od salda po zobowiązaniach: {b_obligated} mies""")

if __name__ == "__main__":
    transactions = load_json(TRANSACTIONS_FILE)
    planned = load_json(PLANNED_FILE)
    print_report(SALDO, transactions, planned)