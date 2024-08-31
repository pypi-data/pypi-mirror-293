"""
This module contains pydantic models for each implemented method on the Nutshell API.

Methods are intantiated then passed to the NutshellAPI class to actually make the call.

"""

from typing import Optional

from pydantic import BaseModel, computed_field

from nutshell.entities import AnalyticsReportType, FindLeadsQuery, ActivityType, User, Team, FindActivitiesQuery, \
    CreateActivity


class _APIMethod(BaseModel):
    """
    Base class for all method calls to the Nutshell API.

    This class should not be used directly, but should be subclassed for each API method.
    """
    api_method: str

    @computed_field
    @property
    def params(self) -> dict:
        return {}


class FindUsers(_APIMethod):
    """Retrieves a list of users, and may be optionally filtered."""
    query: Optional[dict] = None
    order_by: str = "last_name"
    order_direction: str = "ASC"
    limit: int = 50
    page: int = 1
    api_method: str = "findUsers"

    @computed_field
    @property
    def params(self) -> dict:
        params = {
            "orderBy": self.order_by,
            "orderDirection": self.order_direction,
            "limit": self.limit,
            "page": self.page
        }
        if self.query:
            params["query"] = self.query

        return params


class GetUser(_APIMethod):
    """Retrieves a single user"""
    user_id: int = None  # with no user_id, the API will return the current user
    rev: str = None  # included to match API documentation
    api_method: str = "getUser"

    @computed_field
    @property
    def params(self) -> dict:
        params = {}
        if self.user_id:
            params["userId"] = self.user_id
        if self.rev:
            params["rev"] = self.rev
        return params


class FindTeams(_APIMethod):
    """Retrieves a list of teams"""
    order_by: str = "name"
    order_direction: str = "ASC"
    limit: int = 50
    page: int = 1
    api_method: str = "findTeams"

    @computed_field
    @property
    def params(self) -> dict:
        params = {
            "orderBy": self.order_by,
            "orderDirection": self.order_direction,
            "limit": self.limit,
            "page": self.page
        }

        return params


class FindActivityTypes(_APIMethod):
    """Retrieves a list of activity types"""
    order_by: str = "name"
    order_direction: str = "ASC"
    limit: int = 50
    page: int = 1
    api_method: str = "findActivityTypes"

    @computed_field
    @property
    def params(self) -> dict:
        params = {
            "orderBy": self.order_by,
            "orderDirection": self.order_direction,
            "limit": self.limit,
            "page": self.page
        }

        return params


class GetAnalyticsReport(_APIMethod):
    """Retrieves an analytics report based on report type and optional filters"""
    report_type: AnalyticsReportType
    period: str
    filters: Optional[list[User | Team | ActivityType]] = None
    options: list[dict] = None  # little documentation 
    api_method: str = "getAnalyticsReport"

    @computed_field
    @property
    def params(self) -> dict:
        params = {"reportType": self.report_type.value,
                  "period": self.period}
        if self.filters:
            params["filter"] = [{"entityId": entity.id, "entityName": entity.entity_type} for entity in self.filters]
        if self.options:
            params["options"] = self.options
        return params


class FindStagesets(_APIMethod):
    """Retreives a list of pipelines (stagesets)"""
    order_by: str = "name"
    order_direction: str = "ASC"
    limit: int = 50
    page: int = 1
    api_method: str = "findStagesets"

    @computed_field
    @property
    def params(self) -> dict:
        params = {
            "orderBy": self.order_by,
            "orderDirection": self.order_direction,
            "limit": self.limit,
            "page": self.page
        }
        return params


class FindMilestones(_APIMethod):
    """Retrieves a list of milestones"""
    order_by: str = "name"
    order_direction: str = "ASC"
    limit: int = 50
    page: int = 1
    api_method: str = "findMilestones"

    @computed_field
    @property
    def params(self) -> dict:
        params = {
            "orderBy": self.order_by,
            "orderDirection": self.order_direction,
            "limit": self.limit,
            "page": self.page
        }
        return params


class FindLeads(_APIMethod):
    """Retrieves a list of leads with optional query to filter results"""
    query: Optional[FindLeadsQuery] = None
    order_by: str = "id"
    order_direction: str = "ASC"
    limit: int = 50
    page: int = 1
    stub_responses: bool = True
    api_method: str = "findLeads"

    @computed_field
    @property
    def params(self) -> dict:
        params = {
            "query": {},
            "orderBy": self.order_by,
            "orderDirection": self.order_direction,
            "limit": self.limit,
            "page": self.page,
            "stubResponses": self.stub_responses
        }
        if self.query:
            params["query"] = self.query.query
        return params


# TODO: add findActivities
class FindActivities(_APIMethod):
    """Retrieves a list of activities with an optional query to filter results"""
    query: Optional[FindActivitiesQuery] = None
    order_by: str = "name"
    order_direction: str = "ASC"
    limit: int = 50
    page: int = 1
    stub_responses: bool = True
    api_method: str = "findActivities"

    @computed_field
    @property
    def params(self) -> dict:
        params = {
            "query": {},
            "orderBy": self.order_by,
            "orderDirection": self.order_direction,
            "limit": self.limit,
            "page": self.page,
            "stubResponses": self.stub_responses
        }
        if self.query:
            params["query"] = self.query.query
        return params


class NewActivity(_APIMethod):
    """Creates a new activity"""
    activity: CreateActivity
    api_method: str = "newActivity"

    @computed_field
    @property
    def params(self) -> dict:
        return {
            "activity": self.activity.model_dump(by_alias=True, exclude_none=True)
        }


class GetActivity(_APIMethod):
    """Retrieves a single activity"""
    activity_id: int
    api_method: str = "getActivity"

    @computed_field
    @property
    def params(self) -> dict:
        return {
            "activityId": self.activity_id
        }


class EditActivity(_APIMethod):
    """Edits a single activity"""
    activity_id: int
    rev: str
    activity: dict
    api_method: str = "editActivity"

    @computed_field
    @property
    def params(self) -> dict:
        return {
            "activityId": self.activity_id,
            "rev": self.rev,
            "activity": self.activity
        }


class DeleteActivity(_APIMethod):
    """Deletes a single activity"""
    activity_id: int
    rev: str
    api_method: str = "deleteActivity"

    @computed_field
    @property
    def params(self) -> dict:
        return {
            "activityId": self.activity_id,
            "rev": self.rev
        }


class GetLead(_APIMethod):
    """Retrieves a single lead"""
    lead_id: int
    api_method: str = "getLead"

    @computed_field
    @property
    def params(self) -> dict:
        return {
            "leadId": self.lead_id
        }


class EditLead(_APIMethod):
    """Edits a single lead"""
    lead_id: int
    rev: str
    lead: dict
    api_method: str = "editLead"

    @computed_field
    @property
    def params(self) -> dict:
        return {
            "leadId": self.lead_id,
            "rev": self.rev,
            "lead": self.lead
        }

# TODO: add findTimeline

# TODO: add searchLeads
