from pythonz_enum.base import Enum, case

def throw(exc: BaseException): raise exc

class Result(Enum):
    Ok = case("Ok", ...)
    Err = case("Err", ...)

    def unwrap(self):
        return self.match({
            self.Ok: lambda val: val,
            self.Err: lambda err: throw(err),
        })
