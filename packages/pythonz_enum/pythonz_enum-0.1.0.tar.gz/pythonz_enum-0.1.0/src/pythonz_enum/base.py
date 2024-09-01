class Enum:
    def __init__(self, case_name, *args):
        if not hasattr(self, case_name):
            raise ValueError(f"Invalid case name: {case_name}")
        self.case = case_name
        self.args = args

    def __repr__(self):
        cls = self.__class__
        cls_name = cls.__name__
        return f"{cls_name}.{self.case}({', '.join(map(repr, self.args))})"


    def match(self, case_dict: dict):
        cls = type(self)
        return case_dict[getattr(cls, self.case)](*self.args)


def case(name, *placeholders):
    argc = len(placeholders)

    def inner(cls, *args):
        if len(args) != argc:
            raise ValueError(f"Incorrect number of arguments, expected: {argc}, got {len(args)}")
        return cls(name, *args)
    return classmethod(inner)
