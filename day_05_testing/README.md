# Day 05: Testing with pytest 🧪

Piąty dzień nauki Pythona — wprowadzenie do testów jednostkowych. Pierwszy raz piszemy automatyczne testy dla istniejącego kodu.

## 🎯 Co tu zrobiono?
- Skopiowano kod z Dnia 4 do nowego folderu `day_05_testing/`.
- Zainstalowano i skonfigurowano `pytest`.
- Napisano pełne testy jednostkowe dla warstwy logiki (`test_budget.py`) oraz warstwy przechowywania danych (`test_storage.py`).
- Zaimplementowano testy dla czystych funkcji, obsługi błędów, wyjątków oraz operacji I/O.
- Użyto `tmp_path` do bezpiecznego testowania funkcji plikowych.

## 🧠 Kluczowe wnioski i techniki
* **pytest:** Nowoczesne, czytelne i potężne narzędzie do testów jednostkowych — znacznie wygodniejsze niż wbudowany `unittest`.
* **AAA Pattern (Arrange-Act-Assert):** Struktura każdego testu — przygotowanie danych, wykonanie akcji, weryfikacja wyniku.
* **`tmp_path` fixture:** Automatycznie tworzony tymczasowy folder dla każdego testu — kluczowy przy testowaniu operacji na plikach (bezpieczeństwo danych produkcyjnych).
* **`@pytest.mark.parametrize`:** Jedna funkcja testowa, wiele przypadków testowych — idealne do testowania `calculate_runway`.
* **`pytest.raises`:** Testowanie czy funkcja prawidłowo rzuca oczekiwany wyjątek (np. `ValueError` przy `monthly_burn <= 0`).
* **Testy czystych funkcji:** Łatwość testowania funkcji bez efektów ubocznych (`sum_by_category`, `calculate_runway` itd.).
* **Nazewnictwo testów:** `test_funkcja_co_robi_spodziewany_wynik` — czytelna dokumentacja wykonywalna.

## 🚀 Uruchomienie

```bash
# Uruchomienie wszystkich testów
pytest -v

# Tylko testy budgetu
pytest test_budget.py -v

# Tylko testy storage
pytest test_storage.py -v