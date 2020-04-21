import sys
# Do not remove this line
from typing import *

if sys.version_info[0] < 3:
    raise Exception("Must be using Python > 3.5")

if sys.version_info[1] < 8:
    try:
        from typing_extensions import *
    except ImportError:
        raise Exception("please install typing-extensions or upgrade to Python >= 3.8")
