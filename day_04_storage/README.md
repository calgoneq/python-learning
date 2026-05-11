# Day 04: Files I/O, JSON & Modular Design 📁

Czwarty dzień projektu — przejście z hardcoded danych na prawdziwą persystencję. Wprowadzenie modularności i pracy z plikami.

## 🎯 Co tu zrobiono?
- Rozbito projekt na moduły: `budget.py` (logika + raport) oraz `storage.py` (warstwa odpowiedzialna za I/O).
- Przeniesiono wszystkie dane do plików JSON (`transactions.json`, `planned.json`).
- Zaimplementowano bezpieczne wczytywanie i zapisywanie danych z obsługą błędów.
- Dodano skrypty pomocnicze: `add_transaction.py` i `remove_transaction.py`.
- Zaimplementowano mechanizm backupu transakcji.

## 🧠 Kluczowe wnioski i techniki
* **Modularność:** Oddzielenie warstwy przechowywania danych (`storage.py`) od logiki biznesowej (`budget.py`) — lepsza organizacja i możliwość ponownego użycia kodu.
* **`pathlib.Path`:** Nowoczesne operacje na ścieżkach, użycie `Path(__file__).parent` do tworzenia względnych, niezawodnych ścieżek niezależnych od miejsca uruchomienia skryptu.
* **Context managers (`with open...`):** Bezpieczne otwieranie i automatyczne zamykanie plików.
* **Obsługa JSON:** `json.load()` / `json.dump()` z parametrami `indent=2` i `ensure_ascii=False` (zachowanie polskich znaków).
* **Error handling:** `FileNotFoundError` oraz `json.JSONDecodeError` — program gracefully obsługuje brak pliku lub jego uszkodzenie.
* **Funkcje storage:** `load_json`, `save_json`, `append_transaction`, `delete_transaction` oraz `backup_json`.

## 🚀 Uruchomienie

```bash
# Główny raport
python budget.py

# Dodanie testowej transakcji
python add_transaction.py

# Usunięcie testowej transakcji
python remove_transaction.py
```