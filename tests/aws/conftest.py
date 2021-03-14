import pytest


@pytest.fixture
def sqs_sns_event_dict():
    return {
        "Type": "Notification",
        "MessageId": "92bb8248-4cd4-5c14-bf93-daeea52ca612",
        "SequenceNumber": "10000000000000000152",
        "TopicArn": "arn:aws:sns:us-east-1:000000000000:testTopic.fifo",
        "Message": "",
        "Timestamp": "2021-02-17T09:54:00.108Z",
        "UnsubscribeURL": "https://unsubuscribe-url.com",
        "MessageAttributes": {},
    }


@pytest.fixture
def sns_event_dict():
    return {
        "Records": [
            {
                "EventVersion": "1.0",
                "EventSubscriptionArn": "arn:aws:sns:us-east-2:123456789012:sns-la ...",
                "EventSource": "aws:sns",
                "Sns": {
                    "SignatureVersion": "1",
                    "Timestamp": "2019-01-02T12:45:07.000Z",
                    "Signature": "tcc6faL2yUC6dgZdmrwh1Y4cGa/ebXEkAi6RibDsvpi+tE/1+82j...65r==",
                    "SigningCertUrl": "https://sns.us-east-2.amazonaws.com/SimpleNotification",
                    "MessageId": "95df01b4-ee98-5cb9-9903-4c221d41eb5e",
                    "Message": "Hello from SNS!",
                    "MessageAttributes": {
                        "Test": {"Type": "String", "Value": "TestString"},
                        "TestBinary": {"Type": "Binary", "Value": "TestBinary"},
                    },
                    "Type": "Notification",
                    "UnsubscribeUrl": "https://sns.us-east-2.amazonaws.com/?Action=Unsubscribe",
                    "TopicArn": "arn:aws:sns:us-east-2:123456789012:sns-lambda",
                    "Subject": "TestInvoke",
                },
            }
        ]
    }


@pytest.fixture
def sqs_event_dict():
    return {
        "Records": [
            {
                "messageId": "059f36b4-87a3-44ab-83d2-661975830a7d",
                "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a...",
                "body": "Test message.",
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1545082649183",
                    "SenderId": "AIDAIENQZJOLO23YVJ4VO",
                    "ApproximateFirstReceiveTimestamp": "1545082649185",
                },
                "messageAttributes": {
                    "testAttr": {
                        "stringValue": "100",
                        "binaryValue": "base64Str",
                        "dataType": "Number",
                    }
                },
                "md5OfBody": "e4e68fb7bd0e697a0ae8f1bb342846b3",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:us-east-2:123456789012:my-queue",
                "awsRegion": "us-east-2",
            },
            {
                "messageId": "2e1424d4-f796-459a-8184-9c92662be6da",
                "receiptHandle": "AQEBzWwaftRI0KuVm4tP+/7q1rGgNqicHq...",
                "body": "Test message2.",
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1545082650636",
                    "SenderId": "AIDAIENQZJOLO23YVJ4VO",
                    "ApproximateFirstReceiveTimestamp": "1545082650649",
                },
                "messageAttributes": {},
                "md5OfBody": "e4e68fb7bd0e697a0ae8f1bb342846b3",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:us-east-2:123456789012:my-queue",
                "awsRegion": "us-east-2",
            },
        ]
    }


@pytest.fixture
def api_gw_event_dict_str_body():
    return {
        "version": "1.0",
        "resource": "/my/path",
        "path": "/my/path",
        "httpMethod": "GET",
        "headers": {"Header1": "value1", "Header2": "value2"},
        "multiValueHeaders": {"Header1": ["value1"], "Header2": ["value1", "value2"]},
        "queryStringParameters": {"parameter1": "value1", "parameter2": "value"},
        "multiValueQueryStringParameters": {
            "parameter1": ["value1", "value2"],
            "parameter2": ["value"],
        },
        "requestContext": {
            "accountId": "123456789012",
            "apiId": "id",
            "authorizer": {"claims": None, "scopes": None},
            "domainName": "id.execute-api.us-east-1.amazonaws.com",
            "domainPrefix": "id",
            "extendedRequestId": "request-id",
            "httpMethod": "GET",
            "identity": {
                "accessKey": None,
                "accountId": None,
                "caller": None,
                "cognitoAuthenticationProvider": None,
                "cognitoAuthenticationType": None,
                "cognitoIdentityId": None,
                "cognitoIdentityPoolId": None,
                "principalOrgId": None,
                "sourceIp": "IP",
                "user": None,
                "userAgent": "user-agent",
                "userArn": None,
            },
            "path": "/my/path",
            "protocol": "HTTP/1.1",
            "requestId": "id=",
            "requestTime": "04/Mar/2020:19:15:17 +0000",
            "requestTimeEpoch": 1583349317135,
            "resourceId": None,
            "resourcePath": "/my/path",
            "stage": "$default",
        },
        "pathParameters": None,
        "stageVariables": None,
        "body": "Hello from Lambda!",
        "isBase64Encoded": False,
    }


@pytest.fixture
def api_gw_event_dict_json_body():
    return {
        "version": "1.0",
        "resource": "/my/{param}",
        "path": "/my/test-param",
        "httpMethod": "GET",
        "headers": {
            "Header1": "value1",
            "Header2": "value2",
            "Content-Type": "application/json",
        },
        "multiValueHeaders": {
            "Header1": ["value1"],
            "Header2": ["value1", "value2"],
            "Content-Type": ["application/json"],
        },
        "queryStringParameters": {"parameter1": "value2", "parameter2": "value3"},
        "multiValueQueryStringParameters": {
            "parameter1": ["value1", "value2"],
            "parameter2": ["value3"],
        },
        "requestContext": {
            "accountId": "123456789012",
            "apiId": "id",
            "authorizer": {"claims": None, "scopes": None},
            "domainName": "id.execute-api.us-east-1.amazonaws.com",
            "domainPrefix": "id",
            "extendedRequestId": "request-id",
            "httpMethod": "GET",
            "identity": {
                "accessKey": None,
                "accountId": None,
                "caller": None,
                "cognitoAuthenticationProvider": None,
                "cognitoAuthenticationType": None,
                "cognitoIdentityId": None,
                "cognitoIdentityPoolId": None,
                "principalOrgId": None,
                "sourceIp": "IP",
                "user": None,
                "userAgent": "user-agent",
                "userArn": None,
            },
            "path": "/my/path",
            "protocol": "HTTP/1.1",
            "requestId": "id=",
            "requestTime": "04/Mar/2020:19:15:17 +0000",
            "requestTimeEpoch": 1583349317135,
            "resourceId": None,
            "resourcePath": "/my/path",
            "stage": "$default",
        },
        "pathParameters": {"param": "test-param"},
        "stageVariables": None,
        "body": '{"customerId": "6e83612e-4b68-4a0a-aadb-53a5bbce7c7f"}',
        "isBase64Encoded": False,
    }


@pytest.fixture
def api_gw_event_dict_json_base64_body(api_gw_event_dict_json_body):
    api_gw_event_dict_json_body[
        "body"
    ] = "eyJjdXN0b21lcklkIjogIjZlODM2MTJlLTRiNjgtNGEwYS1hYWRiLTUzYTViYmNlN2M3ZiJ9"
    api_gw_event_dict_json_body["isBase64Encoded"] = True
    return api_gw_event_dict_json_body


@pytest.fixture
def api_gw_event_dict_with_base64():
    return {
        "resource": "/",
        "path": "/",
        "httpMethod": "POST",
        "headers": {
            "Accept": "application/json, application/cbor, application/*+json",
            "Accept-Encoding": "gzip,deflate",
            "Authorization": "[Sensitive Data]",
            "Content-Type": "multipart/form-data;charset=UTF-8;boundary=IF8lzvn2hY5VhW9gPR09x_b1J384sCT0",
            "Host": "xxx.yyy.com",
            "User-Agent": "Apache-HttpClient/4.5.8 (Java/11.0.2)",
            "X-Amzn-Trace-Id": "Root=1-602c57ba-7d2074e51d075f6d2395a205",
            "X-Forwarded-For": "1.1.1.1",
            "X-Forwarded-Port": "443",
            "X-Forwarded-Proto": "https",
        },
        "multiValueHeaders": {
            "Accept": ["application/json, application/cbor, application/*+json"],
            "Accept-Encoding": ["gzip,deflate"],
            "Authorization": ["[Sensitive Data]"],
            "Content-Type": [
                "multipart/form-data;charset=UTF-8;boundary=IF8lzvn2hY5VhW9gPR09x_b1J384sCT0"
            ],
            "Host": ["xxx.yyy.com"],
            "User-Agent": ["Apache-HttpClient/4.5.8 (Java/11.0.2)"],
            "X-Amzn-Trace-Id": ["Root=1-602c57ba-7d2074e51d075f6d2395a205"],
            "X-CORRELATION-ID": ["c6a531cd-01fa-44af-8d41-5c994b46a91b"],
            "X-Forwarded-For": ["1.1.1.1"],
            "X-Forwarded-Port": ["443"],
            "X-Forwarded-Proto": ["https"],
        },
        "queryStringParameters": None,
        "multiValueQueryStringParameters": None,
        "pathParameters": {"customerId": "009530a5-e51e-4574-a795-39a33f210ac4"},
        "stageVariables": None,
        "requestContext": {
            "resourceId": "ko4tra",
            "authorizer": {
                "ConsoleInternalToken": "",
                "principalId": "principal",
                "correlationId": "21D9DF00536F46ECABC7D923A89E5D22",
                "integrationLatency": 65,
            },
            "resourcePath": "/",
            "httpMethod": "POST",
            "extendedRequestId": "a3KlGGNKIAMFj9g=",
            "requestTime": "16/Feb/2021:23:39:38 +0000",
            "path": "/",
            "accountId": "086285707022",
            "protocol": "HTTP/1.1",
            "stage": "master",
            "domainPrefix": "master",
            "requestTimeEpoch": 1613518778109,
            "requestId": "7609fa54-efd9-4cc2-8311-c35f5696f119",
            "identity": {
                "cognitoIdentityPoolId": None,
                "accountId": None,
                "cognitoIdentityId": None,
                "caller": None,
                "sourceIp": "1.1.1.1",
                "principalOrgId": None,
                "accessKey": None,
                "cognitoAuthenticationType": None,
                "cognitoAuthenticationProvider": None,
                "userArn": None,
                "userAgent": "Apache-HttpClient/4.5.8 (Java/11.0.2)",
                "user": None,
            },
            "domainName": "xxx.yyy.com",
            "apiId": "vxv7hbixe4",
        },
        "body": "LS1JRjhsenZuMmhZNVZoVzlnUFIwOXhfYjFKMzg0c0NUMA0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJmaWxlcyI7IGZpbGVuYW1lPSJjZXJ0LXRleHQucGVtIg0KQ29udGVudC1UeXBlOiBhcHBsaWNhdGlvbi9vY3RldC1zdHJlYW0NCkNvbnRlbnQtTGVuZ3RoOiAxMTE5DQoNCi0tLS0tQkVHSU4gQ0VSVElGSUNBVEUtLS0tLQpNSUlERERDQ0FmU2dBd0lCQWdJREFRQWdNQTBHQ1NxR1NJYjNEUUVCQlFVQU1ENHhDekFKQmdOVkJBWVRBbEJNCk1Sc3dHUVlEVlFRS0V4SlZibWw2WlhSdklGTndMaUI2SUc4dWJ5NHhFakFRQmdOVkJBTVRDVU5sY25SMWJTQkQKUVRBZUZ3MHdNakEyTVRFeE1EUTJNemxhRncweU56QTJNVEV4TURRMk16bGFNRDR4Q3pBSkJnTlZCQVlUQWxCTQpNUnN3R1FZRFZRUUtFeEpWYm1sNlpYUnZJRk53TGlCNklHOHVieTR4RWpBUUJnTlZCQU1UQ1VObGNuUjFiU0JEClFUQ0NBU0l3RFFZSktvWklodmNOQVFFQkJRQURnZ0VQQURDQ0FRb0NnZ0VCQU02eHdTN1RUM3pOSmM0WVBrL0UKakcrQWFuUElXMUg0bTlMY3V3QmNzYUQ4ZFFQdWdmQ0k3aU5TNmVZVk00MnNMUW5GZHZrck9ZQ0o1SmRMa0tXbwplUGh6UTN1a1liRFlXTXpoYkdaK25QTUpYbFZqaE5XbzcvT3hMakJvczhRODJLeHVqWmxha0U0MDNEYWFqNEdJClVMZHRsa0lKODllVmd3MUJTN0JxYS9qOEQzNWluMmZFN1NaZkVDWVBDRS93cEZjb3pvKzQ3VVgyYnU0bFhhcHUKT2I3a2t5L1pSNkJ5Ni9xbVc2L0tVei9pRHNhV1ZoRnU5K2xtcVNiWWY1VlQ3UXFGaUxwUEthVkNqRjYyL0lVZwpBS3BvQzZFYWhRR2N4RVpqZ29pMklySHUvcXBHV1g3UE5TelZ0dHBkOTBnekZGUzI2OWx2enMySTFxc2IycFk3CkhWa0NBd0VBQWFNVE1CRXdEd1lEVlIwVEFRSC9CQVV3QXdFQi96QU5CZ2txaGtpRzl3MEJBUVVGQUFPQ0FRRUEKdUkzTzcrY1V1cy91c0VTU2JMUTVQcUtFYnEyNElYZlMxSGVDaCtZZ1FZSHU0dmdSdDJQUkZ6ZStHWFlrSEFRYQpUT3M5cW1kdkxkVE4vbVV4Y01VYnBnSUt1bUI3YlZqQ21rbitZeklMYStNNndLeXJPN0RvMHdsUmpCQ0R4alRnCnhTdmdHclpnRkNkc01uZU12TEp5bU0vTnpEKzV5Q1JDRk5aWC9PWW1RNmtkNVlDUXpnTlVLRDczUDlQNFRlMXEKQ2pxVEU1czdGQ01UWTV3LzBZY25lZVZNVWVNQnJZVmRHanV4MVhNUXBOUHl2RzVrOVZwV2tLakhEa3gwRHk1eApPL2ZJUi9ScGJ4WHlFVjZESHB4OFVxNzlBdG9TcUZsbkdOdThjTjJic1dudGdNNkpRRWhxRGpYS0tXWVZJWlFzCjZHQXFtNFZLUVBOcmlpVHNCaFlzY3c9PQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg0KLS1JRjhsenZuMmhZNVZoVzlnUFIwOXhfYjFKMzg0c0NUMA0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJmaWxlcyI7IGZpbGVuYW1lPSJjZXJ0LWJpbmFyeS5jZXIiDQpDb250ZW50LVR5cGU6IGFwcGxpY2F0aW9uL29jdGV0LXN0cmVhbQ0KQ29udGVudC1MZW5ndGg6IDk1OA0KDQowggO6MIICoqADAgECAhApu3EhXSUhp0y0ywnW65GNMA0GCSqGSIb3DQEBCwUAMGExEzARBgoJkiaJk/IsZAEZFgNjb20xHjAcBgoJkiaJk/IsZAEZFg5wcmVwcm9kMTAtMTAtNDEqMCgGA1UEAxMhcHJlcHJvZDEwLTEwLTQtRUMyQU1BWi1QVUdHSDNMLUNBMB4XDTIwMDMyOTA0NTUwM1oXDTMwMDMyOTA1MDUwM1owLTErMCkGA1UEAwwiRUMyQU1BWi1QVUdHSDNMLnByZXByb2QxMC0xMC00LmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAMb1EHNHku3AAhRtsUHTj5MGPQh/qIwFHrvBgkgCLrhFLuRkduZl/VxEXixYZQZY52xITKiXSc1Sxnz5ziELGoVmrnQISNpf64Lxm8rWkYoaOsZdzHwDFBeRRlPqGhSipYAUBerlXxkvnQ1shb31guFDPNdPA1RYBbtJb70lQn+XGdJIr2f+NK6L7a1i60VLH7AsfaqEj2xPc5E+01ggnMU0FajcIvjUUMHXnNjJgRgrWrrSTzMhylHhetmqhqRkdlaHXhWczTAdNCh91/Gqk3/DQYFfZEkD6xm0p0h9xI9rfWchj8JWDafS/fuHwtrgGMVECa8R1rmrTnJlcWBH9uMCAwEAAaOBoTCBnjAOBgNVHQ8BAf8EBAMCBaAwHQYDVR0lBBYwFAYIKwYBBQUHAwIGCCsGAQUFBwMBMC0GA1UdEQQmMCSCIkVDMkFNQVotUFVHR0gzTC5wcmVwcm9kMTAtMTAtNC5jb20wHwYDVR0jBBgwFoAUSbUK8+rZZDhvuIiGbPjl/uFsGfowHQYDVR0OBBYEFCHSfC/iG1PGOou09fCFSTKoJaW7MA0GCSqGSIb3DQEBCwUAA4IBAQBtX3yMtrYF/GfVOYaTee0+tMmNpz7o4a/On3b97OgSHe+Z9USoPNtrAKciosy6k6l8p90jdfR0P16gYwDYRlp90lobB7TW1JggonqFAkl1Uo50V4RkT44HnIEX9xQDxEW2Arbs+OwiRQO2S2vFkio5lTlAzuw6isL5T+ERkrApI+ALoLgp0VYmA/5wkA0Tc7CaHUB7daLIiujCAjdkx5DYLKk/4GiR5hf2vU2PxWyq230uEACxtFvY23AZ+uHC9uHTv5hGGqMxYJS8gyofAFEuh7UQSJAFPtUVRWzPBBIoXdCFtK1frTWCsf27iSjlj3O/xW/+aHgpGW52ycis1IdFDQotLUlGOGx6dm4yaFk1VmhXOWdQUjA5eF9iMUozODRzQ1QwLS0NCg==",  # noqa: E501
        "isBase64Encoded": True,
    }


@pytest.fixture
def sns_sqs_event_dict():
    return {
        "Records": [
            {
                "messageId": "79406a00-bf15-46ca-978c-22c3613fcb30",
                "receiptHandle": "AQEB3fkqlBqq239bMCAHIr5mZkxJYKtxsTTy1lMImmpY7zqpQdfcAE8zFiuRh7X5ciROy24taT2rRXfuJFN/yEUVcQ6d5CIOCEK4htmRJJOHIyGdZPAm2NUUG5nNn2aEzgfzVvrkPBsrCbr7XTzK5s6eUZNH/Nn9AJtHKHpzweRK34Bon9OU/mvyIT7EJbwHPsdhL14NrCp8pLWBiIhkaJkG2G6gPO89dwHtGVUARJL+zP70AuIu/f7QgmPtY2eeE4AVbcUT1qaIlSGHUXxoHq/VMHLd/c4zWl0EXQOo/90DbyCUMejTIKL7N15YfkHoQDHprvMiAr9S75cdMiNOduiHzZLg/qVcv4kxsksKLFMKjwlzmYuQYy2KslVGwoHMd4PD",  # noqa: E501
                "body": '{\n  "Type" : "Notification",\n  "MessageId" : "d88d4479-6ec0-54fe-b63f-1cf9df4bb16e",\n  "TopicArn" : "arn:aws:sns:eu-west-1:231436140809:powertools265",\n  "Message" : "{\\"message\\": \\"hello world\\", \\"username\\": \\"lessa\\"}",\n  "Timestamp" : "2021-01-19T10:07:07.287Z",\n  "SignatureVersion" : "1",\n  "Signature" : "tEo2i6Lw6/Dr7Jdlulh0sXgnkF0idd3hqs8QZCorQpzkIWVOuu583NT0Gv0epuZD1Bo+tex6NgP5p6415yNVujGHJKnkrA9ztzXaVgFiol8rf8AFGQbmb7RsM9BqATQUJeg9nCTe0jksmWXmjxEFr8XKyyRuQBwSlRTngAvOw8jUnCe1vyYD5xPec1xpfOEGLi5BqSog+6tBtsry3oAtcENX8SV1tVuMpp6D+UrrU8xNT/5D70uRDppkPE3vq+t7rR0fVSdQRdUV9KmQD2bflA1Dyb2y37EzwJOMHDDQ82aOhj/JmPxvEAlV8RkZl6J0HIveraRy9wbNLbI7jpiOCw==",\n  "SigningCertURL" : "https://sns.eu-west-1.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem",\n  "UnsubscribeURL" : "https://sns.eu-west-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-west-1:231436140809:powertools265:15189ad7-870e-40e5-a7dd-a48898cd9f86"\n}',  # noqa: E501
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1611050827340",
                    "SenderId": "AIDAISMY7JYY5F7RTT6AO",
                    "ApproximateFirstReceiveTimestamp": "1611050827344",
                },
                "messageAttributes": {},
                "md5OfBody": "8910bdaaf9a30a607f7891037d4af0b0",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:eu-west-1:231436140809:powertools265",
                "awsRegion": "eu-west-1",
            }
        ]
    }


@pytest.fixture
def event_bridge_event_dict():
    return {
        "version": "0",
        "id": "6a7e8feb-b491-4cf7-a9f1-bf3703467718",
        "detail-type": "EC2 Instance State-change Notification",
        "source": "aws.ec2",
        "account": "111122223333",
        "time": "2017-12-22T18:43:48Z",
        "region": "us-west-1",
        "resources": [
            "arn:aws:ec2:us-west-1:123456789012:instance/i-1234567890abcdef0"
        ],
        "detail": {"instance_id": "i-1234567890abcdef0", "state": "terminated"},
        "replay-name": "replay_archive",
    }
