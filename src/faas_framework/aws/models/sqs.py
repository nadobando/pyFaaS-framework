from datetime import datetime

from pydantic import Field

from ...models import TitleCaseModel, CamelCasedModel
from ...responses import DataT
from ...typing import Literal, Dict, List, Optional, Union


class SqsAttributesModel(TitleCaseModel):
    approximate_receive_count: str
    approximate_first_receiveTimestamp: datetime
    message_deduplication_id: Optional[str]
    message_group_id: Optional[str]
    sender_id: str
    sent_timestamp: datetime
    sequence_number: Optional[str]
    aws_trace_header: Optional[str]


class SqsMsgAttributeModel(CamelCasedModel):
    string_value: Optional[str]
    binary_value: Optional[str]
    string_list_values: List[str] = []
    binary_list_values: List[str] = []
    data_type: str


class SqsRecordModel(CamelCasedModel):
    message_id: str
    receipt_handle: str
    body: Union[str, DataT]
    attributes: SqsAttributesModel
    message_attributes: Optional[Dict[str, SqsMsgAttributeModel]]
    md5_of_body: str
    md5_of_message_attributes: Optional[str]
    event_source: Literal["aws:sqs"]
    event_source_arn: str = Field(alias="eventSourceARN")
    aws_region: str


class SqsModel(TitleCaseModel):
    records: List[SqsRecordModel]
