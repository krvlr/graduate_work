import logging
from functools import wraps
from random import sample
from time import sleep

logger = logging.getLogger(__name__)


def backoff(
    start_sleep_time: float = 0.1,
    factor: int = 2,
    border_sleep_time: int = 10,
    max_count_sleep: int = 5,
):
    def wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            sleep_time = start_sleep_time
            sleep_iter = 0
            while True:
                try:
                    res = await func(*args, **kwargs)
                    return res
                except Exception as ex:
                    logger.info(
                        f"Exception in {func.__qualname__}: \n{ex}. \n"
                        f"Start sleeping for {sleep_time} seconds ({sleep_iter} iter)"
                    )
                    sleep(sleep_time)

                    sleep_iter += 1
                    sleep_time *= factor

                    if sleep_time >= border_sleep_time:
                        sleep_time = border_sleep_time

                    if sleep_iter >= max_count_sleep:
                        raise ex

        return inner

    return wrapper
