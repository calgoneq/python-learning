# Day 08: Logging + Custom Exceptions 🪵

Ósmy dzień projektu — profesjonalizacja obsługi błędów i zastąpienie `print()` nowoczesnym systemem logowania.

## 🎯 Co tu zrobiono?
- Stworzono moduł `exceptions.py` z hierarchią własnych wyjątków (`BudgetError` → `StorageError` → `FileCorruptedError` itp.).
- Zastąpiono wszystkie `print("ERROR: ...")` w `storage.py` wywołaniami `logging`.
- Skonfigurowano `logging.basicConfig` w punkcie wejścia aplikacji (`budget.py`).
- Zmieniono zachowanie `load_json()` — uszkodzony plik JSON teraz rzuca `FileCorruptedError` zamiast cicho zwracać pustą listę.
- Dodano obsługę nowych wyjątków w handlerach CLI.
- Utworzono plik `config.py` do przechowywania stałych projektu.
- Zaktualizowano testy (`test_storage.py` i `test_cli.py`).

## 🧠 Kluczowe wnioski i techniki
* **`logging` zamiast `print()`:** Poziomy (`WARNING`, `ERROR`), formatowanie, łatwe włączanie/wyłączanie, separacja outputu programu od logów.
* **`getLogger(__name__)`:** Standardowa konwencja — logger dziedziczy nazwę modułu.
* **Hierarchia wyjątków:** `BudgetError` → `StorageError` → `FileCorruptedError` — pozwala na precyzyjną i ogólną obsługę błędów.
* **`raise X from e`:** Zachowanie oryginalnego tracebacku przy ponownym rzucaniu wyjątku.
* **Separacja konfiguracji:** `config.py` — stałe projektu w jednym miejscu.
* **Fail fast:** Uszkodzony plik JSON = jawny błąd, a nie ciche kontynuowanie z pustymi danymi.

## 🚀 Uruchomienie

```bash
# Normalne działanie
python budget.py report