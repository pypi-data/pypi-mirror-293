from __future__ import annotations

from pydantic import BaseModel, Field

from gmfy.constants import LocaleEnum


class BaseAmount(BaseModel):
    value: float = Field(...)
    currency: str = Field(...)


class BaseConfirmation(BaseModel):
    return_url: str = Field(..., alias="returnUrl")


class BasePayment(BaseModel):
    amount: BaseAmount = Field(...)
    confirmation: BaseConfirmation = Field(...)
    user_id: str = Field(..., alias="userId")
    description: str | None = Field(default=None)
    locale: LocaleEnum = Field(default=LocaleEnum.RU)

    class Config:
        populate_by_name = True
