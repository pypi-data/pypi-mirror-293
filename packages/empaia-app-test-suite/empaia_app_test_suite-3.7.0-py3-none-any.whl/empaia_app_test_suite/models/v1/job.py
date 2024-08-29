"""
This modules defines different concepts that are used in the Job Service, in particular
the Job Request, which is used for creating a Job, and the Job itself, which extends
the Job Request with additional attributes on the job's current status.
"""

from enum import Enum
from typing import Annotated, Dict, List, Optional

from pydantic import UUID4, Field

from .commons import Id, ItemCount, RestrictedBaseModel, Timestamp


class JobStatus(str, Enum):
    """Current status of a Job"""

    NONE = "NONE"  # unknown status
    ASSEMBLY = "ASSEMBLY"  # Job being assembled in the WBS'
    READY = "READY"  # Assembly done, can be passed to JES
    SCHEDULED = "SCHEDULED"  # scheduled for execution
    RUNNING = "RUNNING"  # currently running
    COMPLETED = "COMPLETED"  # completed with return code == 0
    FAILED = "FAILED"  # completed with return code != 0
    TIMEOUT = "TIMEOUT"  # process killed after Request timeout
    ERROR = "ERROR"  # indicating error with job executor, i.e. outside of app
    INCOMPLETE = "INCOMPLETE"  # Job finished, but not all non-optional outputs are set


class JobCreatorType(str, Enum):
    """Type of Job Creator"""

    USER = "USER"
    SCOPE = "SCOPE"
    # AUTOMATIC = "AUTOMATIC"
    # SOLUTION = "SOLUTION"  # post-MVP


# MODELS FOR JOB SERVICE


class PostJob(RestrictedBaseModel):
    """This is sent by the workbench-service to the job-service to request the creation of a new Job.
    The full EAD has to be submitted before the Job is created; Job-Inputs are added after creation.
    """

    app_id: UUID4 = Field(
        examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"],
        description="The ID of the app to start, including the exact version of the app",
    )

    creator_id: Id = Field(
        examples=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"],
        description="ID of the scope or user, that created the job",
    )

    creator_type: JobCreatorType = Field(
        examples=[JobCreatorType.SCOPE],
        description="The type of creator that created the job. This can be a scope or a user (only for WBS v1)",
    )

    # two PostJob objects with same attributes are considered equal causing a `unhashable type` error
    # so we need to distinguish these objects by hash (see https://github.com/pydantic/pydantic/discussions/5159)
    __hash__ = object.__hash__


class Job(PostJob):
    """This describes the actual job and is a superset of the job-request, adding status parameters that are added
    after the job has been created, such as the access-token, but also status-information and references to the created
    output.
    """

    id: UUID4 = Field(
        examples=["a10648a7-340d-43fc-a2d9-4d91cc86f33f"],
        description="The unique ID of the job, set by the database",
    )

    inputs: Dict[str, str] = Field(
        examples=[
            {
                "first_input": "c10648a7-340d-43fc-a2d9-4d91cc86f33f",
            }
        ],
        description="Data references to input parameters, added after job creation",
    )

    outputs: Dict[str, str] = Field(
        examples=[
            {
                "first_output": "d10648a7-340d-43fc-a2d9-4d91cc86f33f",
            }
        ],
        description="Data references to output values, added when the job is being executed",
    )

    ead: Optional[dict] = Field(
        default=None,
        description="The full EAD description of the app; this field is not stored in the database as part of the job, "
        "but separately and can be added to the job when fetching a job by its Id",
    )

    status: JobStatus = Field(
        default=JobStatus.NONE,
        examples=[JobStatus.RUNNING],
        description="The current status of the job",
    )

    created_at: Timestamp = Field(
        examples=[1623349180],
        description="Time when the job was created",
    )

    started_at: Optional[Timestamp] = Field(
        default=None,
        examples=[1623359180],
        description="Time when execution of the job was started",
    )

    ended_at: Optional[Timestamp] = Field(
        default=None,
        examples=[1623369180],
        description="Time when the job was completed or when it failed",
    )

    runtime: Optional[int] = Field(
        default=None,
        examples=[1234],
        description="Time in seconds the job is running (if status RUNNING) or was running (if status COMPLETED)",
    )

    error_message: Optional[str] = Field(
        default=None,
        examples=["Error 123: Parameters could not be processed"],
        description="Optional error message in case the job failed",
    )


class JobList(RestrictedBaseModel):
    """Job query result."""

    item_count: ItemCount = Field(
        examples=[1],
        description="Number of Jobs as queried without skip and limit applied",
    )

    items: List[Job] = Field(
        examples=[
            [
                Job(
                    id="a10648a7-340d-43fc-a2d9-4d91cc86f33f",
                    app_id="b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                    creator_id="c10648a7-340d-43fc-a2d9-4d91cc86f33f",
                    creator_type=JobCreatorType.SCOPE,
                    inputs={"first_input": "d10648a7-340d-43fc-a2d9-4d91cc86f33f"},
                    outputs={},
                    status=JobStatus.ASSEMBLY,
                    created_at=1623349180,
                )
            ]
        ],
        description="List of Job items as queried with skip and limit applied",
    )


class JobQuery(RestrictedBaseModel):
    """Query for one or more Jobs by Status, creator, and others.
    Jobs have to match _any_ of the values in _all_ the provided fields.
    """

    statuses: Optional[Annotated[List[JobStatus], Field(min_length=1)]] = Field(
        default=None,
        examples=[[JobStatus.ASSEMBLY, JobStatus.READY]],
        description="List of job status values",
    )

    apps: Optional[Annotated[List[UUID4], Field(min_length=1)]] = Field(
        default=None,
        examples=[
            [
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            ]
        ],
        description="List of app IDs",
    )

    creators: Optional[Annotated[List[Id], Field(min_length=1)]] = Field(
        default=None,
        examples=[
            [
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            ]
        ],
        description="List of job creator IDs",
    )

    jobs: Optional[Annotated[List[UUID4], Field(min_length=1)]] = Field(
        default=None,
        examples=[
            [
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            ]
        ],
        description="List of job IDs",
    )


class JobToken(RestrictedBaseModel):
    """Wrapper for Job-ID and Access Token, returned on Job creation."""

    job_id: UUID4 = Field(
        examples=["a10648a7-340d-43fc-a2d9-4d91cc86f33f"],
        description="The ID of the newly created job corresponding to the token",
    )

    access_token: str = Field(
        examples=[
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3NTYzMDAxOC03ZjhmLTQ3YjgtODZmNC0wMTliODhjNjZhMTEiLCJle"
            "HAiOjE2MjQzNTkwNTZ9.CnT0NYwVzyNl05Jp0z4W-qDqKjolQHZxmT9i7SYyBYG6D-5K7jLxm3l4lBLp30rnjYOiZm0TtvskK1lYDh"
            "gKNyXnEhB_O7f6DQuTd9tn8yv8XnK19pj6g8nubFfBho9lYhComb6a3XX3vqLK5pnaXuhC9tFdzsnLkQPoIi2DZ8E"
        ],
        description="Access-Token used for accessing the actual data; passed to app by JES. and further to App-Service "
        "to validate authenticity of the job; decodes as {'sub': <job-id>, 'exp': <time>}.",
    )


class PutJobStatus(RestrictedBaseModel):
    """Wrapper for a status and an optional error message."""

    status: JobStatus = Field(
        ...,
        examples=[JobStatus.FAILED],
        description="The new status of the job",
    )

    error_message: Optional[str] = Field(
        default=None,
        examples=["Error 123: Parameters could not be processed"],
        description="Optional error message in case of FAILED status",
    )
