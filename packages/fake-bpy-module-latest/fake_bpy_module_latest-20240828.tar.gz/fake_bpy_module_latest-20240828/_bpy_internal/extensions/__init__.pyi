import typing
import collections.abc
import typing_extensions
from . import junction_module as junction_module
from . import stale_file_manager as stale_file_manager
from . import wheel_manager as wheel_manager

GenericType1 = typing.TypeVar("GenericType1")
GenericType2 = typing.TypeVar("GenericType2")
