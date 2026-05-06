import argparse
from datetime import datetime
import sys
from pathlib import Path
import logging

from storage import load_json, backup_json, append_transaction, delete_transaction
from filters import filter_by_date_range, parse_date, sort_transaction_by_date
from exceptions import FileCorruptedError
from config import HERE, TRANSACTIONS_FILE, PLANNED_FILE, DNI_DANYCH, LINE, LINE_THIN, SALDO

logger = logging.getLogger(__name__)

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
    months: int = 0
    
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
    try:
        transactions = load_json(TRANSACTIONS_FILE)
    except FileCorruptedError as e:
        logger.error("Nie można wczytać transakcji: %s", e)
        args.parser.error(str(e))
    sorted_data = sort_transaction_by_date(transactions)
    filtered_data = filter_by_date_range(sorted_data, args.od, args.do)
    planned = load_json(PLANNED_FILE)
    print_report(SALDO, filtered_data, planned)

def cmd_add(args) -> None:
    '''Adds new transaction record. Impure'''

    transaction: dict = {
        "sklep": args.sklep,
        "kwota": args.kwota,
        "kategoria": args.kategoria,
        "data": args.data
    }
    try:
        append_transaction(transaction, TRANSACTIONS_FILE)
    except FileCorruptedError as e:
        logger.error("Nie można wczytać transakcji: %s", e)
        args.parser.error(str(e))
    print(f"Dodano: {transaction['sklep']} | {transaction['kwota']:.2f} zł | {transaction['kategoria']}")

def cmd_delete(args) -> None:
    '''Removes specified transaction record'''
    
    try:
        transactions = load_json(TRANSACTIONS_FILE)
    except FileCorruptedError as e:
        logger.error("Nie można wczytać transakcji: %s", e)
        args.parser.error(str(e))
    
    if len(transactions) == 0:
        print("Brak transakcji do usunięcia.")
        return

    internal_index: int = args.index - 1

    if internal_index not in range(0, len(transactions)):
        print(f"Błąd: nie ma transakcji o indeksie {internal_index}. Lista ma {len(transactions)} pozycji.")
        sys.exit(1)
    
    print(f"Usunięto pozycję {args.index}: {transactions[internal_index]['sklep']} | {transactions[internal_index]['kwota']:.2f} zł")
    
    try:
        delete_transaction(transactions[internal_index], TRANSACTIONS_FILE)
    except FileCorruptedError as e:
        logger.error("Nie można wczytać transakcji: %s", e)
        args.parser.error(str(e))

def cmd_backup(args) -> None:
    '''Tworzy backup danych transakcji'''
    dest_path = args.dest

    if not dest_path.exists():
        print(f"WARNING: default folder nie istniał, stworzono nowy w {dest_path}")
        dest_path.mkdir()

    backup_json(TRANSACTIONS_FILE, dest_path)
    print(f"Backup utworzony: {dest_path}")

def cmd_categories(args) -> None:
    '''Tworzy zestawienie wydatków dla każdej kategori'''
    transactions = load_json(TRANSACTIONS_FILE)
    data = sum_by_category(transactions)
    for category, sum in data.items():
        print(f"{category}: {sum:.2f} zł")

HANDLERS = {
    "report": cmd_report,
    "add": cmd_add,
    "delete": cmd_delete,
    "backup": cmd_backup,
    "categories": cmd_categories
}

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    report_parser = subparsers.add_parser("report", help="Sends report")
    report_parser.add_argument("--od", type=str, default=None)
    report_parser.add_argument("--do", type=str, default=None)

    add_parser = subparsers.add_parser("add", help="Adds transaction")
    add_parser.add_argument("--sklep", type=str, required=True)
    add_parser.add_argument("--kwota", type=float, required=True)
    add_parser.add_argument("--kategoria", type=str, required=True)
    add_parser.add_argument("--data", type=str, default=datetime.today().strftime("%Y-%m-%d"))
   
    del_parser = subparsers.add_parser("delete", help="Remove transaction")
    del_parser.add_argument("--index", type=int, required=True)

    backup_parser = subparsers.add_parser("backup", help="Create backup folder")
    backup_parser.add_argument("--dest", type=Path, default= HERE / "backup_dir")

    category_parser = subparsers.add_parser("categories", help="Prints sums for each category")

    args = parser.parse_args()
    args.parser = parser

    if args.command == "add" and args.kwota < 0:
        parser.error(f"Kwota musi być większa od zero")

    if args.command == "report" and args.od:
        try:
            parse_date(args.od)
        except ValueError:
            parser.error(f"Format daty '{args.od}' jest zły! Użyj YYYY-MM-DD")

    if args.command == "report" and args.do:
        try:
            parse_date(args.do)
        except ValueError:
            parser.error(f"Format daty '{args.do}' jest zły! Użyj YYYY-MM-DD")

    handler = HANDLERS[args.command]
    handler(args)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )
    main()