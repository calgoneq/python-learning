from typing import Literal

# ========== DATA ==========

saldo: float = 3311.0
dni_danych: int = 3
LINE = "=" * 40
LINE_THIN = "-" * 40

transakcje: list[dict] = [
    {"data": "2026-04-19", "sklep": "Biedronka", "kwota": 87.50,  "kategoria": "jedzenie"},
    {"data": "2026-04-19", "sklep": "Żabka",     "kwota": 12.00,  "kategoria": "jedzenie"},
    {"data": "2026-04-20", "sklep": "Lidl",      "kwota": 134.20, "kategoria": "jedzenie"},
    {"data": "2026-04-20", "sklep": "Fryzjer",   "kwota": 60.00,  "kategoria": "styl"},
    {"data": "2026-04-20", "sklep": "Kreatyna",  "kwota": 45.00,  "kategoria": "zdrowie"},
    {"data": "2026-04-21", "sklep": "Kebab",     "kwota": 22.00,  "kategoria": "jedzenie"},
]

planowane: list[dict] = [
    {"opis": "Nizoral + Rexona", "kwota": 45.0, "deadline": "2026-04-26"},
    {"opis": "Fryzjer shaggy",    "kwota": 100.0, "deadline": "2026-05-05"},
    {"opis": "Perfumy Lattafa",   "kwota": 180.0, "deadline": "2026-05-15"},
]

# ========== FUNCTIONS ==========

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

def calculate_runway(balance: float, msc_burn: float, spent: float = 0.0, obligated: float = 0.0, mode: Literal["from_start", "from_current", "from_obligated"] = "from_current") -> int:
    """
    Liczy runway w miesiącach.
    
    mode='from_start': ile miesięcy wytrzyma się bez uwzględnienia już-poniesionych wydatków
    mode='from_current': ile jeszcze wytrzyma (balance to saldo PO wydatkach)
    mode='from_obligated': ile jeszcze wytrzyma (balance to saldo PO wydatkach i PO zobowiązaniach)
    """
    runway_msc: int = 0
    balance_current: float = balance - spent
    balance_obligated: float = balance_current - obligated

    if mode == "from_start":
        while balance > 0:
            balance -= msc_burn
            runway_msc +=1
    elif mode == "from_obligated":
        while balance_obligated > 0:
            balance_obligated -= msc_burn
            runway_msc +=1
    else:
        while balance_current > 0:
            balance_current -= msc_burn
            runway_msc +=1
    
    return runway_msc

def format_transaction_line(t: dict, index: int) -> str:
    """Jeden rekord transakcji. Pure."""
    transaction = f"{index:>3}. {t['data']} | {t['sklep']:<10} | {t['kwota']:>7.2f} zł | {t['kategoria']}"

    return transaction

def format_planned_line(p: dict) -> str:
    """Jeden rekod zobowiązań. Pure."""
    planned = f"- {p['opis']:<17} | {p['kwota']:>10.2f} zł | do {p['deadline']}"

    return planned

# ========== MAIN ==========

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

    avg: float = spent / dni_danych
    msc_burn: float = avg * 30

    b_start = calculate_runway(balance=balance, msc_burn=msc_burn, mode="from_start")
    b_spend = calculate_runway(balance=balance, msc_burn=msc_burn, spent=spent, mode="from_current")
    b_obligated = calculate_runway(balance=balance, msc_burn=msc_burn, spent=spent, obligated=zaplanowane, mode="from_obligated")

    print(f"""🔮 Runway (3 scenariusze):
  Od salda startowego:        {b_start} mies
  Od salda po wydatkach:      {b_spend} mies
  Od salda po zobowiązaniach: {b_obligated} mies""")


if __name__ == "__main__":
    print_report(balance=saldo, transactions=transakcje, planned=planowane)