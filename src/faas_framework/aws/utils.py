import boto3
from boto3 import Session
from botocore.credentials import RefreshableCredentials
from botocore.session import get_session


# noinspection PyUnresolvedReferences
def get_refreshable_aws_assumed_session(sts: 'STS' = None, **kwargs) -> Session:
    sts_client = sts or boto3.client('sts')

    def refresh():
        """Refresh tokens by calling assume_role again """
        response = sts_client.assume_role(**kwargs).get("Credentials")
        _credentials = {
            "access_key": response.get("AccessKeyId"),
            "secret_key": response.get("SecretAccessKey"),
            "token": response.get("SessionToken"),
            "expiry_time": response.get("Expiration").isoformat(),
        }
        return _credentials

    credentials = refresh()
    refreshable_credentials = RefreshableCredentials.create_from_metadata(credentials, refresh, "sts-assume-role")
    core_session = get_session()
    core_session._credentials = refreshable_credentials
    return Session(botocore_session=core_session)

# class AssumableSession:
#     __sts = boto3.client('sts')
#
#     def __init__(self, role_arn: str, role_session_name: str, policy: str = None,
#                  duration_seconds=900,
#                  tags: List[Dict[str, str]] = None,
#                  transitive_tag_keys: List[str] = None,
#                  external_id: str = None,
#                  serial_number: str = None,
#                  token_code: str = None
#                  ):
#         self.__role_arn = role_arn
#         self.__role_session_name = role_session_name
#         self.__policy = policy
#         self.__duration_seconds = duration_seconds
#         self.__tags = tags
#         self.__transitive_tag_keys = transitive_tag_keys
#         self.__external_id = external_id
#         self.__serial_number = serial_number
#         self.__token_code = token_code
#
#     def __get_session(self):
#         """ Refresh tokens by calling assume_role again """
#         kwargs = {k: v for k, v in dict(
#             RoleArn=self.__role_arn,
#             RoleSessionName=self.__role_session_name,
#             Policy=self.__policy,
#             DurationSeconds=self.__duration_seconds,
#             Tags=self.__tags,
#             TransitiveTagKeys=self.__transitive_tag_keys,
#             ExternalId=self.__external_id,
#             SerialNumber=self.__serial_number,
#             TokenCode=self.__token_code
#         ).items() if v is not None}
#
#         response = self.__sts.assume_role(**kwargs).get("Credentials")
#         _credentials = {
#             "access_key": response.get("AccessKeyId"),
#             "secret_key": response.get("SecretAccessKey"),
#             "token": response.get("SessionToken"),
#             "expiry_time": response.get("Expiration").isoformat(),
#         }
#         return _credentials
#
#     def assume(self) -> Session:
#         credentials = self.__get_session()
#         pprint(credentials)
#         refreshable_credentials = RefreshableCredentials.create_from_metadata(
#             credentials,
#             get_session,
#             "sts-assume-role"
#         )
#         core_session = get_session()
#         core_session._credentials = refreshable_credentials
#         return Session(botocore_session=core_session)
