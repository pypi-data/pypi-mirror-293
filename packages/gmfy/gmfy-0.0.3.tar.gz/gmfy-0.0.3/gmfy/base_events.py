from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
)
from pydantic.alias_generators import to_camel

from gmfy.constants import BaseEventAction, BaseEventType


class BaseEvent(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
        children_list=[],  # type: ignore[typeddict-unknown-key]
    )

    user_id: str
    event_type: BaseEventType

    def __init_subclass__(cls, **kwargs: Any) -> None:
        if not cls.__name__.startswith("Base"):
            cls.model_config["children_list"].append(cls)  # type: ignore[typeddict-item]
        return super().__init_subclass__(**kwargs)

    @computed_field()
    def type(self) -> str:
        return self.event_type

    @property
    def is_ready(self) -> bool:
        return True


class BaseActionEvent(BaseEvent):
    event_action: BaseEventAction = Field(exclude=True)

    @computed_field()
    def type(self) -> str:
        return f"{self.event_action}_{self.event_type}"


class BaseUniqueEvent(BaseEvent):
    idempotence_key: str
