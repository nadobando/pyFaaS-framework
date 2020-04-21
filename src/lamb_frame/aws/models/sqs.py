from datetime import datetime
from typing import Dict, List, Optional

from pydantic import Field

from ...models import TitleCaseModel, CamelCasedModel
from ...typing import Literal


class SqsAttributesModel(TitleCaseModel):
    approximate_receive_count: str
    approximate_first_receiveTimestamp: datetime
    message_deduplication_id: Optional[str]
    message_group_id: Optional[str]
    sender_id: str
    sent_timestamp: datetime
    sequence_number: Optional[str]
    aws_trace_header: Optional[str]


class SqsMsgAttributeModel(TitleCaseModel):
    string_value: Optional[str]
    binary_value: Optional[str]
    string_list_values: List[str] = []
    binary_list_values: List[str] = []
    data_type: str

    # context on why it's commented: https://github.com/awslabs/aws-lambda-powertools-python/pull/118
    # Amazon SQS supports the logical data types String, Number, and Binary with optional custom data type
    # labels with the format .custom-data-type.
    # https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-message-metadata.html#sqs-message-attributes
    # @validator("dataType")
    # def valid_type(cls, v):  # noqa: VNE001,E800 # noqa: E800
    #     pattern = re.compile("Number.*|String.*|Binary.*") # noqa: E800
    #     if not pattern.match(v): # noqa: E800
    #         raise TypeError("data type is invalid") # noqa: E800
    #     return v # noqa: E800
    #
    # # validate that dataType and value are not None and match
    # @root_validator
    # def check_str_and_binary_values(cls, values): # noqa: E800
    #     binary_val, str_val = values.get("binaryValue", ""), values.get("stringValue", "") # noqa: E800
    #     data_type = values.get("dataType") # noqa: E800
    #     if not str_val and not binary_val: # noqa: E800
    #         raise TypeError("both binaryValue and stringValue are missing") # noqa: E800
    #     if data_type.startswith("Binary") and not binary_val: # noqa: E800
    #         raise TypeError("binaryValue is missing") # noqa: E800
    #     if (data_type.startswith("String") or data_type.startswith("Number")) and not str_val: # noqa: E800
    #         raise TypeError("stringValue is missing") # noqa: E800
    #     return values # noqa: E800


class SqsRecordModel(CamelCasedModel):
    message_id: str
    receipt_handle: str
    body: str
    attributes: SqsAttributesModel
    message_attributes: Optional[Dict[str, SqsMsgAttributeModel]]
    md5_of_body: str
    md5_of_message_attributes: Optional[str]
    event_source: Literal["aws:sqs"]
    event_source_arn: str = Field(alias="eventSourceARN")
    aws_region: str


class SqsModel(TitleCaseModel):
    records: List[SqsRecordModel]
