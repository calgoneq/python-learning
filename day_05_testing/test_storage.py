import json

import pytest
from storage import save_json, load_json, append_transaction, delete_transaction, backup_json

def test_save_json_saves_list_load_json_reads_list(tmp_path):
    file = tmp_path / "test.json"
    data = [{"test_data": "test_data_1"}, {"test_data": "test_data_2"}]

    save_json(data, file)
    result = load_json(file)

    assert result == data

def test_load_json_not_existing_file_returns_empty_list(tmp_path):
    file = tmp_path / "nie_istnieje.json"
    
    result = load_json(file)

    assert result == []

def test_load_json_empty_json_returns_empty_list(tmp_path):
    file = (tmp_path / "bad.json")
    file.write_text("to nie jest JSON", encoding="utf-8")

    result = load_json(file)

    assert result == []

def test_append_transaction_adds_entry(tmp_path):
    file = tmp_path / "temp_data.json"

    data = [{
        "data": "2026-04-19",
        "sklep": "Żabka",
        "kwota": 12.0,
        "kategoria": "jedzenie"
    },
    {
        "data": "2026-04-20",
        "sklep": "Lidl",
        "kwota": 134.2,
        "kategoria": "jedzenie"
    }]

    new_entry = {"data": "2026-04-20",
        "sklep": "Lidl",
        "kwota": 134.2,
        "kategoria": "jedzenie"}

    save_json(data, file)
    append_transaction(transaction=new_entry, path=file)

    result = load_json(file)

    assert result[-1] == new_entry

def test_append_transaction_not_existing_file_creates_new_file_with_one_entry(tmp_path):
    file = tmp_path / "not_existing.json"

    new_entry = {"data": "2026-04-20",
        "sklep": "Lidl",
        "kwota": 134.2,
        "kategoria": "jedzenie"}

    append_transaction(path=file, transaction=new_entry)
    result = load_json(file)

    assert result[-1] == new_entry

def test_delete_transaction_removes_existing_entry(tmp_path):
    file = tmp_path / "temp_data.json"

    data = [{
        "data": "2026-04-19",
        "sklep": "Żabka",
        "kwota": 12.0,
        "kategoria": "jedzenie"
    },
    {
        "data": "2026-04-20",
        "sklep": "REMOVED",
        "kwota": 134.2,
        "kategoria": "to_remove"
    },
    {
        "data": "2026-04-20",
        "sklep": "Lidl",
        "kwota": 134.2,
        "kategoria": "jedzenie"
    }]

    save_json(data, file)

    target = data[1]
    delete_transaction(target, file)
    result = load_json(file)
    assert target not in result
    assert len(result) == 2     

def test_delete_transaction_on_missing_entry_does_not_crash(tmp_path):
    file = tmp_path / "temp_data.json"

    data = [{
        "data": "2026-04-19",
        "sklep": "Żabka",
        "kwota": 12.0,
        "kategoria": "jedzenie"
    },
    {
        "data": "2026-04-19",
        "sklep": "Żabka",
        "kwota": 12.0,
        "kategoria": "jedzenie"
    }]

    save_json(data, file)
    delete_transaction({"does not exist"}, file)

    result = load_json(file)

    assert result == data

def test_backup_json_creates_file_in_backup_dir_and_returns_path(tmp_path):
    file = tmp_path / "source.json"
    save_json([{"test": "dane"}], file)

    temp_folder = tmp_path / "backups"
    temp_folder.mkdir(parents=True, exist_ok=True)

    result = backup_json(source=file, backup_dir=temp_folder)

    assert result.exists()
    assert result.parent == temp_folder

    backup_content = load_json(result)
    assert backup_content == [{"test": "dane"}]