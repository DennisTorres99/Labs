import time
from collections.abc import Callable
from functools import wraps


def retry(
    *,
    attempts: int = 3,
    delay: float = 0.5,
    backoff: float = 2.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable:

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as error:
                    if attempt == attempts:
                        raise
                    print(
                        f"[retry] Intento {attempt} falló: {error}. "
                        f"Reintentando en {current_delay:.2f}s..."
                    )
                    time.sleep(current_delay)
                    current_delay *= backoff

        return wrapper

    return decorator
