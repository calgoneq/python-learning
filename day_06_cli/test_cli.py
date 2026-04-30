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

    assert "TEST" in dane[-1]

def test_cmd_add_adds_transaction_to_file(backup_transaction_file, monkeypatch):
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
    
    with pytest.raises(SystemExit):
        main()