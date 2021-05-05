def _value_eval(value,
                between=None,
                data_type=None,
                name="Variable",
                raise_exception=False):
    """
    Tests if value meets criteria.

    :param value: value to test
    :param kwargs:
    :return: True if meets, False if not
    """
    if data_type:
        if type(value) != data_type:
            if raise_exception:
                raise TypeError(f"{name} with value {value} is not of type {data_type}")
            else:
                return False

    if between:
        if not between[0] <= value <= between[1]:
            if raise_exception:
                raise ValueError(f"{name} with value {value} is not in between values {between}")
            else:
                return False

    return True

