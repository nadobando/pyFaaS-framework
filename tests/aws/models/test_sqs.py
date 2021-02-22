from faas_framework.aws.models.sqs import SqsModel


def test_sqs_model(sqs_event_dict):
    SqsModel(**sqs_event_dict)
    # assert False
