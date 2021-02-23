import abc
import json
import logging
import sys

import boto3
from aws_lambda_powertools.utilities.batch import BasePartialProcessor
from aws_lambda_powertools.utilities.batch.exceptions import SQSBatchProcessingError
from aws_lambda_powertools.utilities.typing import LambdaContext
from botocore.config import Config
from pydantic import BaseModel

from ..models.sns import SqsSnsNotificationModel
from ..models.sqs import SqsModel, SqsRecordModel
from ...exceptions import BaseFunctionError
from ...handlers import BaseFunctionHandler
from ...typing import Optional, List, Tuple

logger = logging.getLogger(__name__)


class BatchSQSProcessor(BasePartialProcessor):

    def __init__(self, config: Optional[Config] = None, suppress_exception: bool = False, ):
        """
        Initializes sqs client.
        """

        config = config or Config()
        self.client = boto3.client("sqs", config=config)
        self.suppress_exception = suppress_exception

        super().__init__()

    def _get_queue_url(self) -> Optional[str]:
        """
        Format QueueUrl from first records entry
        """
        if not getattr(self, "records", None):
            return

        records_ = self.records[0]

        *_, account_id, queue_name = records_.event_source_arn.split(":")
        return f"{self.client._endpoint.host}/{account_id}/{queue_name}"

    def _get_entries_to_clean(self) -> List:
        """
        Format messages to use in batch deletion
        """
        return [{"Id": msg["messageId"], "ReceiptHandle": msg["receiptHandle"]} for msg in self.success_messages]

    def _process_record(self, record) -> Tuple:
        """
        Process a record with instance's handler
        Parameters
        ----------
        record: Any
            An object to be processed.
        """
        try:
            result = self.handler(record=record)
            return self.success_handler(record=record, result=result)
        except Exception:
            return self.failure_handler(record=record, exception=sys.exc_info())

    def _prepare(self):
        """
        Remove results from previous execution.
        """
        self.success_messages.clear()
        self.fail_messages.clear()

    def _clean(self):
        """
        Delete messages from Queue in case of partial failure.
        """
        # If all messages were successful, fall back to the default SQS -
        # Lambda behaviour which deletes messages if Lambda responds successfully
        if not self.fail_messages:
            logger.debug(f"All {len(self.success_messages)} records successfully processed")
            return

        queue_url = self._get_queue_url()
        entries_to_remove = self._get_entries_to_clean()

        delete_message_response = None
        if entries_to_remove:
            delete_message_response = self.client.delete_message_batch(QueueUrl=queue_url, Entries=entries_to_remove)

        if self.suppress_exception:
            logger.debug(f"{len(self.fail_messages)} records failed processing, but exceptions are suppressed")
        else:
            logger.debug(f"{len(self.fail_messages)} records failed processing, raising exception")
            raise SQSBatchProcessingError(
                msg=f"Not all records processed succesfully. {len(self.exceptions)} individual errors logged "
                    f"separately below.",
                child_exceptions=self.exceptions,
            )

        return delete_message_response


class SqsHandlerMetaClass(abc.ABCMeta):
    def __new__(cls, name, bases, namespace, **kwargs):
        if name != "SqsEventHandler":
            if namespace.get('handle_as_batch') and not namespace.get("handle_record"):
                raise NotImplementedError(f'{name} must implement handle_record(record) if handle_as_batch is True')

        new_cls = super().__new__(cls, name, bases, namespace, **kwargs)
        return new_cls


class SqsEventHandler(BaseFunctionHandler, abc.ABC, metaclass=SqsHandlerMetaClass):
    request_class = SqsModel
    body_class: BaseModel = None
    sns_subscribed: bool = False
    records_class: BaseModel = None
    records = None
    handle_as_batch: bool = False
    batch_processor_handler = BatchSQSProcessor
    batch_aws_config: Config = None

    def __init__(self):
        super(SqsEventHandler, self).__init__()

    @staticmethod
    def __sns_record_serializer__(record: SqsRecordModel):
        sns = json.loads(record.body)
        record.body = sns
        return record

    def __process_handle__(self):
        self.handle(self.request, self.context)

    def __process_response__(self, response):
        return response

    def __serialize_request__(self, request, context):
        if not issubclass(self.request_class, SqsModel):
            raise Exception(f"request must be subclass of {SqsModel.__name__}")

        self.request: SqsModel = self.request_class.parse_obj(request)

        record_class = self.records_class
        self.records: List[record_class.__class__]

        if self.sns_subscribed:
            if self.records_class is not None and not issubclass(self.records_class, SqsSnsNotificationModel):
                raise Exception(f"records_class must be subclass of {SqsSnsNotificationModel.__name__}")
            elif self.records_class is None:
                self.records_class = SqsSnsNotificationModel

            self.records = [self.__sns_record_serializer__(record) for record in self.request.records]

        if self.records_class:
            for i in self.records:
                i.body = self.records_class.parse_obj(i.body)
        else:
            self.records = self.request.records

    def handle(self, request: SqsModel, context: LambdaContext):
        config = self.batch_aws_config or Config()
        if self.handle_as_batch:
            processor = self.batch_processor_handler(config=config)
            with processor(self.records, self.handle_record):
                processor.process()
            return {"statusCode": 200}
        else:
            raise NotImplementedError()

    def handle_error(self, error: BaseFunctionError):
        if self.handle_as_batch:
            return {"statusCode": 200}

        raise error

    def handle_record(self, record):
        ...
