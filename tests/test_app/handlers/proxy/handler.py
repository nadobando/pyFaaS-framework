from lamb_frame import AwsApiGatewayHttpRequest, LambdaProxyHandler, HttpResponse
from lamb_frame.utils.aws import is_running_on_aws


class HelloWorldHandler(LambdaProxyHandler):
    def handle(self, *, request: AwsApiGatewayHttpRequest, **kwargs) -> HttpResponse:
        res = HttpResponse(status_code=200, body={"kuku": "dasdasdas"})
        return res


if is_running_on_aws():
    handler = HelloWorldHandler()
elif __name__ == '__main__':
    from aws_lambda_context import LambdaContext
    import json

    context = LambdaContext()
    context.aws_request_id = "xxx"
    # context.client_context = LambdaClientContext()
    # context.client_context.custom = {"correlationId": "1232-3123123-12312-123"}

    handler = HelloWorldHandler()

    _request = {
        'resource': '/echo',
        'path': '/echo',
        'httpMethod': 'GET',
        'multiValueHeaders': {

            'accept': [
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'],
            'accept-encoding': ['gzip, deflate, br'],
            'accept-language': ['en-US,en;q=0.9,he;q=0.8'],
            'Host': ['59vjxb9z4b.execute-api.us-east-1.amazonaws.com'],
            'referer': ['https://us-east-1.console.aws.amazon.com/'],
            'sec-ch-ua': [],
            'sec-ch-ua-mobile': ['?0'],
            'sec-fetch-dest': ['document'],
            'sec-fetch-mode': ['navigate'],
            'sec-fetch-site': ['cross-site'],
            'sec-fetch-user': ['?1'],
            'upgrade-insecure-requests': ['1'],
            'User-Agent': [
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'],
            'X-Amzn-Trace-Id': ['Root=1-5fe84b31-7debb86b520b6953714d968e'],
            'X-Forwarded-For': ['37.142.7.68'],
            'X-Forwarded-Port': ['443'],
            'X-Forwarded-Proto': ['https']},
        'multiValueQueryStringParameters': None,
        'pathParameters': None,
        'stageVariables': None,
        'requestContext': {
            'resourceId': 'vjfyvv',
            'resourcePath': '/echo',
            'httpMethod': 'GET',
            'extendedRequestId': 'YNCvuFBXIAMFTKQ=',
            'requestTime': '27/Dec/2020:08:52:01 +0000',
            'path': '/default/echo',
            'accountId': '086285707022',
            'protocol': 'HTTP/1.1',
            'stage': 'default',
            'domainPrefix': '59vjxb9z4b',
            'requestTimeEpoch': 1609059121362,
            'requestId': '70dd722a-0155-4794-a43f-82a7cfdc7545',
            'identity': {
                'cognitoIdentityPoolId': None,
                'accountId': None,
                'cognitoIdentityId': None,
                'caller': None,
                'sourceIp': '37.142.7.68',
                'principalOrgId': None,
                'accessKey': None,
                'cognitoAuthenticationType': None,
                'cognitoAuthenticationProvider': None,
                'userArn': None,
                'userAgent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                'user': None
            },
            'domainName': '59vjxb9z4b.execute-api.us-east-1.amazonaws.com',
            'apiId': '59vjxb9z4b'},
        'body': None,
        'isBase64Encoded': False
    }
    response = handler(_request, context)
    print(json.dumps(response, indent=2))
