import json

from lamb_frame import LambdaProxyHandler, HttpResponse
from tests.test_app.handlers.integration.data import TenantUpdateDnsRequest


class HelloWorldHandler(LambdaProxyHandler):
    # settings_class = HelloWorldSettings
    body_class = TenantUpdateDnsRequest

    def handle(self, *, request, **kwargs) -> HttpResponse:
        dns_dto: TenantUpdateDnsRequest = request.body
        res = HttpResponse(status_code=200, body={"kkyky": "2231"})
        return res


handler = HelloWorldHandler()

if __name__ == '__main__':
    from aws_lambda_context import LambdaContext

    context = LambdaContext()
    context.aws_request_id = "xxx"
    # context.client_context = LambdaClientContext()
    # context.client_context.custom = {"correlationId": "1232-3123123-12312-123"}

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
        'body': {
            "tenantId": "1509e1b1-1994-46c1-bfd1-5e4515891e1b",
            "hostNames": []
        },
        'isBase64Encoded': False
    }
    response = handler(_request, context)
    print(json.dumps(response, indent=1))
