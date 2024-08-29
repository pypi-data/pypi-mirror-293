from typing import List, Optional

from pydantic import ConfigDict, Field

from .commons import RestrictedBaseModel


class StorageAddress(RestrictedBaseModel):
    storage_address_id: str = Field(examples=["a7981525-a465-4240-8da5-e2defae6a746"], description="Storage address ID")
    path: str = Field(
        examples=["path/to/wsi.ext"],
        description="Path to WSI file (can be a file or directory, e.g. in case of DICOM)",
    )


class PutSlideStorage(RestrictedBaseModel):
    """Class representing the put model of a slide storage object."""

    main_storage_address: StorageAddress = Field(
        description="Main storage address to WSI file (can be a file or directory, e.g. in case of DICOM)",
    )
    secondary_storage_addresses: Optional[List[StorageAddress]] = Field(
        default=None,
        description="List of all related secondary storage addresses",
    )

    model_config = ConfigDict(from_attributes=True)


class SlideStorage(PutSlideStorage):
    """Class representing the model of a slide storage object."""

    slide_id: str = Field(examples=["a7981525-a465-4240-8da5-e2defae6a746"], description="Slide ID")
