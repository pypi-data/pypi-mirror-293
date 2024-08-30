import os
import fnmatch
import logging
from .config_loader import load_config
from .helpers import is_development_mode

logger = logging.getLogger(__name__)

config, _ = load_config()
text_extensions = set(config['text_extensions'])

def get_ignore_patterns_paths(root_folder: str) -> list:
    ignore_pattern_files = config['ignore_pattern_files']
    ignore_files_paths = []

    for file in ignore_pattern_files:
        expanded_path = os.path.expanduser(file)
        root_path = os.path.join(root_folder, file)

        if os.path.exists(root_path):
            ignore_files_paths.append(root_path)
        elif os.path.exists(expanded_path):
            ignore_files_paths.append(expanded_path)

    if is_development_mode():
        dev_ignore_path = os.path.join(os.getcwd(), 'templates', '.gptignore')
        ignore_files_paths.append(dev_ignore_path)

    return ignore_files_paths

def read_ignore_file(ignore_files_paths: list) -> list:
    ignore_patterns = []
    for path in ignore_files_paths:
        try:
            with open(path, 'r') as file:
                ignore_patterns.extend(file.read().splitlines())
        except IOError as e:
            logger.error(f"Не удалось прочитать файл {path}: {e}")
    return ignore_patterns

def should_ignore(path: str, patterns: list) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)

def is_text_file(file_path: str) -> bool:
    _, ext = os.path.splitext(file_path)
    if ext in text_extensions:
        return True

    try:
        with open(file_path, 'rb') as file:
            chunk = file.read(1024)
            if b'\0' in chunk:
                return False

            try:
                chunk.decode('utf-8', errors='ignore') ## try fix
                return True
            except (UnicodeDecodeError, IOError) as e:
                logger.error(f"Ошибка при чтении файла {file_path}: {e}")
                return False
    except IOError as e:
        logger.error(f"Файл не может быть открыт: {file_path}: {e}")
        return False

def get_text_files(root: str, ignore_patterns: list) -> list:
    text_files = []
    try:
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if not should_ignore(os.path.relpath(os.path.join(dirpath, d), root), ignore_patterns)]
            for filename in filenames:
                relpath = os.path.relpath(os.path.join(dirpath, filename), root)
                full_path = os.path.join(root, relpath)
                if not should_ignore(relpath, ignore_patterns) and is_text_file(full_path):
                    text_files.append(relpath)
    except Exception as e:
        logger.error(f"При сканировании возникла ошибка: {e}")
    return text_files

def read_file_content(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except IOError as e:
        logger.error(f"Не удалось прочитать файл {file_path}: {e}")
        return ""

def scan(root_folder: str) -> str:
    ignore_files_paths = get_ignore_patterns_paths(root_folder)
    logger.info(f"Файлы для для поиска паттернов игнорирования: {ignore_files_paths}")
    ignore_patterns = read_ignore_file(ignore_files_paths)
    logger.info(f"Паттерны для игнорирования: {ignore_patterns}")

    text_files = get_text_files(root_folder, ignore_patterns)
    logger.info(f"Файлы для сканирования: {text_files}")

    scan_result = "\n".join(
        f"{file}\n```\n{read_file_content(os.path.join(root_folder, file))}\n```"
        for file in text_files
    )

    return scan_result