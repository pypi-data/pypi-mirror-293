from mincly.utils.result import Result as _Result
import typing as _t

_T = _t.TypeVar("_T")

Result = _t.Type[_Result[_T]]
