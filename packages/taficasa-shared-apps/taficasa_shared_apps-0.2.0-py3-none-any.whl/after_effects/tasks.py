import json
import os
from typing import Dict, Optional

from django.utils import timezone
from google.cloud import tasks_v2
from google.protobuf import timestamp_pb2


def create_http_task(
    json_payload: Dict,
    scheduled_seconds_from_now: Optional[int] = None,
    task_id: Optional[str] = None,
) -> tasks_v2.Task:
    """Create an HTTP POST task with a JSON payload.
    Args:
        url: The target URL of the task.
        json_payload: The JSON payload to send.
        scheduled_seconds_from_now: Seconds from now to schedule the task for.
        task_id: ID to use for the newly created task.
        deadline_in_seconds: The deadline in seconds for task.
    Returns:
        The newly created task.
    """

    project = os.environ["GOOGLE_CLOUD_PROJECT"] or "taficasa-core-dev"
    location = "europe-west1"
    queue = "after-effects-queue"
    url = "https://taficasa-core-api-dev-scheduler-ohvkdl34jq-ew.a.run.app/"

    # Create a client.
    client = tasks_v2.CloudTasksClient()

    # Construct the task.
    task = tasks_v2.Task(
        http_request=tasks_v2.HttpRequest(
            http_method=tasks_v2.HttpMethod.POST,
            url=url,
            headers={"Content-type": "application/json"},
            body=json.dumps(json_payload).encode(),
        ),
        name=(
            client.task_path(project, location, queue, task_id)
            if task_id is not None
            else None
        ),
    )

    # Convert "seconds from now" to an absolute Protobuf Timestamp
    if scheduled_seconds_from_now is not None:
        timestamp = timestamp_pb2.Timestamp()
        timestamp.FromDatetime(
            timezone.now() + timezone.timedelta(seconds=scheduled_seconds_from_now)
        )
        task.schedule_time = timestamp

    # Use the client to send a CreateTaskRequest.
    return client.create_task(
        tasks_v2.CreateTaskRequest(
            # The queue to add the task to
            parent=client.queue_path(project, location, queue),
            # The task itself
            task=task,
        )
    )
