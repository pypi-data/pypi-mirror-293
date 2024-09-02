import logging
from typing import Optional

log = logging.getLogger(__file__)


def catch(
        on_fail: Optional[str] = None,
        on_success: Optional[str] = None,
):
    def decorator(fun):
        # noinspection PyBroadException
        def wrapper(*args, **kwargs):
            var_names = fun.__code__.co_varnames[:len(args)]
            variables = dict(zip(var_names, args))
            variables.update(kwargs)
            try:
                result = fun(*args, **kwargs)
                if on_success:
                    variables.update({"return": result})
                    success_msg = on_success.format(**variables)
                    log.info(success_msg)
                return result
            except Exception as e:
                error_msg = on_fail
                if not error_msg:
                    error_msg = f"Error executing function {fun.__name__}"
                log.exception(error_msg + f"\nCaused by:\n{e}")
                return None

        return wrapper

    return decorator
