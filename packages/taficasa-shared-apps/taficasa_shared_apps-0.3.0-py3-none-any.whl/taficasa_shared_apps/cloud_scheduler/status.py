"""
This module defines job states and Job status
it provides a function to convert numeric state/status codes to their corresponding names
"""


class JobStatus:
    OK = 0
    CANCELLED = 1
    UNKNOWN = 2
    INVALID_ARGUMENT = 3
    DEADLINE_EXCEEDED = 4
    NOT_FOUND = 5
    ALREADY_EXISTS = 6
    PERMISSION_DENIED = 7
    RESOURCE_EXHAUSTED = 8
    FAILED_PRECONDITION = 9
    ABORTED = 10
    OUT_OF_RANGE = 11
    UNIMPLEMENTED = 12
    INTERNAL = 13
    UNAVAILABLE = 14
    DATA_LOSS = 15
    UNAUTHENTICATED = 16


def convert_status_code(status_code):
    status_mapping = {
        JobStatus.OK: "OK",
        JobStatus.CANCELLED: "CANCELLED",
        JobStatus.UNKNOWN: "UNKNOWN",
        JobStatus.INVALID_ARGUMENT: "INVALID_ARGUMENT",
        JobStatus.DEADLINE_EXCEEDED: "DEADLINE_EXCEEDED",
        JobStatus.NOT_FOUND: "NOT_FOUND",
        JobStatus.ALREADY_EXISTS: "ALREADY_EXISTS",
        JobStatus.PERMISSION_DENIED: "PERMISSION_DENIED",
        JobStatus.RESOURCE_EXHAUSTED: "RESOURCE_EXHAUSTED",
        JobStatus.FAILED_PRECONDITION: "FAILED_PRECONDITION",
        JobStatus.ABORTED: "ABORTED",
        JobStatus.OUT_OF_RANGE: "OUT_OF_RANGE",
        JobStatus.UNIMPLEMENTED: "UNIMPLEMENTED",
        JobStatus.INTERNAL: "INTERNAL",
        JobStatus.UNAVAILABLE: "UNAVAILABLE",
        JobStatus.DATA_LOSS: "DATA_LOSS",
        JobStatus.UNAUTHENTICATED: "UNAUTHENTICATED",
    }
    return status_mapping.get(status_code, "UNKNOWN")


class JobState:
    STATE_UNSPECIFIED = 0
    ENABLED = 1
    PAUSED = 2
    DISABLED = 3
    UPDATE_FAILED = 4


def convert_job_state(state):
    state_mapping = {
        JobState.STATE_UNSPECIFIED: "STATE_UNSPECIFIED",
        JobState.ENABLED: "ENABLED",
        JobState.PAUSED: "PAUSED",
        JobState.DISABLED: "DISABLED",
        JobState.UPDATE_FAILED: "UPDATE_FAILED",
    }
    return state_mapping.get(state, "STATE_UNSPECIFIED")
