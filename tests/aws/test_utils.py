from datetime import datetime, timedelta, timezone

import boto3
from botocore.credentials import RefreshableCredentials
from botocore.stub import Stubber

from faas_framework.aws.utils import get_refreshable_aws_assumed_session


def test_get_refreshable_aws_assumed_session():
    sts = boto3.client("sts")

    stubber = Stubber(sts)
    response = {
        "Credentials": {
            "AccessKeyId": "SOMEACCESSKEYFOR",
            "SecretAccessKey": "SOMESECRETACCESSKEY",
            "SessionToken": "string",
            "Expiration": datetime(2015, 1, 1, tzinfo=timezone.utc),
        },
        "AssumedRoleUser": {
            "AssumedRoleId": "string",
            "Arn": "SOMEASSUMEDROLEARNFORTEST",
        },
        "PackedPolicySize": 123,
    }
    role_arn = "arn:iam:us-east-1:role/SOME-ROLE_TEST"

    expected_params = dict(
        RoleArn=role_arn, RoleSessionName="role-session-name", ExternalId="external-id"
    )

    stubber.add_response(
        "assume_role", response, expected_params
    )  # call with expired time
    response["Credentials"]["Expiration"] = datetime.now(tz=timezone.utc) + timedelta(
        hours=2
    )  # call future expiration
    stubber.add_response("assume_role", response, expected_params)
    stubber.activate()

    session = get_refreshable_aws_assumed_session(sts, **expected_params)
    credentials = session.get_credentials()
    assert type(credentials) is RefreshableCredentials
    assert credentials.access_key is response["Credentials"]["AccessKeyId"]
    assert credentials.secret_key is response["Credentials"]["SecretAccessKey"]

    stubber.deactivate()
