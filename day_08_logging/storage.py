"""Storage layer — JSON file I/O."""

import json
from pathlib import Path
from datetime import datetime
import logging

from exceptions import FileCorruptedError

logger = logging.getLogger(__name__)
HERE = Path(__file__).parent

def load_json(path: Path) -> list[dict]:
    """
    Wczytuje listę dictów z pliku JSON.
    Zwraca pustą listę jeśli plik nie istnieje.
    Raises:
        json.JSONDecodeError: jeśli plik istnieje ale jest popsuty.
    """

    try: 
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data

    except FileNotFoundError:
        logger.warning("%s does not exist, new empty list created", path)
        return []

    except json.JSONDecodeError as e:
        message = f"file {path} is corrupted!"
        raise FileCorruptedError(message) from e


def save_json(data: list[dict], path: Path) -> None:
    """Zapisuje listę dictów do pliku JSON (utf-8, indent 2)."""

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def append_transaction(transaction: dict, path: Path) -> None:
    """
    Dopisuje JEDNĄ transakcję do istniejącego pliku.
    Jeśli plik nie istnieje — tworzy z jedną transakcją.
    """

    data = load_json(path)
    data.append(transaction)
    save_json(data, path)


def delete_transaction(transaction: dict, path: Path) -> None:
    """
    Usuwa JEDNĄ transakcję z istniejącego pliku.
    """

    data = load_json(path)
    try:
        data.remove(transaction)
        save_json(data, path)
    except ValueError:
        logger.warning("%s not found, skipping", transaction)


def backup_json(source: Path, backup_dir: Path) -> Path:
    """
    Kopiuje source do backup_dir/source-YYYYMMDD-HHMMSS.json.
    Zwraca ścieżkę nowego backupu.
    """

    data = load_json(source)
    timestamp = datetime.today().strftime("%Y%m%d-%H%M%S")
    if backup_dir.exists():
        backup_file = backup_dir / f"source-{timestamp}.json"
    else:
        raise FileNotFoundError("ERROR: Folder backup nie istnieje!")
    save_json(data, backup_file)
    return backup_file