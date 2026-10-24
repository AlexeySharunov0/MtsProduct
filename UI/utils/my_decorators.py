import time
import logging
from functools import wraps
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

# Настройка логгирования
logger = logging.getLogger(__name__)

def retry_on_timeout(max_retries=3, retry_delay=5):
    """Декоратор для повторных попыток выполнения функции в случае таймаута."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    logger.info(f"Попытка {attempt + 1} из {max_retries} для функции {func.__name__}")
                    return func(*args, **kwargs)
                except PlaywrightTimeoutError as error:
                    logger.warning(f"Таймаут при выполнении {func.__name__}: {error}. Ожидание {retry_delay} секунд перед повторной попыткой.")
                    time.sleep(retry_delay)
            raise RuntimeError(f"Не удалось выполнить {func.__name__} после {max_retries} попыток.")
        return wrapper
    return decorator