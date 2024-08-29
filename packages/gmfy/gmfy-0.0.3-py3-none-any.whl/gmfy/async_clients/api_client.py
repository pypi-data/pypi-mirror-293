from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import httpx

from gmfy.base_api_client import GMFYApiClientBase
from gmfy.exceptions import GMFYClientError

if TYPE_CHECKING:
    from gmfy import BasePayment
    from gmfy.event_managers import EventManager, SingleEventManager


class GMFYApiClientAsync(GMFYApiClientBase):
    def __init__(self, api_key: str, base_url: str, verify: bool, timeout: int) -> None:
        super().__init__(api_key, base_url)
        self.session = httpx.AsyncClient(
            headers=self.headers,
            verify=verify,
            timeout=timeout,
        )

    async def _get(self, url: str | None, **kwargs: Any) -> httpx.Response:
        try:
            if url is None:
                error_message = "URL doesn't exist, the request was canceled"
                raise GMFYClientError(error_message)
            params = kwargs.get("params", {})
            response = await self.session.get(url, params=params)
            response.raise_for_status()
        except httpx.HTTPStatusError as error:
            error_message = f"Bad response status for {url}"
            raise GMFYClientError(error_message) from error
        except (
            httpx.ConnectError,
            httpx.TimeoutException,
            httpx.RequestError,
        ) as error:
            error_message = "Network error when fetching gmfy"
            raise GMFYClientError(error_message) from error
        else:
            message = f"Successful GET request to {url}"
            logging.info(message)
            return response

    async def _post(self, url: str | None, data: Any) -> httpx.Response:
        try:
            if url is None:
                error_message = "URL doesn't exist, the request was canceled"
                raise GMFYClientError(error_message)
            response = await self.session.post(url=url, data=data)
            response.raise_for_status()
        except httpx.HTTPStatusError as error:
            error_message = f"Bad response status for {url}"
            raise GMFYClientError(error_message) from error
        except (
            httpx.ConnectError,
            httpx.TimeoutException,
            httpx.RequestError,
        ) as error:
            error_message = "Network error when fetching gmfy"
            raise GMFYClientError(error_message) from error
        else:
            message = f"Successful POST request to {url}"
            logging.info(message)
            return response

    async def create_event(self, event_manager: SingleEventManager) -> httpx.Response:
        dumped_event = event_manager.model_dump_json(by_alias=True)
        return await self._post(self.urls.get("post_event"), dumped_event)

    async def create_events(self, event_manager: EventManager) -> httpx.Response:
        dumped_events = event_manager.model_dump_json(by_alias=True)
        return await self._post(self.urls.get("post_events"), dumped_events)

    async def create_payment(self, payment: BasePayment) -> httpx.Response:
        dumped_payment = payment.model_dump_json(by_alias=True)
        return await self._post(self.urls.get("post_payment"), dumped_payment)

    async def create_resend_code(self, payment_id: str) -> httpx.Response:
        return await self._post(
            self.urls.get("resend_code").format(payment_id=payment_id),  # type: ignore[union-attr]
            None,
        )

    async def get_version(self) -> httpx.Response:
        return await self._get(self.urls.get("get_version"))

    async def get_users(self, user_id: str | None) -> httpx.Response:
        if user_id:
            return await self._get(self.urls.get("get_user").format(user_id=user_id))  # type: ignore[union-attr]
        return await self._get(self.urls.get("get_users"))

    async def get_rating_top_users(
        self,
        rating_id: str,
        params: dict[str, object],
    ) -> httpx.Response:
        return await self._get(
            self.urls.get("get_ratings").format(rating_id=rating_id),  # type: ignore[union-attr]
            params=params,
        )

    async def get_challenge_top_users(
        self,
        challenge_id: str,
        params: dict[str, int],
    ) -> httpx.Response:
        return await self._get(
            self.urls.get("get_challenges").format(challenge_id=challenge_id),  # type: ignore[union-attr]
            params=params,
        )

    async def get_user_badges(self, user_id: str) -> httpx.Response:
        return await self._get(self.urls.get("get_badges").format(user_id=user_id))  # type: ignore[union-attr]

    async def get_notifications(self) -> httpx.Response:
        return await self._get(self.urls.get("get_notifications"))

    async def get_unread_notifications(
        self,
        user_id: str | None = None,
    ) -> httpx.Response:
        if user_id:
            return await self._get(
                self.urls.get("get_unread_notifications_user").format(user_id=user_id),  # type: ignore[union-attr]
            )
        return await self._get(self.urls.get("get_unread_notifications"))

    async def get_payment(self, payment_id: str) -> httpx.Response:
        return await self._get(
            self.urls.get("get_payment").format(payment_id=payment_id),  # type: ignore[union-attr]
        )

    async def close(self) -> None:
        await self.session.aclose()
