import os
import subprocess
import time
import logging
from .helpers import parse_and_apply_changes

def get_branch_name(conversation_number: int) -> str:
    return f"conversation_{conversation_number}"

def check_branch_exists(branch_name: str, root_folder: str) -> bool:
    try:
        result = subprocess.run(['git', 'branch', '--list', branch_name], cwd=root_folder, stdout=subprocess.PIPE)
        return branch_name in result.stdout.decode('utf-8').split('\n')
    except subprocess.CalledProcessError as e:
        logging.error(f"Ошибка при проверке существования ветки: {e}")
        return False

def switch_to_branch(branch_name: str, root_folder: str) -> None:
    try:
        subprocess.run(['git', 'checkout', branch_name], cwd=root_folder, check=True)
        logging.info(f"Переключились на ветку: {branch_name}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Ошибка при переключении на ветку: {e}")

def create_and_switch_to_branch(branch_name: str, root_folder: str) -> None:
    try:
        subprocess.run(['git', 'checkout', '-b', branch_name], cwd=root_folder, check=True)
        logging.info(f"Создана и переключились на новую ветку: {branch_name}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Ошибка при создании и переключении на новую ветку: {e}")

def apply_changes(root_folder: str, conversation_number: int, response: str) -> None:
    branch_name = get_branch_name(conversation_number)

    if check_branch_exists(branch_name, root_folder):
        switch_to_branch(branch_name, root_folder)
    else:
        create_and_switch_to_branch(branch_name, root_folder)

    if response.strip():
        parse_and_apply_changes(root_folder, response)

        try:
            subprocess.run(['git', 'add', '.'], cwd=root_folder, check=True)
            commit_message = f"conversation_{conversation_number}: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(['git', 'commit', '-m', commit_message], cwd=root_folder, check=True)
            logging.info(f"Коммит сделан с сообщением: {commit_message}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Ошибка при создании коммита: {e}")