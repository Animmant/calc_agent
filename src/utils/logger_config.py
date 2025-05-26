import logging
import sys

def setup_logging(level=logging.INFO):
    """Sets up basic logging configuration."""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        stream=sys.stdout,
    )
    # Вимкнення занадто детальних логів від деяких бібліотек, якщо потрібно
    # logging.getLogger("httpx").setLevel(logging.WARNING)
    # logging.getLogger("httpcore").setLevel(logging.WARNING)

# Налаштовуємо логування при імпорті
setup_logging() 