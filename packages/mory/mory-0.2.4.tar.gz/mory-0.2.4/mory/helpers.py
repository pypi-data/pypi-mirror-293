import os
import sys
import webbrowser
import markdown
import logging
import subprocess
from termcolor import colored

def is_development_mode() -> bool:
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    return os.path.isfile(os.path.join(parent_dir, 'setup.py'))

def check_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logging.error("Ошибка: Переменная окружения OPENAI_API_KEY не установлена.")
        exit(1)
    return api_key

def get_string_size_kb(string: str) -> float:
    size_bytes = sys.getsizeof(string)
    size_kb = size_bytes / 1024
    return size_kb

def pretty_print_message(message: dict) -> None:
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "function": "magenta",
    }

    if not isinstance(message, dict):
        message = {"role": message.role, "content": message.content}

    role = message.get('role')
    if role not in role_to_color:
        logging.warning("Неизвестная роль или отсутствует информация о роли.")
        return

    formatted_message = {
        "system": lambda m: f"system: {m['content']}",
        "user": lambda m: f"user: {m['content']}",
        "assistant": lambda m: f"assistant: {m.get('function_call', m['content'])}",
        "function": lambda m: f"function ({m['name']}): {m['content']}"
    }

    colored_message = colored(formatted_message.get(role, lambda x: "")(message), role_to_color[role])
    print(colored_message)

def save_response_to_file(response: str, temp_dir: str) -> str:
    count = len(os.listdir(temp_dir)) + 1
    file_path = os.path.join(temp_dir, f"response_{count}.md")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(response)
    logging.info(f"Ответ сохранен в {temp_dir}")
    return file_path

def display_markdown_in_browser(md_file_path: str) -> None:
    with open(md_file_path, 'r', encoding='utf-8') as file:
        html_content = markdown.markdown(file.read(), extensions=['extra', 'smarty', 'toc', 'codehilite'])

    temp_html_path = md_file_path.replace('.md', '.html')
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Markdown Preview</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/4.0.0/github-markdown.min.css">
        <style>
            body {{
                box-sizing: border-box;
                min-width: 200px;
                max-width: 980px;
                margin: 0 auto;
                padding: 45px;
            }}
            .markdown-body {{
                box-sizing: border-box;
                min-width: 200px;
                max-width: 980px;
                margin: 0 auto;
                padding: 45px;
            }}
        </style>
    </head>
    <body>
        <article class="markdown-body">
            {html_content}
        </article>
    </body>
    </html>
    """
    with open(temp_html_path, 'w', encoding='utf-8') as file:
        file.write(html_template)

    webbrowser.open('file://' + os.path.realpath(temp_html_path))

def create_new_branch(branch_name: str) -> None:
    try:
        subprocess.run(["git", "checkout", "-b", branch_name], check=True)
        logging.info(f"Создана новая ветка: {branch_name}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Ошибка при создании новой ветки: {e}")

def apply_patch(patch_content: str) -> None:
    try:
        process = subprocess.run(["patch", "-p1"], input=patch_content.encode(), text=True)
        if process.returncode == 0:
            logging.info("Патч успешно применен")
        else:
            logging.error("Ошибка при применении патча")
    except Exception as e:
        logging.error(f"Ошибка при применении патча: {e}")

def parse_and_apply_changes(root_folder: str, assistant_message: str) -> None:
    changes = assistant_message.split('\n\n')
    for change in changes:
        if change.strip():
            file_name, file_content = change.split('\n', 1)
            file_path = os.path.join(root_folder, file_name.strip())
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(file_content.strip())
            logging.info(f"Изменен файл: {file_path}")
