# pyFaaS-framework

[![codecov](https://codecov.io/gh/nadobando/pyFaaS-framework/branch/master/graph/badge.svg?token=8QZ00BRLFU)](https://codecov.io/gh/nadobando/pyFaaS-framework)[![Build Status]()]() # TODO

pyFaaS-framework is a Cloud agnostic Function as a Service framework for Python.
Work is still in progress, but getting there :)
# Installation
Currently work is in progress so the installation is from github
## Github
```sh
pip install https://github.com/nadobando/pyFaaS-framework
```
```sh
pipenv install https://github.com/nadobando/pyFaaS-framework
```
# Current Supported Cloud Providers
  - AWS

# Features
  - Function Lifecycle
  - Model Parsing and Validation
  - Handler Settings Parsing and Validation
  - Error Handling

## Model Validation and Handler Settings Validation
The validations are based on [Pydantic] AliasedBaseModel and BaseSettings which you can define to meet your needs

# AWS Features
  - Native Lambda Handler
  - AWS Lambda API Gateway Proxy Handler
  - SQS Event Handler including SNS Subscription
  - EventBridge Handler



## How To use
### Deployment Configuration
#### Serverless Framework
```yaml
service: my-fist-faas-framework-service

custom:
  pythonRequirements:
    dockerizePip: non-linux
    slim: true
    slimPatterns:
      - "**/tests/**"
    layer:
      retain: false

provider:
  name: aws
  runtime: python3.8
  stage: ${opt:stage,'test'}
  environment:
    POWERTOOLS_SERVICE_NAME: ${self:service}-${self:provider.stage} # this will be also part of the framework

plugins:
  - serverless-python-requirements # optional but recommended

functions:
  myFirstFunction:
    handler: faas_framework.app.handler
    environment:
      CLASS_HANDLER: "path.to.your.handler"
```

#### AWS
##### NativeHandler

```python
from pydantic import AliasedBaseModel, validator, BaseSettings
from faas_framework.aws.handlers.native import NativeHandler

class HelloWorldSettings(BaseSettings):
    greeter: str

class HelloWorldNativeRequestModel(AliasedBaseModel):
    name: str

    @validator('name', pre=True)
    def convert_to_title(cls, value: str):
        return value.title()

class HelloWorldResponse(AliasedBaseModel):
    message: str

class HelloWorldHandler(NativeHandler):
    request_class = HelloWorldNativeRequestModel
    settings_class = HelloWorldSettings

    def handle(self, request: HelloWorldNativeRequestModel):
        return HelloWorldResponse(message=f"{self.settings.greeter} says hello to {request.name}")
```

##### LambdaApiGwProxyHandler
```python
from aws_lambda_powertools.utilities.typing import LambdaContext # will be part of the framework
from pydantic import AliasedBaseModel, validator, BaseSettings

from faas_framework.aws.handlers.api_gw import LambdaApiGwProxyHandler


# Loaded from environment variables
class HelloWorldSettings(BaseSettings):
    greeter: str


class HelloWorldNativeRequestModel(AliasedBaseModel):
    name: str

    @validator('name', pre=True)
    def convert_to_title(cls, value: str):
        return value.title()


class HelloWorldResponse(AliasedBaseModel):
    message: str


class HelloWorldApiGwHandler(LambdaApiGwProxyHandler):
    body_class = HelloWorldNativeRequestModel
    settings_class = HelloWorldSettings

    def handle(self, request: HelloWorldNativeRequestModel):
        return HelloWorldResponse(message=f"{self.settings.greeter} says hello to {request.name}")


import os

os.environ["greeter"] = "me"
handler = HelloWorldApiGwHandler()
event = {
    "version": "1.0",
    "resource": "/my/{param}",
    "path": "/my/test-param",
    "httpMethod": "GET",
    "headers": {
        "Header1": "value1",
        "Header2": "value2",
        "Content-Type": "application/json"
    },
    "multiValueHeaders": {
        "Header1": [
            "value1"
        ],
        "Header2": [
            "value1",
            "value2"
        ],
        "Content-Type": ["application/json"]

    },
    "queryStringParameters": {
        "parameter1": "value2",
        "parameter2": "value3"
    },
    "multiValueQueryStringParameters": {
        "parameter1": [
            "value1",
            "value2"
        ],
        "parameter2": [
            "value3"
        ]
    },
    "requestContext": {
        "accountId": "123456789012",
        "apiId": "id",
        "authorizer": {
            "claims": None,
            "scopes": None
        },
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
            "userArn": None
        },
        "path": "/my/path",
        "protocol": "HTTP/1.1",
        "requestId": "id=",
        "requestTime": "04/Mar/2020:19:15:17 +0000",
        "requestTimeEpoch": 1583349317135,
        "resourceId": None,
        "resourcePath": "/my/path",
        "stage": "$default"
    },
    "pathParameters": {'param': 'test-param'},
    "stageVariables": None,
    "body": '{"name": "pyFaaS-framework"}',
    "isBase64Encoded": False
}
handler(event, LambdaContext())


```
returns:
```python
{
    'body': '{"message": "me says hello to pyFaaS-framework"}',
    'isBase64Encoded': False,
    'multiValueHeaders': {
            'X-Correlation-Id': ['82348ccf-ddac-4f73-b61e-a960a8d2369b']
        },
    'statusCode': 200
}
```




### Todos
  - Create Pypi Repository
 - Add more Cloud Providers

License
----
MIT


**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)



   [Pydantic]: <https://pydantic-docs.helpmanual.io/>
