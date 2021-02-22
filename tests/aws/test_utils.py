from datetime import datetime

from botocore.credentials import RefreshableCredentials
from botocore.session import get_session
from botocore.stub import Stubber
from pytest_mock import MockerFixture

from faas_framework.aws.utils import get_refreshable_aws_assumed_session


def test_get_refreshable_aws_assumed_session(mocker: MockerFixture):
    sts = get_session().create_client('sts')
    stubber = Stubber(sts)
    response = {
        'Credentials': {
            'AccessKeyId': 'SOMEACCESSKEYFORTEST'[:16],
            'SecretAccessKey': 'SOMESECRETACCESSKEY',
            'SessionToken': 'string',
            'Expiration': datetime(2015, 1, 1)
        },
        'AssumedRoleUser': {
            'AssumedRoleId': 'string',
            'Arn': 'SOMEASSUMEDROLEARNFORTEST'
        },
        'PackedPolicySize': 123
    }
    role_arn = "arn:iam:us-east-1:role/SOME-ROLE_TEST"

    expected_params = dict(RoleArn=role_arn,
                           RoleSessionName="role-session-name",
                           ExternalId='external-id')

    stubber.add_response('assume_role', response, expected_params)
    stubber.activate()

    session = get_refreshable_aws_assumed_session(sts, RoleArn=role_arn,
                                                  RoleSessionName="role-session-name",
                                                  ExternalId="external-id")
    assert type(session.get_credentials()) is RefreshableCredentials
