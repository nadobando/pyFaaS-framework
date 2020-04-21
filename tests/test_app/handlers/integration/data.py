import typing
import uuid

from lamb_frame import BaseModel
from lamb_frame.models import validator
# from package_x.models import Hostname
from tests.test_app.package_x.models import Hostname


class TenantUpdateDnsRequest(BaseModel):
    tenant_id: uuid.UUID
    host_names: typing.Set[Hostname]

    @validator('host_names')
    def no_same_host_names(cls, host_names):
        _list = list((map(lambda x: x.domain, host_names)))
        for domain in _list:
            assert _list.count(domain) <= 1, "is not allowed to include 2 entries with the same domain"
        return host_names

