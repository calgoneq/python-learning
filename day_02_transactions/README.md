# Day 02: Lists, Dictionaries & Loops 🔄

Etap nauki Pythona skupiony na kolekcjach danych i sterowaniu przepływem programu.

## 🎯 Co tu zrobiono?
- Zaimplementowano dynamiczną analizę budżetu na podstawie listy transakcji.
- Wdrożono grupowanie wydatków według kategorii przy użyciu słownika (`dict`).
- Obliczono "runway" finansowy (prognoza przeżycia) przy użyciu pętli `while`.

## 🧠 Kluczowe wnioski i techniki
* **Słowniki (`dict`) i `dict.get()`:** Użyłem .get() w celach zabezpieczenia programu przed KeyError wywołanym przy otrzymaniu nowego klucza.
* **Pętle `for` z `enumerate`:** Enumerate pozwoliło na dynamiczne indeksowanie transakcji.
* **Pętla `while`:** Zrozumienie ryzyka nieskończonych pętli (infinite loops) przy błędnych danych wejściowych (np. zerowy burn-rate).

## 🚀 Uruchomienie
```bash
python budget_v2.py