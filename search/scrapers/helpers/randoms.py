import time
from random import randint, choice
from utilities.logger import logger


def random_sleep_small():
    """Custom sleep function that sleeps from 1 to 3 seconds"""

    value = randint(1, 3)
    logger.debug(f"random_sleep_small for {value} seconds")
    return time.sleep(value)


def random_sleep_medium():
    """Custom sleep function that sleeps from 3 to 6 seconds"""

    value = randint(3, 6)
    logger.debug(f"random_sleep_small for {value} seconds")
    return time.sleep(value)


def random_sleep_long():
    """Custom sleep function that sleeps from 6 to 8 seconds"""

    value = randint(6, 8)
    logger.debug(f"random_sleep_mediuml for {value} seconds")
    return time.sleep(value)


def random_sleep_deep():
    """Custom sleep function that sleeps from 15 to 20 seconds"""

    value = randint(15, 20)
    logger.debug(f"random_sleep_large for {value} seconds")
    return time.sleep(value)


def get_random_user_agent(user_agent_list):
    """Return random User-Agent"""
    agent = choice(user_agent_list)
    return agent
