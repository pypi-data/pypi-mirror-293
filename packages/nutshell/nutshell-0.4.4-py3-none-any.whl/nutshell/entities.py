"""
This module contains Enums as well as pydantic models for various entities in the Nutshell API
"""

from __future__ import annotations

from enum import StrEnum, IntEnum
from typing import Optional

from pydantic import BaseModel, computed_field, Field


class AnalyticsReportType(StrEnum):
    """
    Enumeration of analytics report types available in the system.

    This enum is used to specify the type of report to generate or analyze.

    Attributes
    ----------
    EFFORT : str
    PIPELINE : str
    """
    EFFORT = "Effort"
    PIPELINE = "Pipeline"


class FindLeadsQueryStatus(IntEnum):
    """
    Enum for the status of a lead.

    Attributes
    ----------
    OPEN : Open status.
    CANCELLED : Cancelled status.
    LOST : Lost status.
    WON : Won status.
    
    """
    OPEN = 0
    CANCELLED = 12
    LOST = 11
    WON = 10


class FindLeadsQueryFilter(IntEnum):
    """
    Enum for the filter to apply to the leads query.

    ...
    Attributes
    ----------
    MY_LEADS : My leads filter.
    MY_TEAM_LEADS : My team leads filter.
    ALL_LEADS : All leads filter.
    
    """
    MY_LEADS = 0
    MY_TEAM_LEADS = 1
    ALL_LEADS = 2


class ActivityStatus(IntEnum):
    """
    Enum for the status of an activity.

    Attributes
    ----------
    SCHEDULED : Scheduled status.
    LOGGED : Logged status.
    CANCELLED : Cancelled status.
    OVERDUE: Overdue status.
    
    """
    SCHEDULED = 0
    LOGGED = 1
    CANCELLED = 2
    OVERDUE = -1


class User(BaseModel):
    """Model of a Nutshell User"""
    stub: bool = None
    id: int
    entity_type: str = Field(..., alias="entityType", pattern=r"Users")
    rev: str
    name: str
    first_name: str = Field(None, alias="firstName")
    last_name: str = Field(None, alias="lastName")
    is_enabled: bool = Field(..., alias="isEnabled")
    is_administrator: bool = Field(..., alias="isAdministrator")
    emails: list[str]
    modified_time: str = Field(..., alias="modifiedTime")
    created_time: str = Field(..., alias="createdTime")


class Team(BaseModel):
    """Model of a Nutshell Team"""
    stub: bool
    id: int
    name: str
    rev: str
    entity_type: str = Field(..., alias="entityType", pattern=r"Teams")
    modified_time: str = Field(..., alias="modifiedTime")
    created_time: str = Field(..., alias="createdTime")


class ActivityType(BaseModel):
    """Model of a Nutshell Activity Type"""
    stub: bool
    id: int
    rev: str
    entity_type: str = Field(..., alias="entityType", pattern=r"Activity_Types")
    name: str
    deleted_time: Optional[str] = Field(None, alias="deletedTime")


class TimeSeriesData(BaseModel):
    """Model of the Time Series Data for an Analytics Report"""
    total_effort: list[list[int]]
    successful_effort: list[list[int]]


class SummaryData(BaseModel):
    """Model of the Summary Data for an Analytics Report"""
    sum: float
    avg: float
    min: float
    max: float
    sum_delta: float
    avg_delta: float
    min_delta: float
    max_delta: float


class AnalyticsReport(BaseModel):
    """Model for constructing a Nutshell Analytics Report"""
    series_data: TimeSeriesData = Field(..., alias="seriesData")
    summary_data: dict[str, SummaryData] = Field(..., alias="summaryData")
    period_description: str = Field(..., alias="periodDescription")
    delta_period_description: str = Field(..., alias="deltaPeriodDescription")


class Stageset(BaseModel):
    """Model of a Nutshell Stageset (Pipeline) """
    id: int
    entity_type: str = Field(..., alias="entityType", pattern=r"Stagesets")
    name: str
    default: Optional[int] = None
    position: Optional[int] = None


class Milestone(BaseModel):
    """Model of a Nutshell Milestone"""
    id: int
    entity_type: str = Field(..., alias="entityType", pattern=r"Milestones")
    rev: str
    name: str
    position: Optional[int] = None
    stageset_id: Optional[int] = Field(None, alias="stagesetId")


class Lead(BaseModel):
    """Model of a Nutshell Lead"""
    stub: Optional[bool] = None
    id: int
    entity_type: str = Field(..., alias="entityType", pattern=r"Leads")
    rev: str
    name: str
    html_url: Optional[str] = Field(None, alias="htmlUrl")
    tags: Optional[list[str]] = None
    description: str
    created_time: Optional[str] = Field(None, alias="createdTime")
    creator: Optional[User] = None
    milestone: Optional[Milestone] = None
    stageset: Optional[Stageset] = None
    status: int
    confidence: Optional[int] = None
    assignee: Optional[User | Team] = None
    due_time: Optional[str] = Field(None, alias="dueTime")
    value: Optional[dict[str, float | str]] = 0
    normalized_value: Optional[dict[str, float | str]] = Field(None, alias="normalizedValue")
    products: Optional[list[dict]] = None
    primary_account: Optional[dict] = Field(None, alias="primaryAccount")
    custom_fields: Optional[dict] = Field(None, alias="customFields")


class Activity(BaseModel):
    """Model of a Nutshell Activity"""
    id: int
    stub: Optional[bool] = None
    entity_type: str = Field(..., alias="entityType", pattern=r"Activities")
    rev: str
    name: str
    description: Optional[str] = None
    activity_type: ActivityType = Field(None, alias="activityType")
    lead: Optional[Lead] = None
    leads: Optional[list[Lead]] = None
    start_time: str = Field(..., alias="startTime")
    end_time: str = Field(..., alias="endTime")
    is_all_day: bool = Field(..., alias="isAllDay")
    is_flagged: bool = Field(..., alias="isFlagged")
    status: int
    log_description: Optional[str] = Field(None, alias="logDescription")
    log_note: Optional[dict] = Field(None, alias="logNote")
    logged_by: Optional[dict[str, str | int | list]] = Field(None, alias="loggedBy")
    participants: Optional[list] = None
    follow_up: Optional[Activity] = Field(None, alias="followUp")
    follow_up_to: Optional[Activity] = Field(None, alias="followUpTo")
    deleted_time: Optional[str] = Field(None, alias="deletedTime")
    modified_time: str = Field(..., alias="modifiedTime")
    created_time: str = Field(..., alias="createdTime")


class CreateActivity(BaseModel):
    """Minimal class for creating an activity in the Nutshell API. serialization_alias used as this class should only be
    used to create a new activity"""

    name: str = None
    description: str = None
    activity_type_id: int = Field(None, serialization_alias="activityTypeId")
    leads: Optional[list[Lead]] = None
    start_time: str = Field(..., serialization_alias="startTime")
    end_time: str = Field(..., serialization_alias="endTime")
    is_all_day: Optional[bool] = Field(None, serialization_alias="isAllDay")
    is_flagged: Optional[bool] = Field(None, serialization_alias="isFlagged")
    status: Optional[int] = None
    participants: Optional[list] = None


class FindLeadsQuery(BaseModel):
    """Model for building a FindLeads query"""
    status: Optional[FindLeadsQueryStatus] = None
    filter: Optional[FindLeadsQueryFilter] = None
    milestone_id: Optional[int] = None
    milestone_ids: Optional[list[int]] = None
    stageset_id: Optional[int] = None
    stageset_ids: Optional[list[int]] = None
    due_time: Optional[str] = None
    assignee: Optional[list[User | Team]] = None
    number: Optional[int] = None

    @computed_field
    @property
    def query(self) -> dict:
        query_dict = {}

        if isinstance(self.status, FindLeadsQueryStatus):
            query_dict["status"] = self.status.value
        if isinstance(self.filter, FindLeadsQueryFilter):
            query_dict["filter"] = self.filter.value
        if self.milestone_id:
            query_dict["milestoneId"] = self.milestone_id
        if self.milestone_ids:
            query_dict["milestoneIds"] = self.milestone_ids
        if self.stageset_id:
            query_dict["stagesetId"] = self.stageset_id
        if self.stageset_ids:
            query_dict["stagesetIds"] = self.stageset_ids
        if self.due_time:
            query_dict["dueTime"] = self.due_time
        if self.assignee:
            query_dict["assignee"] = [
                {"entityType": entity.entity_type, "id": entity.id} for entity in self.assignee
            ]
        if self.number:
            query_dict["number"] = self.number

        return query_dict


class FindActivitiesQuery(BaseModel):
    """Model for building a FindActivities query"""
    lead_id: Optional[int] = None
    contact_id: Optional[list[int]] = None
    account_id: Optional[list[int]] = None
    user_id: Optional[list[int]] = None
    status: Optional[ActivityStatus] = None
    activity_type_id: Optional[list[int]] = None
    is_flagged: Optional[bool] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None

    @computed_field
    @property
    def query(self) -> dict:
        query_dict = {}

        if self.lead_id:
            query_dict["leadId"] = self.lead_id
        if self.contact_id:
            query_dict["contactId"] = self.contact_id
        if self.account_id:
            query_dict["accountId"] = self.account_id
        if self.user_id:
            query_dict["userId"] = self.user_id
        if isinstance(self.status, ActivityStatus):
            query_dict["status"] = self.status.value
        if self.activity_type_id:
            query_dict["activityTypeId"] = self.activity_type_id
        if self.is_flagged:
            query_dict["isFlagged"] = self.is_flagged
        if self.start_time:
            query_dict["startTime"] = self.start_time
        if self.end_time:
            query_dict["endTime"] = self.end_time

        return query_dict
