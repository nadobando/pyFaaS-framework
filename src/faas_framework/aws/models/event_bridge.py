from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


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
        alias_generator = lambda x: x.replace('_', '-')
