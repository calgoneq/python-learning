import pytest
import shutil

from budget import main, TRANSACTIONS_FILE, HERE
from storage import load_json

def test_cmd_report_prints_raport_with_saldo(capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", ["budget.py", "report"])
    main()
    captured = capsys.readouterr()
    assert "BUDGET v4" in captured.out
    assert "Saldo startowe" in captured.out

@pytest.fixture
def backup_transaction_file():
    backup_path = TRANSACTIONS_FILE.with_suffix(".json.bak")
    
    if TRANSACTIONS_FILE.exists():
        shutil.copy(TRANSACTIONS_FILE, backup_path)
    
    yield

    if backup_path.exists():
        shutil.move(backup_path, TRANSACTIONS_FILE)

@pytest.fixture
def backup_backup_dir():
    original_folder = HERE / "backup_dir"
    backup_folder = HERE / "backup_dir_original.bak"
    
    if original_folder.exists():
        shutil.copytree(original_folder, backup_folder, dirs_exist_ok=True)

    yield

    if original_folder.exists():
        shutil.rmtree(original_folder)

    if backup_folder.exists():
        shutil.move(backup_folder, original_folder)

def test_cmd_add_adds_transaction_to_file(backup_transaction_file, monkeypatch):
    monkeypatch.setattr("sys.argv", ["budget.py", "add", "--sklep", "TEST", "--kwota", "1.0", "--kategoria", "test"])
    main()
    dane = load_json(TRANSACTIONS_FILE)

    assert "TEST" in dane[-1]['sklep']

def test_cmd_add_with_negative_amount_exits(backup_transaction_file, monkeypatch):
    with pytest.raises(SystemExit):
        monkeypatch.setattr("sys.argv", ["budget.py", "add", "--sklep", "TEST", "--kwota", "-10.0", "--kategoria", "test"])
        main()  

def test_cmd_del_with_index_1_removes_first_transaction(backup_transaction_file, monkeypatch):
    data_before = load_json(TRANSACTIONS_FILE)
    monkeypatch.setattr("sys.argv", ["budget.py", "delete", "--index", "1"])
    main()
    data_after = load_json(TRANSACTIONS_FILE)
    
    assert len(data_before) > len(data_after)
    assert data_before[0] != data_after[0]

def test_cmd_del_with_index_out_of_range_returns_error(backup_transaction_file, monkeypatch):
    with pytest.raises(SystemExit):
        monkeypatch.setattr("sys.argv", ["budget.py", "delete", "--index", "999"])
        main()

def test_cmd_backup_creates_new_file_in_default_dir(backup_backup_dir, monkeypatch):
    folder = HERE / "backup_dir"
    
    amount_before: int = 0
    amount_after: int = 0

    if folder.exists():
        amount_before += len([f for f in folder.iterdir() if f.is_file()])

    monkeypatch.setattr("sys.argv", ["budget.py", "backup"])
    main()

    if folder.exists():
        amount_after += len([f for f in folder.iterdir() if f.is_file()])

    assert amount_before < amount_after

def test_parameter_help_prints_usage_and_ends_with_exit_code_0(capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", ["budget.py", "--help"])
   
    with pytest.raises(SystemExit) as e:
        main()

    assert e.value.code == 0
    
    captured = capsys.readouterr()
    assert "usage: " in captured.out

def test_no_command_returns_error_and_exits(monkeypatch):
    monkeypatch.setattr("sys.argv", ["budget.py"])
    
    with pytest.raises(SystemExit) as e:
        main()
        
    assert e.value.code != 0

def test_cmd_report_for_range_start_of_may_to_end_of_may_returns_only_transactions_of_the_month(capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", ["budget.py", "report", "--od", "2026-05-01", "--do", "2026-05-31"])
    main()
    captured = capsys.readouterr()
    for i in range(0, 13):
        if i == 5:
            continue
        assert f"-0{i}-" not in captured.out
    
    assert "-05-" in captured.out

def test_cmd_report_with_no_flags_returns_sorted_transactions(capsys, monkeypatch):
    '''dla listy transakcji == expected'''

    expected: str = """Transakcje (12):
  1. 2026-04-19 | Biedronka  |   87.50 zł | jedzenie
  2. 2026-04-19 | Żabka      |   12.00 zł | jedzenie
  3. 2026-04-20 | Lidl       |  134.20 zł | jedzenie
  4. 2026-04-20 | Fryzjer    |   60.00 zł | styl
  5. 2026-04-20 | Kreatyna   |   45.00 zł | zdrowie
  6. 2026-04-21 | Kebab      |   22.00 zł | jedzenie
  7. 2026-05-19 | Biedronka  |   87.50 zł | jedzenie
  8. 2026-05-19 | Żabka      |   12.00 zł | jedzenie
  9. 2026-05-20 | Lidl       |  134.20 zł | jedzenie
 10. 2026-05-21 | Kebab      |   22.00 zł | jedzenie
 11. 2026-06-20 | Fryzjer    |   60.00 zł | styl
 12. 2026-07-20 | Kreatyna   |   45.00 zł | zdrowie"""

    monkeypatch.setattr("sys.argv", ["budget.py", "report"])
    main()
    captured = capsys.readouterr()

    assert expected in captured.out

def test_cmd_report_incorrect_data_raises_system_exit(monkeypatch):
    monkeypatch.setattr("sys.argv", ["budget.py", "report", "--od", "nieprawidłowaData"])

    with pytest.raises(SystemExit) as e:
        main()
        
    assert e.value.code != 0

def test_cmd_report_when_transactions_file_is_corrupted_raises_system_exit(monkeypatch, tmp_path):
    file = tmp_path / "broken.json"
    file.write_text("to nie jest JSON", encoding="utf-8")
    monkeypatch.setattr("budget.TRANSACTIONS_FILE", str(file))
    monkeypatch.setattr("sys.argv", ["budget.py", "report"])
    
    with pytest.raises(SystemExit) as e:
        main()
        
    assert e.value.code != 0