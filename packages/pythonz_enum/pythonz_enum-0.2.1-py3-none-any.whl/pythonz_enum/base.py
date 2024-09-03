import inspect
from collections import OrderedDict
from typing import Any


class EnumCase:
    def __init__(self, *args):
        if len(args) < 1:
            raise TypeError('EnumCase requires at least one argument')
        ident, *args = args
        self.name = None
        self.params = OrderedDict()

        if isinstance(ident, str):
            self.name = ident
            for idx, arg in enumerate(args):
                if isinstance(arg, str):
                    self.params[arg] = ...
                else:
                    self.params[f"val_{idx}"] = ...
        elif isinstance(ident, (classmethod, staticmethod, type(lambda: ...))):
            func = getattr(ident, '__func__', ident)
            self.name = func.__name__
            for idx, param in enumerate(inspect.signature(func).parameters):
                if idx == 0 and isinstance(ident, classmethod):
                    continue
                self.params[param] = ...
        elif issubclass(ident, type):
            self.name = ident.__name__
            for param in ident.__annotations__:
                self.params[param] = ...
        else:
            raise TypeError('EnumCase can only be created through str, method, or class')

    # just for the signature. never gets called
    def __call__(self, *args, **kwargs) -> "Enum": ...

case = EnumCase


class EnumMeta(type):
    __cases__: OrderedDict
    __sealed__: bool

    def __new__(mcs, name, bases, attrs):
        for base in bases:
            if isinstance(base, EnumMeta) and not hasattr(base, name):
                if base.__sealed__:
                    raise TypeError("cannot subclass arg sealed enum")
        __cases__ = OrderedDict()
        for attr, value in tuple(attrs.items()):
            if attr != "__case_info__" and isinstance(value, EnumCase):
                __cases__[attr] = value
                del attrs[attr]
        attrs['__cases__'] = __cases__
        cls = super().__new__(mcs, name, bases, attrs)
        for case_name, case_info in __cases__.items():
            case_attrs = OrderedDict()
            case_attrs["__match_args__"] = tuple(case_info.params)
            case_attrs["__annotations__"] = OrderedDict()
            case_attrs["__params__"] = case_info.params
            for param in case_info.params:
                case_attrs["__annotations__"][param] = Any

            def __new__(_cls, *_args, **_kwargs):
                _name = _cls.__name__
                params = _cls.__params__
                args = []
                for idx, p in enumerate(params):
                    if hasattr(_kwargs, p):
                        arg = _kwargs[p]
                        del _kwargs[p]
                    elif idx < len(_args):
                        arg = _args[idx]
                    else:
                        raise TypeError(f"{_name} missing required argument `{p}` at position {idx}")
                    args.append(arg)
                if _kwargs or len(args) < len(_args):
                    raise TypeError(f"Too many arguments for `{_name}`. required parameters are: {', '.join(case_info.params)}")
                # noinspection PyArgumentList
                _self = tuple.__new__(_cls, args)
                for p, arg in zip(params, args):
                    setattr(_self, p, arg)
                return _self
            case_attrs["__new__"] = __new__

            def __repr__(self):
                _enum_name = name
                _case_cls = type(self)
                return "{enum}.{case}({params})".format(
                    enum=_enum_name,
                    case=_case_cls.__name__,
                    params=", ".join([
                        f"{p}={repr(arg)}"
                        for p, arg in zip(self.__params__, self)
                    ])
                )
            case_attrs["__repr__"] = __repr__

            case_cls = type(case_name, (cls, tuple), case_attrs)
            case_cls.__module__ = f"{cls.__module__}.{cls.__name__}"
            setattr(cls, case_name, case_cls)
        cls.__sealed__ = attrs.get('__sealed__', True)
        return cls


class Enum(tuple, metaclass=EnumMeta):
    __sealed__ = False

    def match(self, case_dict: dict):
        cls = type(self)
        return case_dict[cls](*self)
