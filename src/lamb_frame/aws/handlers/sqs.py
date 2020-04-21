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

from ..models.sns import BaseSnsNotificationModel
from ..models.sqs import SqsModel, SqsRecordModel
from ...exceptions import BaseLambdaError
from ...handlers import BaseFunctionHandler
from ...responses import Response
from ...typing import Optional, List, Tuple

logger = logging.getLogger(__name__)


class BatchSQSProcessor(BasePartialProcessor):

    def __init__(self, config: Optional[Config] = None, suppress_exception: bool = False,
                 sns_subscription=False):
        """
        Initializes sqs client.
        """

        config = config or Config()
        self.sns_subscription = sns_subscription
        self.client = boto3.client("sqs", config=config)
        self.suppress_exception = suppress_exception

        super().__init__()

    def _get_queue_url(self) -> Optional[str]:
        """
        Format QueueUrl from first records entry
        """
        if not getattr(self, "records", None):
            return

        # pprint(self.records[0].__dict__)

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
            result = self.handler(record=record.body)
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


class SqsEventHandler(BaseFunctionHandler, abc.ABC):
    request_class = SqsModel
    body_class: BaseModel = None
    sns_subscripted: bool = False
    records_class: BaseModel = None
    records = None
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

    def __serialize_request__(self, request, context):
        if not issubclass(self.request_class, SqsModel):
            raise Exception(f"request must be subclass of {SqsModel.__name__}")

        self.request: SqsModel = self.request_class.parse_obj(request)

        record_class = self.records_class
        self.records: List[record_class.__class__]

        if self.sns_subscripted:
            if self.records_class is not None and not issubclass(self.records_class, BaseSnsNotificationModel):
                raise Exception(f"records_class must be subclass of {BaseSnsNotificationModel.__name__}")
            elif self.records_class is None:
                self.records_class = BaseSnsNotificationModel

            self.records = [self.__sns_record_serializer__(record) for record in self.request.records]

        if self.records_class:
            for i in self.records:
                i.body = self.records_class.parse_obj(i.body)

    def handle(self, request: SqsModel, context: LambdaContext):
        config = self.batch_aws_config or Config()
        processor = self.batch_processor_handler(config=config, sns_subscription=self.sns_subscripted)
        with processor(self.records, self.handle_record):
            processor.process()

    def handle_error(self, error: BaseLambdaError) -> Response:
        return self.response_class(status_code=500)

    @abc.abstractmethod
    def handle_record(self, *args, **kwargs):
        ...
