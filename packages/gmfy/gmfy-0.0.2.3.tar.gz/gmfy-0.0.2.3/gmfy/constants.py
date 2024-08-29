from enum import StrEnum


class BaseEventType(StrEnum):
    """
    --- Event type ---

    Example:

    subscription = "subscription"
    subscriber = "subscriber"
    vote = "vote"
    register = "register"
    """


class BaseEventAction(StrEnum):
    """
    --- Event Actions ---

    Example:

    create = "create"
    remove = "remove"
    update = "update"
    delete = "delete"
    """


class LocaleEnum(StrEnum):
    """
    --- Local Enum to determine the payment locale. Not overridden ---
    """

    RU = "RU"
    EN = "EN"
