from __future__ import annotations

from pydantic import BaseModel, Field

from gmfy.constants import BaseEventAction, BaseEventType, LocaleEnum


class EventData(BaseModel):
    event_type: BaseEventType = Field(...)
    user_id: str = Field(...)
    event_action: BaseEventAction | None = Field(default=None)
    idempotence_key: str | None = Field(default=None)


class PaymentData(BaseModel):
    amount: dict = Field(...)
    confirmation: dict = Field(...)
    user_id: str = Field(...)
    description: str = Field(default=None)
    locale: LocaleEnum = Field(default=LocaleEnum.RU)
