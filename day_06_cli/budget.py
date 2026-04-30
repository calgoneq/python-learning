import argparse
from datetime import datetime

from pathlib import Path
from storage import load_json, backup_json, append_transaction, delete_transaction

HERE = Path(__file__).parent
TRANSACTIONS_FILE = HERE / "transactions.json"
PLANNED_FILE = HERE / "planned.json"

DNI_DANYCH: int = 3
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
    
    if monthly_burn <= 0: 
        raise ValueError("monthly_burn musi być dodatni!")

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
💰 BUDGET v4 — breakdown
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

    avg: float = spent / DNI_DANYCH
    monthly_burn: float = avg * 30
    b_start     = calculate_runway(balance, monthly_burn)
    b_spend     = calculate_runway(balance - spent, monthly_burn)
    b_obligated = calculate_runway(balance - spent - zaplanowane, monthly_burn)

    print(f"""🔮 Runway (3 scenariusze):
  Od salda startowego:        {b_start} mies
  Od salda po wydatkach:      {b_spend} mies
  Od salda po zobowiązaniach: {b_obligated} mies""")

def cmd_report(args) -> None:
    '''Loads transaction and planned files and prints report. Impure'''
    transactions = load_json(TRANSACTIONS_FILE)
    planned = load_json(PLANNED_FILE)
    print_report(SALDO, transactions, planned)

def cmd_add(args) -> None:
    '''Adds new transaction record. Impure'''

    transaction: dict = {
        "sklep": args.sklep,
        "kwota": args.kwota,
        "kategoria": args.kategoria,
        "data": args.data
    }

    append_transaction(transaction, TRANSACTIONS_FILE)
    print(f"Dodano: {transaction['sklep']} | {transaction['kwota']:.2f} zł | {transaction['kategoria']}")

def cmd_delete(args) -> None:
    '''Removes specified transaction record'''
    transactions = load_json(TRANSACTIONS_FILE)
    if len(transactions) == 0:
        print("Brak transakcji do usunięcia.")
        return

    internal_index = args.index - 1

    if internal_index not in range(0, len(transactions)):
        print(f"Błąd: nie ma transakcji o indeksie {internal_index}. Lista ma {len(transactions)} pozycji.")
        return
    
    print(f"Usunięto pozycję {args.index}: {transactions[internal_index]['sklep']} | {transactions[internal_index]['kwota']:.2f} zł")
    delete_transaction(transactions[internal_index], TRANSACTIONS_FILE)

def cmd_backup(args) -> None:
    '''Tworzy backup danych transakcji'''
    dest_path: str = args.dest
    backup_json(TRANSACTIONS_FILE, dest_path)
    print(f"Backup utworzony: {dest_path}")

HANDLERS = {
    "report": cmd_report,
    "add": cmd_add,
    "delete": cmd_delete,
    "backup": cmd_backup
}

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Command 1: report
    hello_parser = subparsers.add_parser("report", help="Sends report")

    # Command 2: add
    add_parser = subparsers.add_parser("add", help="Adds transaction")
    add_parser.add_argument("--sklep", type=str, required=True)
    add_parser.add_argument("--kwota", type=float, required=True)
    add_parser.add_argument("--kategoria", type=str, required=True)
    add_parser.add_argument("--data", type=str, default=datetime.today().strftime("%Y-%m-%d"))
   
    # Command 3: delete
    del_parser = subparsers.add_parser("delete", help="Adds transaction")
    del_parser.add_argument("--index", type=int, required=True)

    # Command 4: backup
    backup_parser = subparsers.add_parser("backup", help="Adds transaction")
    backup_parser.add_argument("--dest", type=str, default= HERE / "backup_dir")

    args = parser.parse_args()

    if args.command == "add" and args.kwota <= 0:
        parser.error(f"Kwota musi być większa lub równa zero")
    
    handler = HANDLERS[args.command]
    handler(args)

if __name__ == "__main__":
    main()