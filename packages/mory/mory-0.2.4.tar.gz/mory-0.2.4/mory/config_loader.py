import os
import yaml
from .helpers import is_development_mode
from .version import PROGRAM_NAME

def load_config() -> dict:
    if is_development_mode():
        parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        config_dir = os.path.join(parent_dir, 'templates')
    else:
        config_dir = os.path.join(os.path.expanduser('~'), '.config', PROGRAM_NAME)

    config_path = os.path.join(config_dir, 'config.yml')
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Конфигурационный файл не найден по пути: {config_path}")

    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config, config_path

def open_config_file():
    _, config_path = load_config()

    if config_path:
        os.system(f'open "{config_path}"' if os.name == 'posix' else f'start "" "{config_path}"')
    else:
        print("Файл конфигурации не найден.")


config, config_path = load_config()

gpt_model = config['gpt_model']
role = config['role']
role_system_content = role['system']['developer']['content']
role_user_content = role['user']['content']
log_level = config['log_level']