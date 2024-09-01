from pythonz_enum.base import Enum, case

def throw(exc: BaseException): raise exc

class Maybe(Enum):
    Nothing = case("Nothing")
    Just = case("Just", ...)

    def unwrap(self):
        return self.match({
            self.Nothing: lambda: throw(UnwrapNothingError()),
            self.Just: lambda val: val,
        })


class UnwrapNothingError(RuntimeError): ...
