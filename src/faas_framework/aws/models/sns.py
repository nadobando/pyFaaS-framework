from datetime import datetime

from pydantic import Field, HttpUrl

from ...models import TitleCaseModel
from ...typing import DataT, Dict, List, Literal, Optional, Union


class SnsMsgAttributeModel(TitleCaseModel):
    type: str  # noqa: VNE003
    value: str


class BaseSnsModel(TitleCaseModel):
    topic_arn: str
    type: Literal["Notification", "SubscriptionConfirmation"]  # noqa: VNE003
    message: Union[str, DataT]
    message_id: str
    timestamp: datetime


class SnsSubscriptionConfirmationModel(BaseSnsModel):
    subscribe_url: HttpUrl = Field(alias="SubscribeURL")
    type: Literal["SubscriptionConfirmation"]  # noqa: VNE003
    token: str
    signing_cert_url: HttpUrl = Field(alias="SigningCertURL")
    signature_version: str
    signature: str


class BaseSnsNotificationModel(BaseSnsModel):
    subject: Optional[str]
    unsubscribe_url: HttpUrl
    type: Literal["Notification"]  # noqa: VNE003
    message_attributes: Optional[Dict[str, SnsMsgAttributeModel]]


class SnsNotificationModel(BaseSnsNotificationModel):
    signing_cert_url: HttpUrl
    signature: str
    signature_version: str


class SnsRecordModel(TitleCaseModel):
    event_source: Literal["aws:sns"]
    event_version: str
    event_subscription_arn: str
    sns: SnsNotificationModel


class SnsModel(TitleCaseModel):
    records: List[SnsRecordModel]


class SqsSnsNotificationModel(BaseSnsNotificationModel):
    unsubscribe_url: HttpUrl = Field(alias="UnsubscribeURL")
