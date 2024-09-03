from pythonz_enum.base import Enum, case

def throw(exc: BaseException): raise exc

class Maybe(Enum):
    @case
    @classmethod
    def nothing(cls) -> "Maybe": ...

    @case
    @classmethod
    def just(cls, val) -> "Maybe": ...


    def unwrap(self):
        return self.match({
            self.nothing: lambda: throw(UnwrapNothingError()),
            self.just: lambda val: val,
        })


class UnwrapNothingError(RuntimeError): ...
