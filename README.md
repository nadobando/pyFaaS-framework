# pyFaas-framework

[![Build Status]()]() # TODO

pyFaas-framework is a Cloud agnostic Function as a Service framework for Python. 
Work is still in progress, but getting there :)
# Current Supported Cloud Providers
  - AWS

# Features 
  - Function Lifecycle
  - Model Validation
  - Handler Settings Validation
  - Error Handling
 
## Model Validation and Handler Settings Validation
The validations are based on [Pydantic] BaseModel and BaseSettings which you can define to meet your needs  

# AWS Features
  - Native Lambda Handler 
  - AWS Lambda API Gateway Proxy Handler
  - SQS Event Handler including SNS Subscription
  - EventBridge



### Installation
Currently work is in progress so the insallation is from github
#### Github
```sh
pip install https://github.com/nadobando/pyFaaS-framework
```
```sh
pipenv install https://github.com/nadobando/pyFaas-framework
```

### How To use ###

#### AWS
##### NativeHandler 

```python
from pydantic import BaseModel, validator, BaseSettings
from faas_framework.aws.handlers.native import NativeHandler

class HelloWorldSettings(BaseSettings):
    greeter: str

class HelloWorldNativeRequestModel(BaseModel):
    name: str

    @validator('name', pre=True)
    def convert_to_title(cls, value: str):
        return value.title()

class HelloWorldResponse(BaseModel):
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
from pydantic import BaseModel, validator, BaseSettings

from faas_framework.aws.handlers.api_gw import LambdaApiGwProxyHandler


# Loaded from environment variables
class HelloWorldSettings(BaseSettings):
    greeter: str


class HelloWorldNativeRequestModel(BaseModel):
    name: str

    @validator('name', pre=True)
    def convert_to_title(cls, value: str):
        return value.title()


class HelloWorldResponse(BaseModel):
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
    "body": '{"name": "pyFaas-framework"}',
    "isBase64Encoded": False
}
handler(event, LambdaContext())


```
returns:
```python
{
    'body': '{"message": "me says hello to Pyfaas-Framework"}',
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
