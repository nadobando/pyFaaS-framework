from faas_framework.aws.models.sns import SnsModel, SqsSnsNotificationModel


def test_sns_model(sns_event_dict):
    SnsModel(**sns_event_dict)


def test_sqs_sns_notification_model(sqs_sns_event_dict):
    SqsSnsNotificationModel(**sqs_sns_event_dict)
