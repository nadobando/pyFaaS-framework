import uuid

from lamb_frame import NativeHandler
# from .data import TenantUpdateDnsRequest
# from .settings import HelloWorldSettings
# from package_x.models import Hostname
from tests.test_app.handlers.integration.data import TenantUpdateDnsRequest
from tests.test_app.handlers.integration.settings import HelloWorldSettings
from tests.test_app.package_x.models import Hostname


class HelloWorldHandler(NativeHandler):
    request_class = TenantUpdateDnsRequest
    settings_class = HelloWorldSettings
    settings: HelloWorldSettings

    def handle(self, request: TenantUpdateDnsRequest):
        return Hostname(domain="dasdsa", subDomains=["dasd"])


handler = HelloWorldHandler()
u = str(uuid.uuid4())

if __name__ == '__main__':
    from aws_lambda_context import LambdaContext, LambdaClientContext
    import json
    context = LambdaContext()
    context.aws_request_id = "xxx"
    context.client_context = LambdaClientContext()
    # context.client_context.custom = {"correlationId": "1232-3123123-12312-123"}
    print(u)
    event = {
        "tenantId": u,
        "hostNames": [
            {"domain": "dadas", "subDomains": ["asd"]},
            {"domain": "dadas", "subDomains": ["asd"]},
            # {"domain": "dadas", "subDomains": ["asd", "21312"]},
            {"domain": "dadas", "subDomains": ["asd"]},
            {"domain": "dadas", "subDomains": ["asd"]},
        ]}
    d = handler(event, context)
    print(d)
    # print(json.dumps(d, indent=2))
