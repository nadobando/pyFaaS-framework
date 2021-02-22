try:
    from typing import *
except ImportError:
    try:
        from typing_extensions import Literal  # noqa: F401
    except ImportError:
        raise Exception("please install typing-extensions or upgrade to Python >= 3.8")

DataT = TypeVar('DataT')
