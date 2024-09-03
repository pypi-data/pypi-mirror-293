from typing import Optional

import google.auth
from cloud_scheduler.status import convert_job_state, convert_status_code
from google.cloud import scheduler_v1


def create_scheduler_job(
    url: str,
    method: str,
    job_name: str,
    schedule: str,
    token: str,
    description: Optional[str] = None,
    data: Optional[bytes] = None,
) -> scheduler_v1.Job:
    """
    This function creates a cloud scheduler job on google cloud.

    Args:
    - url (str): The full URI path that the request will be sent to. This string must begin with either "http://" or "https://".
    - method (str): The HTTP method to be used for the request ('GET', 'POST', 'PUT', 'DELETE', etc.).
    - job_name (str): The name of the Cloud Scheduler job.
    - schedule (str): The cron schedule for the job in the form 'MINUTE HOUR DAY_OF_MONTH MONTH DAY_OF_WEEK' e.g (* * * * *).
    - token (str): The Authorization token for the requested endpoint
    - description (Optional[str]): Description of the job (default is None).
    - data (Optional[bytes]]): The data to be sent in the request body (default is None).

    Returns:
    - response (dict): The response from creating the Cloud Scheduler job.

    Documentation:
    - https://cloud.google.com/python/docs/reference/cloudscheduler/latest/google.cloud.scheduler_v1.services.cloud_scheduler.CloudSchedulerClient

    """
    credentials, project_id = google.auth.default()

    # Create a client
    client = scheduler_v1.CloudSchedulerClient(credentials=credentials)

    location = "europe-west1"
    parent = f"projects/{project_id}/locations/{location}"

    # Get HttpMethod enum value
    http_method = getattr(scheduler_v1.HttpMethod, method.upper())

    http_target = {
        "uri": url,
        "http_method": http_method,
        "headers": {"Authorization": f"Token {token}"},
    }

    # Add data to http_target body if request method is post or put
    if (
        http_method in (scheduler_v1.HttpMethod.POST, scheduler_v1.HttpMethod.PUT)
        and data
    ):
        http_target["body"] = data

    job = {
        "name": f"{parent}/jobs/{job_name}",
        "description": description,
        "http_target": http_target,
        "schedule": schedule,
        "time_zone": "UTC",
    }

    response = client.create_job(parent=parent, job=job)

    return response


def get_job_status(name: str):
    """
    This function returns the status of a google cloud scheduler job
    """

    credentials, _ = google.auth.default()

    # Create a client
    client = scheduler_v1.CloudSchedulerClient(credentials=credentials)

    # Initialize request
    request = scheduler_v1.GetJobRequest(name=name)

    # Make the request
    response = client.get_job(request=request)

    # return the job state is status is not present
    if not response.status.code:
        return convert_job_state(response.state)

    return convert_status_code(response.status.code)
