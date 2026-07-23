import os
import shutil
from pathlib import Path


def _get_file_size_str(size_bytes):
    for unit in ("B", "KB", "MB", "GB"):
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def _get_zip_size(zip_path):
    try:
        return os.path.getsize(zip_path)
    except OSError:
        return 0


def move_to_trash(zip_path, trash_dir):
    zip_path = Path(zip_path)
    trash_dir = Path(trash_dir)

    if not zip_path.exists() or not zip_path.suffix.lower() == ".zip":
        return None, "Not a valid ZIP file"

    dest = trash_dir / zip_path.name

    if dest.exists():
        base = dest.stem
        ext = dest.suffix
        counter = 1
        while dest.exists():
            dest = trash_dir / f"{base}_{counter}{ext}"
            counter += 1

    try:
        shutil.move(str(zip_path), str(dest))
        return dest, None
    except (OSError, shutil.Error) as e:
        return None, str(e)


def restore_zip(entry, config):
    trash_path = Path(entry["trash_path"])
    original_path = Path(entry["original_path"])

    if not trash_path.exists():
        return False, "ZIP not found in trash"

    original_dir = original_path.parent
    if not original_dir.exists():
        try:
            original_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            return False, f"Cannot create directory: {e}"

    dest = original_path
    if dest.exists():
        base = dest.stem
        ext = dest.suffix
        counter = 1
        while dest.exists():
            dest = original_dir / f"{base}_{counter}{ext}"
            counter += 1

    try:
        shutil.move(str(trash_path), str(dest))
        config.add_ignored_zip(dest.name, original_path.parent)
        config.remove_deleted_zip_record(trash_path)
        return True, None
    except (OSError, shutil.Error) as e:
        return False, str(e)


def delete_permanently(trash_path):
    trash_path = Path(trash_path)
    if not trash_path.exists():
        return True, None

    try:
        if trash_path.is_file():
            trash_path.unlink()
        elif trash_path.is_dir():
            shutil.rmtree(trash_path)
        return True, None
    except OSError as e:
        return False, str(e)


def clean_trash(config):
    eliminated = []
    remaining = []
    for entry in list(config.deleted_zips):
        trash_path = Path(entry["trash_path"])
        if not trash_path.exists():
            config.remove_deleted_zip_record(trash_path)
            eliminated.append(entry)
        else:
            remaining.append(entry)
    return eliminated, remaining


def detect_garbage_zips(folder_path):
    folder = Path(folder_path)
    if not folder.exists() or not folder.is_dir():
        return []

    results = []
    for item in folder.iterdir():
        if item.is_file() and item.suffix.lower() == ".zip":
            expected_folder = folder / item.stem
            if expected_folder.exists() and expected_folder.is_dir():
                results.append(item)
    return results
