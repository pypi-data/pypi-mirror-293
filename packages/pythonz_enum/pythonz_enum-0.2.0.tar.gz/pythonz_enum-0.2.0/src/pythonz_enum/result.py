from pythonz_enum.base import Enum, case

def throw(exc: BaseException): raise exc

class Result(Enum):
    @case
    @classmethod
    def ok(cls, val) -> "Result": ...

    @case
    @classmethod
    def err(cls, val) -> "Result": ...

    def unwrap(self):
        return self.match({
            self.ok: lambda val: val,
            self.err: lambda err: throw(err),
        })
