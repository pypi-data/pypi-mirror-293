import tempfile
import shutil
import logging
import json
from termcolor import colored
import os  # Импортируем библиотеку os для использования функции os.path.abspath
from .helpers import *
from .chat import chat_completion_request
from .scan import scan
from .git_helpers import apply_changes
from .config_loader import role_system_content, role_user_content

def get_current_conversation_number() -> int:
    try:
        with open("conversation_number.json", "r") as file:
            data = json.load(file)
            conversation_number = data.get("conversation_number", 0) + 1
    except FileNotFoundError:
        conversation_number = 1

    with open("conversation_number.json", "w") as file:
        json.dump({"conversation_number": conversation_number}, file)

    return conversation_number

def conversation(need_scan: bool, root_folder: str) -> None:
    if need_scan:
        scan_result = scan(root_folder)
        size_kb = get_string_size_kb(scan_result)
        logging.info(f"Сканирование завершено. Размер в килобайтах: {size_kb:.2f} KB.")
        # input(colored("Продолжаем?", "green"))

    try:
        temp_dir = tempfile.mkdtemp()
        messages = []

        if role_system_content:
            messages.append({"role": "system", "content": role_system_content})
            print(colored(role_system_content, "green"))
        if need_scan:
            messages.append({"role": "system", "content": f"Работа ведется над проектом: {scan_result}."})
            print(colored(f"Работа ведется над проектом: {os.path.abspath(root_folder)}", "green"))
        # if role_user_content:
        #     messages.append({"role": "user", "content": role_user_content})
        #     print(colored(role_user_content, "green"))

        # print("\nВыберите один из 4 вариантов:")
        # print("1. Оптимизация")
        # print("2. Документация")
        # print("3. Выполнение требований из папки 'Требования'")
        # print("4. Ввести свой вариант")

        # choice = input(colored("Ваш выбор (нажмите Enter для продолжения): ", "green")).strip()
        role_user_content = input(colored("Запрос: ", "blue"))
        messages.append({"role": "user", "content": role_user_content})

        # if choice == '1':
        #     content = '{"action": "optimization"}'
        # elif choice == '2':
        #     content = '{"action": "documentation"}'
        # elif choice == '3':
        #     content = '{"action": "requirements"}'
        # elif choice == '4':
        #     content = input(colored("Введите свой вариант: ", "green"))
        # else:
        #     logging.warning("Неизвестный выбор, запрос будет отправлен с пустым контентом.")
        #     content = ""

        # Остальная часть функции, как была ранее
        while True:
            chat_response = chat_completion_request(messages)
            assistant_message = chat_response.choices[0].message
            messages.append(assistant_message)

            md_file_path = save_response_to_file(assistant_message.content, temp_dir)
            display_markdown_in_browser(md_file_path)

            print("\nВыберите действие после ответа:")
            print("1. Применить изменения к коду")
            print("Все остальное будет воспринято как чат")

            try:
                choice = input(colored("Ваш выбор (нажмите Enter для продолжения): ", "green"))
            except:
                logging.info("Закончили")
            if choice == "1":
                apply_changes(root_folder, chat_response.id[:17], assistant_message.content)
                content = input(colored("вопрос: ", "green"))
            else:
                content = choice
            message = {"role": "user", "content": content}
            pretty_print_message(message)
            messages.append(message)
    except KeyboardInterrupt:
        logging.info("Закончили")
    finally:
        shutil.rmtree(temp_dir)
        logging.info("Сессия завершена")