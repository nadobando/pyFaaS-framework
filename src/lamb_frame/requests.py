from dataclasses import dataclass

from . import typing


# from pydantic import Extra


@dataclass
class AwsApiGatewayHttpRequest:
    path: str
    method: typing.Literal["HEAD", "GET", "POST", "PUT", "PATCH", "OPTIONS", "CONNECT", "TRACE", "DELETE"]
    headers: typing.Mapping[str, typing.List[str]] = None
    query_str: typing.Optional[typing.Mapping[str, typing.List[str]]] = None
    params: typing.Optional[typing.Mapping[str, str]] = None
    body: typing.Any = None

    # class Config:
    #     allow_mutation = True
    #     extra = Extra.allow

    @classmethod
    def parse_request(cls, request):
        headers = request['multiValueHeaders']
        qs_params = request['multiValueQueryStringParameters'] if request['multiValueQueryStringParameters'] else {}
        query_str = {
            x: y[0] for x, y in qs_params.items() if len(y) == 1
        }
        qs_params.update(query_str)
        path_params = request['pathParameters']

        _request = dict(
            path=request['path'],
            headers=headers if headers else {},
            query_str=qs_params,
            params=path_params if path_params else {},
            body=request['body'] if not request['isBase64Encoded'] else request['body'].decode('ascii'),
            method=request['httpMethod']

        )
        return cls(**_request)
