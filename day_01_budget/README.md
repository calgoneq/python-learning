# Day 01: Setup & Basic Budget Calculator 🏁

Pierwszy etap projektu. Ten folder zawiera inicjalny skrypt kalkulatora budżetu, stworzony w celu opanowania podstawowych koncepcji środowiska Python.

## 🎯 Co tu zrobiono?
- Skonfigurowano środowisko wirtualne (`venv`), aby odizolować projekt od systemu.
- Zainicjowano repozytorium Git oraz utworzono plik `.gitignore`.
- Napisano skrypt `budget.py`, który na sztywno przelicza tzw. "runway" (na ile miesięcy wystarczy środków przy obecnym tempie wydatków).

## 🧠 Kluczowe wnioski i techniki
* **Type Hints (`: float`):** Użyto w celach dobrej praktyki pisania kodu.
* **F-Strings:** Ułatwił pisanie raportu finansowego dzięki możliwości dynamicznego przypisywania zmiennych oraz formatowatowanie danych liczbowych.
* **Moduł `datetime`:** Użyto klasy datetime do pobrania aktualnego czasu systemowego oraz dyrektyw formatujących (%B dla pełnej nazwy miesiąca i %Y dla roku) w celu automatycznego generowania nagłówka raportu.

## 🚀 Uruchomienie
```bash
python budget.py
```