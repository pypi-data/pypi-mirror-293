from collections import OrderedDict

from after_effects.registry import after_effect
from after_effects.serializers import AfterEffectSerializer
from core.routers import CustomAPIRoute
from rest_framework import mixins, permissions
from rest_framework import status as http_status
from rest_framework import viewsets
from rest_framework.response import Response


class AfterEffectRunViewset(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    A view to allow cloud tasks to run after effects jobs
    """

    serializer_class = AfterEffectSerializer
    permission_classes = [permissions.AllowAny]
    custom_api_routes = [
        CustomAPIRoute(
            url="run",
            url_args=OrderedDict(),
            url_name="after_effects_run",
            methods=["create"],
        )
    ]

    def create(self, request, *args, **kwarg):
        # Validate request data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Run task
        effect = after_effect.registered_effects[serializer.validated_data["effect"]]
        effect(
            *serializer.validated_data["effect_args"],
            **serializer.validated_data["effect_kwargs"],
        )

        return Response(status=http_status.HTTP_200_OK)
