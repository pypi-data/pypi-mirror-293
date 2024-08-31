"""
This module contains classes that represent the responses from the Nutshell API.
"""

from nutshell.entities import User, Team, ActivityType, AnalyticsReport, Stageset, Milestone, Lead, Activity

from pydantic import BaseModel


class _APIResponse(BaseModel):
    """Base class for all API responses."""
    result: list[BaseModel] | BaseModel | bool


class FindUsersResult(_APIResponse):
    """Result of a FindUsers API call"""
    result: list[User]


class GetUserResult(_APIResponse):
    """"Result of a GetUser API call"""
    result: User


class FindTeamsResult(_APIResponse):
    """Result of a FindTeams API call"""
    result: list[Team]


class FindActivityTypesResult(_APIResponse):
    """Result of a FindActivityTypes API call"""
    result: list[ActivityType]


class GetAnalyticsReportResult(_APIResponse):
    """Result of a GetAnalyticsReport API call"""
    result: AnalyticsReport


class FindStagesetsResult(_APIResponse):
    """Result of a FindStagesets (Pipelines) API call"""
    result: list[Stageset]


class FindMilestonesResult(_APIResponse):
    """Result of a FindMilestones API call"""
    result: list[Milestone]


class FindLeadsResult(_APIResponse):
    """Result of a FindLeads API call"""
    result: list[Lead]


class FindActivitiesResult(_APIResponse):
    """Result of a FindActivities API"""
    result: list[Activity]


class NewActivityResult(_APIResponse):
    """Result of a NewActivity API call"""
    result: Activity


class GetActivityResult(_APIResponse):
    """Result of a GetActivity API call"""
    result: Activity


class EditActivityResult(_APIResponse):
    """Result of an EditActivity API call"""
    result: Activity


class DeleteActivityResult(_APIResponse):
    """Result of a DeleteActivity API call"""
    result: bool


class GetLeadResult(_APIResponse):
    """Result of a GetLead API call"""
    result: Lead


class EditLeadResult(_APIResponse):
    """Result of an EditLead API call"""
    result: Lead
