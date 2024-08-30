import logging
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
from .config_loader import gpt_model

client = OpenAI()
logger = logging.getLogger(__name__)

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages: list, tools: list = None, tool_choice: str = None) -> dict:
    try:
        logger.info("Отправка запроса...")
        response = client.chat.completions.create(
            model=gpt_model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        logger.info("Запрос выполнен.")
        return response
    except Exception as e:
        logger.error(f"Ошибка при генерации ответа: {e}")
        raise