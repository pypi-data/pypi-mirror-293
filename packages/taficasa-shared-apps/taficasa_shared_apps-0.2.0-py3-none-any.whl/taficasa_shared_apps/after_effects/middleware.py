from after_effects.registry import after_effect
from after_effects.tasks import create_http_task


class AfterEffectsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        while len(after_effect.queued_tasks):
            task = after_effect.queued_tasks.pop(0)
            create_http_task(
                json_payload=task["json_payload"],
                scheduled_seconds_from_now=task["scheduled_seconds_from_now"],
            )
        return response
