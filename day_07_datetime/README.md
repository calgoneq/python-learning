# Day 07: datetime, Sortowanie i Filtrowanie 📅

Siódmy dzień projektu — dodanie obsługi dat, sortowania i filtrowania transakcji oraz rozszerzenie CLI o zakres dat.

## 🎯 Co tu zrobiono?
- Stworzono nowy moduł `filters.py` odpowiedzialny za operacje na datach.
- Zaimplementowano funkcje: `parse_date`, `sort_transaction_by_date` oraz `filter_by_date_range`.
- Rozszerzono komendę `report` o flagi `--od` i `--do` (format `YYYY-MM-DD`).
- Dodano walidację dat w CLI z czytelnymi komunikatami błędów.
- Napisano testy jednostkowe (`test_filters.py`) oraz rozszerzono testy CLI (`test_cli.py`).
- Zachowano pełną kompatybilność wsteczną (brak flag = wszystkie transakcje posortowane).

## 🧠 Kluczowe wnioski i techniki
* **`datetime.date` vs `datetime.datetime`:** Używamy `date` ponieważ pracujemy tylko z datami (bez godziny).
* **`strptime`:** Konwersja string → `date` (`"%Y-%m-%d"`).
* **`sorted()` z `key=lambda`:** Zaawansowane sortowanie z użyciem tupla `(priorytet, wartość)` — transakcje bez daty trafiają na koniec.
* **Graceful filtering:** Niepoprawna data w transakcji = pominięcie (nie crash programu).
* **`None` jako brak limitu:** Eleganckie obsługiwanie opcjonalnych granic zakresu dat.
* **Modularność:** Logika dat wydzielona do osobnego modułu `filters.py` (Single Responsibility Principle).
* **CLI Extension:** Walidacja argumentów w `main()` przed wywołaniem handlera.

## 🚀 Uruchomienie

```bash
# Wszystkie transakcje (posortowane po dacie)
python budget.py report

# Transakcje z zakresu
python budget.py report --od 2026-04-01 --do 2026-05-31

# Tylko od określonej daty
python budget.py report --od 2026-05-01