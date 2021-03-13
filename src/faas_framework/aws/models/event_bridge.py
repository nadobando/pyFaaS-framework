from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


def event_bridge_alias_generator(field: str) -> str:
    return field.replace("_", "-")


class EventBridgeModel(BaseModel):
    version: str
    id: str
    source: str
    account: str
    time: datetime
    region: str
    resources: List[str]
    detail_type: str
    detail: Dict[str, Any]
    replay_name: Optional[str]

    class Config:
        alias_generator = event_bridge_alias_generator
