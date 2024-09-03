import functools
from typing import Callable, Dict, List, ParamSpec, TypeVar

from django.conf import settings

T = TypeVar("T")
P = ParamSpec("P")


def check_effect_arguments(
    args: List[str], kwargs: Dict[str, str | int | None]
) -> bool:
    allowed_types = [int, str, None]
    # Check args
    for arg in args:
        if type(arg) not in allowed_types:
            return False

    # Check kwargs
    for key, value in kwargs.items():
        if type(key) != str or type(value) not in allowed_types:
            return False

    return True


class AfterEffectRegistry:
    def __init__(self):
        self._registered_effects = {}
        self._queued_tasks = []

    @property
    def queued_tasks(self):
        return self._queued_tasks

    @property
    def registered_effects(self):
        return self._registered_effects

    def __call__(self, app_name):
        def decorator(func: Callable[P, T]) -> Callable[P, T]:
            effect_unique_name = f"{app_name}:{func.__name__}"
            self._registered_effects[effect_unique_name] = func

            @functools.wraps(func)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                # Check types before creating task
                if not check_effect_arguments(args=args, kwargs=kwargs):
                    raise ValueError(
                        "After Effect Functions can only take arguments that accept str, int or None values"
                    )

                if settings.LOCAL or settings.TESTING:
                    # Call task immediately
                    func(*args, **kwargs)
                else:
                    # Delegate to gcp task queue which will be processed in
                    # order after response is received from view
                    self._queued_tasks.append(
                        {
                            "json_payload": {
                                "effect": f"{app_name}:{func.__name__}",
                                "effect_args": args,
                                "effect_kwargs": kwargs,
                            },
                            "scheduled_seconds_from_now": 60,
                        }
                    )

            return wrapper

        return decorator

    def __get__(self, obj, objtype=None):
        return self._registered


after_effect = AfterEffectRegistry()
