import typing
import uuid

from lamb_frame import BaseModel
from tests.test_app.package_x.models import Hostname


class DnsDTO(BaseModel):
    tenant_id: uuid.UUID
    host_names: typing.Set[Hostname]
