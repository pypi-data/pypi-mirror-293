import asyncio
from typing import Sequence
from collections import namedtuple

import aiohttp

from nutshell.methods import _APIMethod
from nutshell.responses import FindUsersResult, GetUserResult, GetAnalyticsReportResult, FindTeamsResult, \
    FindActivityTypesResult, _APIResponse, FindStagesetsResult, FindMilestonesResult, FindLeadsResult, \
    FindActivitiesResult, EditActivityResult, NewActivityResult, GetActivityResult, DeleteActivityResult, GetLeadResult, \
    EditLeadResult

_MethodResponse = namedtuple("MethodResponse", ["method", "response"])


class NutshellAPI:
    """Class to handle multiple API calls to the Nutshell API"""
    URL = "https://app.nutshell.com/api/v1/json"

    def __init__(self, username: str, password: str):
        self.auth = aiohttp.BasicAuth(username, password=password)
        self._api_calls = []

    @property
    def api_calls(self):
        return self._api_calls

    @api_calls.setter
    def api_calls(self, calls: Sequence[_APIMethod] | _APIMethod):
        self._api_calls = [calls] if isinstance(calls, _APIMethod) else calls

    def call_api(self):
        responses = asyncio.run(self._calling_api())

        return self._map_results(responses)

    async def _calling_api(self):
        tasks = []
        async with aiohttp.ClientSession() as session:
            tasks.extend(self._fetch_report(session, call) for call in self._api_calls)
            responses = await asyncio.gather(*tasks)

        return responses

    async def _fetch_report(self, session: aiohttp.ClientSession, call: _APIMethod) -> dict:
        payload = {"id": "apeye",
                   "jsonrpc": "2.0",
                   "method": call.api_method,
                   "params": call.params}
        async with session.post(self.URL, auth=self.auth, json=payload, ) as resp:
            return await resp.json()

    def _map_results(self, results: list[dict]) -> _APIResponse | list[_APIResponse]:
        call_responses = []
        for idx, call in enumerate(self._api_calls):
            match call.api_method:
                case "findUsers":
                    call_responses.append(FindUsersResult(**results[idx]))
                case "getUser":
                    call_responses.append(GetUserResult(**results[idx]))
                case "findTeams":
                    call_responses.append(FindTeamsResult(**results[idx]))
                case "findActivityTypes":
                    call_responses.append(FindActivityTypesResult(**results[idx]))
                case "getAnalyticsReport":
                    call_responses.append(GetAnalyticsReportResult(**results[idx]))
                case "findStagesets":
                    call_responses.append(FindStagesetsResult(**results[idx]))
                case "findMilestones":
                    call_responses.append(FindMilestonesResult(**results[idx]))
                case "findLeads":
                    call_responses.append(FindLeadsResult(**results[idx]))
                case "findActivities":
                    call_responses.append(FindActivitiesResult(**results[idx]))
                case "newActivity":
                    call_responses.append(NewActivityResult(**results[idx]))
                case "getActivity":
                    call_responses.append(GetActivityResult(**results[idx]))
                case "editActivity":
                    call_responses.append(EditActivityResult(**results[idx]))
                case "deleteActivity":
                    call_responses.append(DeleteActivityResult(**results[idx]))
                case "getLead":
                    call_responses.append(GetLeadResult(**results[idx]))
                case "editLead":
                    call_responses.append(EditLeadResult(**results[idx]))
        return call_responses[0] if len(call_responses) == 1 else call_responses
