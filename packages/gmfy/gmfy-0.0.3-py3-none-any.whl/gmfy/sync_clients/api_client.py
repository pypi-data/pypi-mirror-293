from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import requests

from gmfy.base_api_client import GMFYApiClientBase
from gmfy.exceptions import GMFYClientError

if TYPE_CHECKING:
    from gmfy import BasePayment
    from gmfy.event_managers import EventManager, SingleEventManager


class GMFYApiClientSync(GMFYApiClientBase):
    def __init__(self, api_key: str, base_url: str, verify: bool, timeout: int) -> None:
        super().__init__(api_key, base_url)
        self.session = requests.Session()
        self.session.verify = verify
        self.timeout = timeout
        self.session.headers.update(self.headers)

    def _get(self, url: str | None, **kwargs) -> requests.Response:
        try:
            if url is None:
                error_message = "URL doesn't exist, the request was canceled"
                raise GMFYClientError(error_message)
            params = kwargs.get("params", {})
            response = self.session.get(url, timeout=self.timeout, params=params)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            error_message = f"Bad response status for {url}"
            raise GMFYClientError(error_message) from error
        except (
            requests.ConnectionError,
            requests.Timeout,
            requests.RequestException,
        ) as error:
            error_message = "Network error when fetching gmfy"
            raise GMFYClientError(error_message) from error
        else:
            message = f"Successful GET request to {url}"
            logging.info(message)
            return response

    def _post(self, url: str | None, data: Any) -> requests.Response:
        try:
            if url is None:
                error_message = "URL doesn't exist, the request was canceled"
                raise GMFYClientError(error_message)
            response = self.session.post(url=url, data=data, timeout=self.timeout)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            error_message = f"Bad response status for {url}"
            raise GMFYClientError(error_message) from error
        except (
            requests.ConnectionError,
            requests.Timeout,
            requests.RequestException,
        ) as error:
            error_message = "Network error when fetching gmfy"
            raise GMFYClientError(error_message) from error
        else:
            message = f"Successful POST request to {url}"
            logging.info(message)
            return response

    def create_event(self, event_manager: SingleEventManager) -> requests.Response:
        dumped_event = event_manager.model_dump_json(by_alias=True)
        return self._post(self.urls.get("post_event"), dumped_event)

    def create_events(self, event_manager: EventManager) -> requests.Response:
        dumped_events = event_manager.model_dump_json(by_alias=True)
        return self._post(self.urls.get("post_events"), dumped_events)

    def create_payment(self, payment: BasePayment) -> requests.Response:
        dumped_payment = payment.model_dump_json(by_alias=True)
        return self._post(self.urls.get("post_payment"), dumped_payment)

    def create_resend_code(self, payment_id: str) -> requests.Response:
        return self._post(
            self.urls.get("resend_code").format(payment_id=payment_id),  # type: ignore[union-attr]
            None,
        )

    def get_version(self) -> requests.Response:
        return self._get(self.urls.get("get_version"))

    def get_users(self, user_id: str | None) -> requests.Response:
        if user_id:
            return self._get(self.urls.get("get_user").format(user_id=user_id))  # type: ignore[union-attr]
        return self._get(self.urls.get("get_users"))

    def get_rating_top_users(
        self,
        rating_id: str,
        params: dict[str, object],
    ) -> requests.Response:
        return self._get(
            self.urls.get("get_ratings").format(rating_id=rating_id),  # type: ignore[union-attr]
            params=params,
        )

    def get_challenge_top_users(
        self,
        challenge_id: str,
        params: dict[str, int],
    ) -> requests.Response:
        return self._get(
            self.urls.get("get_challenges").format(challenge_id=challenge_id),  # type: ignore[union-attr]
            params=params,
        )

    def get_user_badges(self, user_id: str) -> requests.Response:
        return self._get(self.urls.get("get_badges").format(user_id=user_id))  # type: ignore[union-attr]

    def get_notifications(self) -> requests.Response:
        return self._get(self.urls.get("get_notifications"))

    def get_unread_notifications(self, user_id: str | None = None) -> requests.Response:
        if user_id:
            return self._get(
                self.urls.get("get_unread_notifications_user").format(user_id=user_id),  # type: ignore[union-attr]
            )
        return self._get(self.urls.get("get_unread_notifications"))

    def get_payment(self, payment_id: str) -> requests.Response:
        return self._get(self.urls.get("get_payment").format(payment_id=payment_id))  # type: ignore[union-attr]

    def close(self) -> None:
        self.session.close()
