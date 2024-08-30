import argparse
import logging
import os
from termcolor import colored
from .helpers import check_api_key
from .conversation import conversation
from .config_loader import log_level, open_config_file
from .version import PROGRAM_NAME, PROGRAM_VERSION

logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(prog=PROGRAM_NAME, description="Сканирование папки и отправка в gpt")

    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")

    # Команда 'scan'
    scan_parser = subparsers.add_parser("scan", help="Сканирование директории")
    scan_parser.add_argument("-p", "--path", type=str, help="Путь к сканируемой директории")

    # Команда 'config'
    subparsers.add_parser("config", help="Открыть файл конфигурации")

    # Версия программы
    parser.add_argument('-v', '--version', action='version', version=f"%(prog)s {PROGRAM_VERSION}")

    return parser, parser.parse_args()

def main():
    parser, args = parse_args()

    check_api_key()
    root_folder = ""
    try:
        if not args.command:
            print("Команда не распознана")
            parser.print_help()
        elif args.command == "config":
            open_config_file()
        elif args.command == "scan":
            if args.path:
                root_folder = args.path.strip()
            else:
                root_folder = input(colored("Введите путь к папке для сканирования или оставьте пустым если сканируется текущая: ", "green")).strip()

            if not root_folder:
                root_folder = os.getcwd()

            if not os.path.isdir(root_folder):
                logger.error("Ошибка: Путь не является директорией.")
                raise NotADirectoryError("Ошибка: Путь не является директорией.")

            logger.info(f"Сканируем папку: {os.path.abspath(root_folder)}")
            conversation(True, root_folder)
        else:
            parser.print_help()
    except KeyboardInterrupt:
        logger.info("\nПрограмма завершена пользователем.")

if __name__ == '__main__':
    main()