from datetime import datetime
from typing import Optional, Literal, Dict, List

from pydantic import HttpUrl, Field

from ...models import TitleCaseModel


class SnsMsgAttributeModel(TitleCaseModel):
    type: str
    value: str


class BaseSnsNotificationModel(TitleCaseModel):
    subject: Optional[str]
    topic_arn: str
    unsubscribe_url: HttpUrl = Field(alias='UnsubscribeURL')
    type: Literal["Notification"]
    message_attributes: Optional[Dict[str, SnsMsgAttributeModel]]
    message: str
    message_id: str
    timestamp: datetime

    # @root_validator(pre=True)
    # def rewrite_unsubscribe_url(cls, values):
    #     sqs_rewritten_keys = ("UnsubscribeURL",)
    #     if any(key in sqs_rewritten_keys for key in values):
    #         values["unsubscribe_url"] = values.pop("UnsubscribeURL")
    #
    #     return values


class SnsNotificationModel(BaseSnsNotificationModel):
    signing_cert_url: HttpUrl = Field(alias='SigningCertURL')
    signature: str
    signature_version: str

    # @root_validator(pre=True)
    # def rewrite_signing_cert_url(cls, values):
    #     sqs_rewritten_keys = ("SigningCertURL")
    #     if any(key in sqs_rewritten_keys for key in values):
    #         # values["UnsubscribeUrl"] = values.pop("UnsubscribeURL")
    #         values["SigningCertUrl"] = values.pop("SigningCertURL")
    #     return values


class SnsRecordModel(TitleCaseModel):
    event_source: Literal["aws:sns"]
    event_version: str
    event_subscription_arn: str
    sns: SnsNotificationModel


class SnsModel(TitleCaseModel):
    records: List[SnsRecordModel]


SqsSnsNotificationModel = BaseSnsNotificationModel
