from collections import OrderedDict

from cloud_scheduler.services import get_job_status
from core.routers import CustomAPIRoute
from rest_framework import mixins
from rest_framework import status as http_status
from rest_framework import viewsets
from rest_framework.response import Response


class CronJobStatusViewset(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    custom_api_routes = [
        CustomAPIRoute(
            url="job/status",
            url_args=OrderedDict(),
            url_name="job-status",
            methods=["create"],
        ),
    ]

    def create(self, request, *args, **kwargs):
        """
        Description: Used for getting the status
                     of a google cloud scheduler job

        URL Args: - None

        URL Kwargs: - None

        Request Data: None

        Returns: TODO
        """

        status = get_job_status(name=request.data["name"])

        return Response(
            data={"status": status},
            status=http_status.HTTP_200_OK,
        )
