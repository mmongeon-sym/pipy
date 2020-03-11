

def assert_type(value: object,
                value_type: type,
                name: str = None,
                allow_none: bool = False,
                ):
    if name is not None:
        param_s = "parameter: {NAME}={REPR}({TYPE})".format(NAME=name,
                                                            TYPE=type(value),
                                                            REPR=repr(value)
                                                            )
    else:
        param_s = "argument: ({REPR})({TYPE})".format(NAME=name,
                                                      TYPE=type(value),
                                                      REPR=repr(value)
                                                      )
    if value is None:
        if allow_none is False:
            raise ValueError("Provided {PARAM_S} must be not be None".format(PARAM_S=param_s, TYPE=type(value_type)))
        else:
            return None
    try:
        value = value_type(value)
    except Exception as e:
        pass

    if isinstance(value, value_type) is True:
        return value
    else:
        raise TypeError("Provided {PARAM_S} must be of type({TYPE})".format(PARAM_S=param_s,
                                                                            TYPE=type(value_type)
                                                                            ))


def assert_list(value: list, name: str = None, allow_none: bool = False):
    value: list = assert_type(value=value, value_type=list, name=name, allow_none=allow_none)
    return value


def assert_int(value: int, name: str = None, allow_none: bool = False):
    value: int = assert_type(value=value, value_type=int, name=name, allow_none=allow_none)
    return value


def assert_str(value: str, name: str = None, allow_none: bool = False):
    value: str = assert_type(value=value, value_type=str, name=name, allow_none=allow_none)
    return value


def assert_bool(value: bool, name: str = None, allow_none: bool = False):
    value: bool = assert_type(value=value, value_type=bool, name=name, allow_none=allow_none)
    return value


def assert_float(value: float, name: str = None, allow_none: bool = False):
    value: float = assert_type(value=value, value_type=float, name=name, allow_none=allow_none)
    return value
