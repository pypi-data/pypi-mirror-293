from importlib.metadata import PackageNotFoundError, version

from gmfy.base_events import BaseActionEvent, BaseEvent, BaseUniqueEvent
from gmfy.base_payment import BaseAmount, BaseConfirmation, BasePayment
from gmfy.constants import BaseEventAction, BaseEventType, LocaleEnum
from gmfy.data import EventData, PaymentData

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = None  # type: ignore[assignment]

__all__ = (
    "BaseEventAction",
    "BaseEventType",
    "BaseEvent",
    "BaseActionEvent",
    "BaseUniqueEvent",
    "LocaleEnum",
    "BasePayment",
    "BaseAmount",
    "BaseConfirmation",
    "EventData",
    "PaymentData",
)
