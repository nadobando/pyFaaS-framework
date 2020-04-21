import typing

from lamb_frame import BaseModel


class Hostname(BaseModel):
    domain: str
    subDomains: typing.Sequence[str]

    def __hash__(self):
        if self.subDomains and len(self.subDomains):
            return (self.domain + "".join(self.subDomains)).__hash__()
        else:
            return self.domain.__hash__()

