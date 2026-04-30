import pytest
from budget import sum_by_category, total_amount, calculate_runway, format_transaction_line

def test_sum_by_category_empty_list_returns_empty_dict():
    empty_list: list = []
   
    result = sum_by_category(empty_list)

    assert result == {} 

def test_sum_by_category_one_transaction_returns_dict_with_one_entry():
    one_record: list[dict] = [{
    "data": "2026-04-19",
    "sklep": "Biedronka",
    "kwota": 87.5,
    "kategoria": "jedzenie"
    }]

    result = sum_by_category(one_record)

    assert result == {"jedzenie": 87.5}

def test_sum_by_category_sum_in_category_returns_dict_with_summed_categories():
    data: list[dict] = [{
        "data": "2026-04-19",
        "sklep": "H&M",
        "kwota": 87.5,
        "kategoria": "styl"
    },
    {
        "data": "2026-04-19",
        "sklep": "Żabka",
        "kwota": 12.0,
        "kategoria": "jedzenie"
    },
    {
        "data": "2026-04-19",
        "sklep": "H&M",
        "kwota": 87.5,
        "kategoria": "styl"
    },
    {
        "data": "2026-04-20",
        "sklep": "Lidl",
        "kwota": 134.2,
        "kategoria": "jedzenie"
    }]

    result = sum_by_category(data)

    assert result == {"jedzenie": 146.2, "styl": 175}

def test_sum_by_category_transaction_without_key_goes_to_empty_category():
    one_record: list[dict] = [{
    "data": "2026-04-19",
    "sklep": "Biedronka",
    "kwota": 87.5,
    }]

    result = sum_by_category(one_record)

    assert result == {"BRAK": 87.5}

def test_total_amount_for_empty_list_returns_zero():
    empty_list: list = []

    result = total_amount(empty_list)

    assert result == 0

def test_total_amount_for_list_and_default_key_kwota():
    default_list_dict: list[dict] = [{"kwota": 10.0}, {"kwota": 10.0}, {"kwota": 10.0}]

    result = total_amount(default_list_dict)

    assert result == 30.0

def test_total_amount_with_different_key():
    default_list_dict: list[dict] = [{"deadline": "test"}, {"deadline": "test"}, {"deadline": "test"}]

    with pytest.raises(TypeError):
        total_amount(default_list_dict, key="deadline")

@pytest.mark.parametrize("balance, monthly_burn, expected", [
    (1000, 100, 10),
    (1000, 1000, 1),
    (500, 100, 5),
    (0, 100, 0),
    (99, 100, 1),
])

def test_calculate_runway_happy_path(balance, monthly_burn, expected):
    assert calculate_runway(balance, monthly_burn) == expected

@pytest.mark.parametrize("balance, monthly_burn, expected", [
    (100, 0, ValueError)
])

def test_calculate_runway_edge_case_month_equals_zero(balance, monthly_burn, expected):
    with pytest.raises(expected):
        calculate_runway(balance, monthly_burn)

def test_format_transaction_line_returns_correct_formating_string():
    one_record: dict = {
    "data": "2026-04-19",
    "sklep": "Biedronka",
    "kwota": 87.5,
    "kategoria": "jedzenie"
    }

    result = format_transaction_line(t=one_record, index=1)

    assert one_record["data"] in result
    assert one_record["sklep"] in result
    assert f"{one_record['kwota']:.2f}" in result
    assert one_record["kategoria"] in result