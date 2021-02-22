from unittest.mock import call, MagicMock

import pytest
from aws_lambda_powertools.utilities.batch.exceptions import SQSBatchProcessingError
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import create_model
from pytest_mock import MockerFixture

from faas_framework.aws.handlers.sqs import SqsEventHandler
from faas_framework.aws.models.sqs import SqsModel


class MySqsEventSuccessHandler(SqsEventHandler):

    def handle(self, request: SqsModel, context: LambdaContext):
        pass


class MySqsEventFailureHandler(SqsEventHandler):

    def handle(self, request: SqsModel, context: LambdaContext):
        raise Exception('Test exception')


class MyBatchSqsEventSuccessHandler(SqsEventHandler):
    handle_as_batch = True

    def handle_record(self, *args, **kwargs):
        print(args)
        print("*" * 100)


class MyBatchSqsEventFailureHandler(SqsEventHandler):
    handle_as_batch = True

    def handle_record(self, *args, **kwargs):
        raise Exception('Test exception')


class MySnsSqsEventSuccessHandler(SqsEventHandler):
    sns_subscribed = True

    def handle(self, request: SqsModel, context: LambdaContext):
        pass


class MySnsSqsEventFailureHandler(SqsEventHandler):
    handle_as_batch = True
    sns_subscribed = True

    def handle_record(self, *args, **kwargs):
        raise Exception('Test exception')


class MySnsSqsEventBadRecordClassHandler(SqsEventHandler):
    sns_subscribed = True
    records_class = create_model('NotSqsSnsNotificationModel')

    def handle_record(self, *args, **kwargs):
        raise Exception('Test exception')


class NotSqsModelHandler(SqsEventHandler):
    request_class = create_model("NotSqsModel")


class MySqsEventNotImplementedHandler(SqsEventHandler):
    handle_as_batch = False


# noinspection PyUnresolvedReferences
@pytest.mark.parametrize('handler,event', [
    (MySqsEventSuccessHandler, pytest.lazy_fixture('sqs_event_dict')),
    (MySnsSqsEventSuccessHandler, pytest.lazy_fixture('sns_sqs_event_dict')),
])
def test_handle(handler, event, lambda_context):
    handler = handler()
    # noinspection PyTypeChecker
    handler(event, lambda_context)
    assert type(handler.request) is SqsModel
    assert handler.records


# noinspection DuplicatedCode
exception_calls = [
    (Exception, MySqsEventSuccessHandler),
    (SQSBatchProcessingError, MyBatchSqsEventFailureHandler),
    (Exception, NotSqsModelHandler),
    (NotImplementedError, MySqsEventNotImplementedHandler),
    (Exception, MySnsSqsEventBadRecordClassHandler)
]


@pytest.mark.parametrize('exc,handler', exception_calls)
def test_handle_error(exc, handler, sqs_event_dict, lambda_context):
    try:
        handler()(sqs_event_dict, lambda_context)
    except Exception as e:
        assert type(e) is exc, f"exception not as expected: {str(e)}"


def test_handle_record(sqs_event_dict, lambda_context, mocker: MockerFixture):
    mocker.patch.object(MyBatchSqsEventSuccessHandler, 'handle_record')
    handler = MyBatchSqsEventSuccessHandler()
    # noinspection PyTypeHints
    handler.handle_record: MagicMock
    model = SqsModel(**sqs_event_dict)
    calls = [call(record=x) for x in model.records]
    handler(sqs_event_dict, lambda_context)
    handler.handle_record.assert_has_calls(calls)


def test_batch_is_not_implemented(sqs_event_dict, lambda_context):
    with pytest.raises(NotImplementedError):
        # noinspection PyUnusedLocal
        class MyBatchSqsEventNotImplementedHandler(SqsEventHandler):
            handle_as_batch = True
