import re

camelcase_re = re.compile(r"[\-_\.\s]([a-z])")


def camelcase(string: str):
    """ Convert string into camel case.
    Args:
        string: String to convert.
    Returns:
        string: Camel case string.
    """

    string = re.sub(r"^[\-_\.]", '', str(string))
    # if not string:
    #     return string

    return string[0].lower() + camelcase_re.sub(lambda matched: matched.group(1).upper(), string[1:])


def title_case(string):
    """ Convert string into camel case.
    Args:
        string: String to convert.
    Returns:
        string: Camel case string.
    """

    string = re.sub(r"^[\-_\.]", '', str(string))
    if not string:
        return string

    return string[0].upper() + camelcase_re.sub(lambda matched: matched.group(1).upper(), string[1:])


def is_primitive(obj):
    return type(obj) in [str, int, float, bool, None, type(None)]
