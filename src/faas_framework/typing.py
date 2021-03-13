try:
    from typing import *  # noqa: F403 F401
    from typing import Literal
except ImportError:
    try:
        from typing_extensions import Literal  # noqa: F401
    except ImportError:
        raise Exception("please install typing-extensions or upgrade to Python >= 3.8")


from typing import TypeVar

DataT = TypeVar("DataT")
