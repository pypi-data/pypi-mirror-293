# -*- coding: utf-8 -*-
"""Data signals types."""

import datetime

from pydantic import BaseModel, ValidationInfo, field_validator


class Metric(BaseModel):
    """A pydantic schema for the metrics names."""

    start_timestamp: str
    end_timestamp: str
    site: str
    location: str
    data_group: str | None
    metric: str
    statistic: str | None
    short_hand: str | None
    unit_str: str | None
    print_str: str | None
    description: str | None
    crud_privileges: str | None


class Metrics(BaseModel):
    """A pydantic schema for the metrics names."""

    metrics: list[Metric]


class GetData(BaseModel):
    """A pydantic schema for the data signals."""

    start_timestamp: str | datetime.datetime
    end_timestamp: str | datetime.datetime
    sites: str | list[str] | None
    locations: str | list[str] | None
    metrics: str | list[str] | None
    outer_join_on_timestamp: bool | None
    headers: dict[str, str] | None

    @field_validator("start_timestamp", "end_timestamp", mode="before")
    def validate_timestamp(cls, v: str | datetime.datetime) -> str:
        """Validate the timestamps."""
        if isinstance(v, str):
            try:
                datetime.datetime.strptime(v, "%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                raise ValueError(
                    "Incorrect start timestamp format, expected ISO 8601."
                )

        if isinstance(v, datetime.datetime):
            # Enforce timezone UTC as well
            return v.strftime("%Y-%m-%dT%H:%M:%SZ")

        return v

    @field_validator("end_timestamp")
    def validate_end_timestamp(cls, v, info: ValidationInfo):
        """Validate the end timestamp."""
        if "start_timestamp" in info.data and v < info.data["start_timestamp"]:
            raise ValueError(
                "End timestamp must be greater than start timestamp."
            )
        return v

    @field_validator("sites", "locations", mode="before")
    def validate_sites_locations(cls, v):
        """Validate and normalize sites and locations."""
        if isinstance(v, str):
            v = [v]
        if isinstance(v, list):
            v = [item.lower() for item in v]
        return v

    @field_validator("metrics", mode="before")
    def validate_metrics(cls, v):
        """Validate and normalize metrics."""
        if isinstance(v, str):
            v = [v]
        if isinstance(v, list):
            # fmt: off
            v = [item.replace(" ", ".*")
                     .replace("_", ".*")
                     .replace("-", ".*") for item in v]
            # fmt: on
        return "|".join(v)

    @field_validator("outer_join_on_timestamp", mode="before")
    def validate_outer_join_on_timestamp(cls, v):
        """Validate the outer join on timestamp."""
        if v is None:
            return False
        return v

    @field_validator("headers", mode="before")
    def validate_headers(cls, v):
        """Validate the headers."""
        if v is None:
            return {"accept": "application/json"}
        return v
