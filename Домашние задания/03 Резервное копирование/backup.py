import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
from zipfile import BadZipFile, ZIP_DEFLATED, ZipFile

MANIFEST = ".backup-manifest.json"


def digest(stream):
    checksum = hashlib.sha256()
    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
        checksum.update(chunk)
    return checksum.hexdigest()


def inventory(source):
    result = {}
    for entry in sorted(source.rglob("*")):
        if entry.is_symlink():
            raise ValueError(f"Символьная ссылка: {entry.name}")
        if entry.is_file():
            name = entry.relative_to(source).as_posix()
            if name == MANIFEST:
                raise ValueError(f"Зарезервированное имя: {name}")
            with entry.open("rb") as stream:
                result[name] = digest(stream)
        elif not entry.is_dir():
            raise ValueError(f"Неподдерживаемый файл: {entry.name}")
    return result


def verify(archive):
    names = archive.namelist()
    if len(names) != len(set(names)) or archive.testzip() is not None:
        raise ValueError("Архив повреждён")
    manifest = json.loads(archive.read(MANIFEST))
    if set(names) != set(manifest) | {MANIFEST}:
        raise ValueError("Список файлов отличается от манифеста")
    for name, expected in manifest.items():
        parts = name.split("/")
        if any(part in ("", ".", "..") for part in parts) or "\\" in name:
            raise ValueError(f"Недопустимый путь: {name}")
        with archive.open(name) as stream:
            if digest(stream) != expected:
                raise ValueError(f"Неверная контрольная сумма: {name}")
    return manifest


def create(source, target):
    source = source.resolve(strict=True)
    target = target.resolve()
    if not source.is_dir() or source in target.parents:
        raise ValueError("Архив должен находиться вне исходной папки")
    expected = inventory(source)
    with tempfile.TemporaryDirectory(dir=target.parent) as temporary:
        candidate = Path(temporary) / "backup.zip"
        with ZipFile(candidate, "w", compression=ZIP_DEFLATED) as archive:
            for name in expected:
                archive.write(source / name, name)
            archive.writestr(MANIFEST, json.dumps(expected, ensure_ascii=False))
        with ZipFile(candidate) as archive:
            verify(archive)
        if inventory(source) != expected:
            raise ValueError("Исходная папка изменилась во время копирования")
        os.link(candidate, target)
    print(f"{target.name}: {len(expected)} файлов, SHA-256 проверены")


def restore(source, target):
    if target.exists() or target.is_symlink():
        raise ValueError("Папка назначения уже существует")
    with ZipFile(source) as archive:
        expected = verify(archive)
        with tempfile.TemporaryDirectory(dir=target.parent) as temporary:
            staging = Path(temporary) / "restore"
            staging.mkdir()
            for name in expected:
                output = staging / name
                output.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(name) as stream, output.open("xb") as destination:
                    shutil.copyfileobj(stream, destination)
            if inventory(staging) != expected:
                raise ValueError("Контрольные суммы восстановленных файлов различаются")
            staging.rename(target)
    print(f"{source.name} → {target.name}: {len(expected)} файлов восстановлено")


def main():
    parser = argparse.ArgumentParser(description="Проверяемые ZIP-копии документов")
    parser.add_argument("action", choices=("create", "restore"))
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    args = parser.parse_args()
    try:
        action = create if args.action == "create" else restore
        action(args.source, args.target)
    except (OSError, ValueError, KeyError, TypeError, BadZipFile) as error:
        parser.exit(1, f"Ошибка: {error}\n")


if __name__ == "__main__":
    main()
