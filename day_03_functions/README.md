# Day 03: Functions & Modular Design 🧩

Drugi etap refaktoryzacji. Przejście z "kodowania skryptowego" na budowanie modułowych, wielokrotnego użytku komponentów.

## 🎯 Co tu zrobiono?
- Zaimplementowano architekturę opartą na **czystych funkcjach** (pure functions).
- Wprowadzono **docstringi** (zgodnie z PEP 257) oraz **type hints** dla każdej funkcji.
- Rozdzielono logikę obliczeniową od warstwy prezentacji (`print_report` jako jedyny punkt wyjścia).

## 🧠 Kluczowe wnioski i techniki
* **Pure Functions:** Oddzielenie logiki od I/O pozwala na testowanie jednostkowe bez konieczności przechwytywania strumienia wyjściowego.
* **Type Hints & Docstrings:** Służą jako żywa dokumentacja, co drastycznie obniża czas onboardingu nowego programisty w projekt.
* **`if __name__ == "__main__":`**: Mechanizm ten umożliwia importowanie poszczególnych funkcji do innych modułów lub testów bez automatycznego uruchamiania całego programu.

## 🚀 Uruchomienie
```bash
python budget_v3.py