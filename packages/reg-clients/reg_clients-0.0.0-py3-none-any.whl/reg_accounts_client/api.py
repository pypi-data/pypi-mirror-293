import logging
import os
import typing as t
import urllib.parse

import marshmallow_recipe as mr
from reg_shared_lib.api import BaseAPIClient, HttpClientProtocol

from .data import User

logger = logging.getLogger(__name__)
_not_set: t.Any = object()


class AccountsAPIClient(BaseAPIClient):
    async def get_by_param(
        self, *, telegram_id: str | None = None, telegram_username: str | None = None, rus_youth_id: str | None = None
    ) -> User | None:
        query = urllib.parse.urlencode(
            {
                k: (v or "").strip()
                for k, v in {
                    "telegram_id": telegram_id,
                    "telegram_username": telegram_username,
                    "rus_youth_id": rus_youth_id,
                }.items()
                if (v or "").strip()
            }
        )
        assert query
        users = await self._make_request("get", f"accounts/internal/api/user/?{query}")
        if not users:
            return None
        if len(users) != 1:
            logger.warning("Too many users to return")
            return None
        return mr.load(User, users[0])

    async def update_user(self, user_id: int, *, telegram_id: str | None = None) -> User | None:
        assert telegram_id
        user = await self._make_request(
            "put", f"accounts/internal/api/user/{user_id}/", data={"telegram_id": telegram_id}
        )
        if user:
            return mr.load(User, user)

    def __init__(self, client: HttpClientProtocol) -> None:
        self.base_url = os.getenv("REG_ACCOUNTS_URL") + "/"  # type: ignore[reportOptionalOperand]
        super().__init__(client)
