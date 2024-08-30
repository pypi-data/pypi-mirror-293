import asyncio
import datetime
import json
import logging
import os
import typing as t
import urllib.parse

import marshmallow_recipe as mr
from reg_shared_lib.api import BaseAPIClient, BaseClientError, HttpClientProtocol, RequestProtocol, ResponseProtocol

from .data import Draft, Plan

logger = logging.getLogger(__name__)
_not_set: t.Any = object()


class ClientError(BaseClientError):
    @classmethod
    async def from_response(cls, url: str, request: RequestProtocol, response: ResponseProtocol):
        error_class = cls
        if response.status_code == 400:
            validation_error = response.json()
            if asyncio.iscoroutine(validation_error):
                validation_error_json = json.loads(await validation_error)
            else:
                validation_error_json = validation_error
            if action_error := validation_error_json.get("action"):
                match action_error:
                    case ["Wrong stream"]:
                        error_class = WrongStreamError
                    case ["Maximal capacity exceeded"]:
                        error_class = MaxCapacityExceededError
                    case ["Minimal age error"]:
                        error_class = RequiredMinimalAgeError
                    case _:
                        pass
        return error_class(url, request, response)


class DraftAPIClient(BaseAPIClient):
    error_class = ClientError

    async def get_draft(
        self,
        event_slug: str,
        *,
        date: datetime.date | None = None,
        units: list[int] | None = None,
        actions: list[int] | None = None,
        name: str | None = None,
        numbers: list[int] | None = None,
    ) -> Draft:
        assert date or units or actions or name or numbers

        query: list[tuple[str, str | int]] = []
        if date:
            query.append(("date", date.isoformat()))
        if units:
            query.extend([("units", int(i)) for i in units])
        if actions:
            query.extend([("actions", int(i)) for i in actions])
        if name:
            query.append(("name", name))
        if numbers:
            query.extend([("numbers", int(i)) for i in numbers])
        query_str = urllib.parse.urlencode(query)

        response = await self._make_request("get", f"{event_slug}/draft/internal/api/?{query_str}")
        return mr.load(Draft, response)

    async def get_plan(self, event_slug: str, user_id: int) -> Plan:
        response = await self._make_request("get", f"{event_slug}/draft/internal/api/plan/{user_id}/")
        return mr.load(Plan, response)

    async def add_to_plan(self, event_slug: str, *, user_id: int, action: int) -> Plan:
        response = await self._make_request(
            "patch", f"{event_slug}/draft/internal/api/plan/{user_id}/", data={"action": action}
        )
        return mr.load(Plan, response)

    async def remove_from_plan_by_number(self, event_slug: str, *, user_id: int, number: int) -> Plan:
        response = await self._make_request(
            "delete", f"{event_slug}/draft/internal/api/plan/{user_id}/?number={number}"
        )
        return mr.load(Plan, response)

    def __init__(self, client: HttpClientProtocol):
        self.base_url = os.getenv("REG_DRAFT_URL") + "/"  # type: ignore[reportOptionalOperand]
        super().__init__(client)


class MaxCapacityExceededError(ClientError):
    pass


class WrongStreamError(ClientError):
    pass


class RequiredMinimalAgeError(ClientError):
    pass
