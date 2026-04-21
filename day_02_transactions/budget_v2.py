saldo: float = 3311.0

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

line = "=" * 40
line_thin = "-" * 40
kategorie_suma: dict = {}
plany_suma: dict = {}

print(f"""{line}
💰 BUDGET v2 — breakdown
{line}
Saldo startowe: {saldo:.2f} zł\n
📋 Transakcje ({len(transakcje)}):""")

for i, item in enumerate(transakcje, start=1):
    kategorie_suma[item["kategoria"]] = kategorie_suma.get(item["kategoria"], 0.0) + item["kwota"]
    transaction = f"{i:>3}. {item['data']:>3} | {item['sklep']:<15} | {item['kwota']:>7.2f} zł | {item['kategoria']}"
    print(transaction)

wydane = float(f"{sum(kategorie_suma.values())}")
saldo_po = saldo - wydane

print(f"""{line_thin}
📊 Podsumowanie kategorii:
  {f"jedzenie":<10} : {kategorie_suma.get("jedzenie", 0.0):>7.2f} zł
  {f"styl":<10} : {kategorie_suma.get("styl", 0.0):>7.2f} zł 
  {f"zdrowie":<10} : {kategorie_suma.get("zdrowie", 0.0):>7.2f} zł\n
💰 Saldo po wydatkach: {saldo_po:.2f} zł
{line_thin}""")

for item in planowane:
    plany_suma[item["opis"]] = plany_suma.get(item["opis"], 0.0) + item["kwota"]

zaplanowane = float(f"{sum(plany_suma.values())}")

print(f"🎯 Zobowiązania ({zaplanowane:.2f} zł):")

for i, item in enumerate(planowane, start=1):
    plany_suma[item["opis"]] = plany_suma.get(item["opis"], 0.0) + item["kwota"]
    planned = f"- {item['opis']:<17} | {item['kwota']:>10.2f} zł | do {item['deadline']}"
    print(planned)

dni_danych = 3
wydano = wydane + zaplanowane
avg = wydano / dni_danych
msc_burn = avg * 30

runway_miesiace = 0

while saldo > 0:
    saldo -= msc_burn
    runway_miesiace += 1

print(f"""
💰 Saldo po zobowiązaniach: {saldo_po - zaplanowane:.2f} zł
{line_thin}
💸 Łącznie wydane:  {wydano:.2f} zł

🔮 Prognoza runway (avg {dni_danych} dni):
Dzienna średnia: {avg:.2f} zł
Miesięczna est:  {msc_burn:.2f} zł
Runway:          ~{runway_miesiace} miesięcy ⚠️
{line_thin}""")