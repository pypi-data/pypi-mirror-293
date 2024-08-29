from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from pydantic import ValidationError

from gmfy.event_managers import EventManager, Events, SingleEventManager
from gmfy.exceptions import GMFYClientError
from gmfy.sync_clients.api_client import GMFYApiClientSync

if TYPE_CHECKING:
    import requests

    from gmfy import BasePayment


class GMFYClientSync:
    def __init__(
        self,
        api_key: str,
        base_url: str,
        verify: bool = True,
        timeout: int = 60,
    ):
        self.api_sync_client = GMFYApiClientSync(api_key, base_url, verify, timeout)

    def create_batch_events(self, events: list[Events]) -> requests.Response:
        try:
            message = f"Creating batch events for {len(events)} events"
            logging.info(message)
            event_manager = EventManager(events)
            event_manager.root = [
                event for event in event_manager.root if event.is_ready
            ]
            response = self.api_sync_client.create_events(event_manager)
        except ValidationError as error:
            error_message = "Validation error while creating events"
            raise GMFYClientError(error_message) from error
        else:
            message = (
                f"Batch events created successfully. "
                f"Status code: {response.status_code}. "
                f"Response: {response.text}"
            )
            logging.info(message)
            return response

    def create_event(self, event: Events) -> requests.Response:
        try:
            message = f"Creating event: {event}"
            logging.info(message)
            event_manager = SingleEventManager(event)
            response = self.api_sync_client.create_event(event_manager)
        except ValidationError as error:
            error_message = "Validation error while creating event"
            raise GMFYClientError(error_message) from error
        else:
            message = (
                f"Event created successfully. "
                f"Status code: {response.status_code}."
                f" Response: {response.text}"
            )
            logging.info(message)
            return response

    def create_payment(self, payment: BasePayment) -> requests.Response:
        try:
            message = f"Creating payment: {payment}"
            logging.info(message)
            response = self.api_sync_client.create_payment(payment)
        except ValidationError as error:
            message = "Validation error while creating payment"
            raise GMFYClientError(message) from error
        else:
            message = (
                f"Payment created successfully. "
                f"Status code: {response.status_code}."
                f" Response: {response.text}"
            )
            logging.info(message)
            return response

    def create_resend_code(self, payment_id: str) -> requests.Response:
        message = f"Creating resend code for payment with id {payment_id}"
        logging.info(message)
        return self.api_sync_client.create_resend_code(payment_id)

    def get_api_version(self) -> requests.Response:
        logging.info("Getting API version")
        return self.api_sync_client.get_version()

    def get_users(self, user_id: str | None = None) -> requests.Response:
        logging.info("Getting users")
        return self.api_sync_client.get_users(user_id)

    def get_rating_top_users(
        self,
        rating_id: str,
        offset: int = 0,
        limit: int = 10,
        sort: str = "ASC",
    ) -> requests.Response:
        message = f"Getting top users in rating with id {rating_id}"
        logging.info(message)
        params = {"offset": offset, "limit": limit, "sort": sort}
        return self.api_sync_client.get_rating_top_users(rating_id, params=params)

    def get_challenge_top_users(
        self,
        challenge_id: str,
        limit: int = 10,
    ) -> requests.Response:
        message = f"Getting top users in challenge with id {challenge_id}"
        logging.info(message)
        params = {"limit": limit}
        return self.api_sync_client.get_challenge_top_users(challenge_id, params=params)

    def get_user_badges(self, user_id: str) -> requests.Response:
        message = f"Getting badges for user with id {user_id}"
        logging.info(message)
        return self.api_sync_client.get_user_badges(user_id)

    def get_notifications(self) -> requests.Response:
        logging.info("Getting notifications")
        return self.api_sync_client.get_notifications()

    def get_unread_notifications(self, user_id: str | None = None) -> requests.Response:
        message = (
            f"Getting unread notifications for user with id {user_id}"
            if user_id
            else "Getting unread notifications for users"
        )
        logging.info(message)
        return self.api_sync_client.get_unread_notifications(user_id)

    def get_payment(self, payment_id: str) -> requests.Response:
        message = f"Getting payment with id {payment_id}"
        logging.info(message)
        return self.api_sync_client.get_payment(payment_id)
