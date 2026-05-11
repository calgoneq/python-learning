# Day 06: CLI with argparse 🖥️

Szósty dzień projektu — przekształcenie skryptu w prawdziwe narzędzie linii poleceń z wieloma komendami.

## 🎯 Co tu zrobiono?
- Refaktoryzacja `budget.py` na nowoczesne narzędzie CLI z użyciem `argparse`.
- Wprowadzono **sub-commands**: `report`, `add`, `delete`, `backup` (i bonusowo `categories`).
- Zaimplementowano dispatch przez słownik `HANDLERS` zamiast łańcucha `if/elif`.
- Dodano walidację argumentów (np. kwota > 0).
- Napisano testy CLI (`test_cli.py`) z użyciem `monkeypatch`, `capsys` oraz fixture'ów z `yield` do backupu/restore plików.
- Zachowano wszystkie poprzednie testy jednostkowe (`test_budget.py`, `test_storage.py`).

## 🧠 Kluczowe wnioski i techniki
* **argparse:** Standardowa biblioteka do budowania profesjonalnych interfejsów CLI — automatyczna generacja `--help`, walidacja typów, sub-commands.
* **Subparsers:** Umożliwiają tworzenie wielu komend w jednym narzędziu (`python budget.py <komenda> [opcje]`).
* **Dispatch dict (`HANDLERS`):** Czysty, skalowalny sposób na routing komend — łatwy do rozbudowy o nowe funkcjonalności.
* **`monkeypatch`:** Podmiana `sys.argv` w testach, dzięki czemu możemy symulować uruchomienie z linii poleceń.
* **Fixtures z `yield`:** Setup → test → teardown (backup pliku przed testem + przywrócenie po teście).
* **Separacja warstw:** Handlery CLI są cienkie — tylko parsują argumenty i delegują do istniejących funkcji (`storage.py` + funkcje z `budget.py`).

## 🚀 Uruchomienie

```bash
# Główny raport
python budget.py report

# Dodanie transakcji
python budget.py add --sklep "Żabka" --kwota 15.50 --kategoria jedzenie

# Usunięcie transakcji
python budget.py delete --index 1

# Backup
python budget.py backup

# Pomoc
python budget.py --help
python budget.py add --help