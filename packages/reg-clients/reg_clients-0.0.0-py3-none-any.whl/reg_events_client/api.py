import logging
import os
import typing as t

import marshmallow_recipe as mr
from reg_shared_lib.api import BaseAPIClient, HttpClientProtocol

from .data import Event

logger = logging.getLogger(__name__)
_not_set: t.Any = object()


class EventsAPIClient(BaseAPIClient):
    async def get_event(self, event_slug: str) -> Event:
        response = await self._make_request("get", f"{event_slug}/events/internal/api/event/")
        return mr.load(Event, response)

    def __init__(self, client: HttpClientProtocol):
        self.base_url = os.getenv("REG_EVENTS_URL") + "/"  # type: ignore[reportOptionalOperand]
        super().__init__(client)
