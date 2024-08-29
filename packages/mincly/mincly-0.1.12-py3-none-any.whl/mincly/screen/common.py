from abc import ABC as _Abstract, abstractmethod as abstract
import typing as _t
from ..utils.result import Result as _Result

_T = _t.TypeVar("_T")


class Screen(_Abstract, _t.Generic[_T]):
    def __init__(self, screen_name: _t.Union[str, None] = None) -> None:
        self.name = screen_name

    def __str__(self) -> str:
        return f"{self.__class__.__name__}('{self.name if self.name is not None else '<NoName>'}')"

    @abstract
    def process_input(self, user_input: str) -> _Result[_T]:
        """
        React to `user_input` and give back a Result that represents the
        validity of the given input. `Result.Err` means input is invalid and its
        not this class's responsability what to do further. `Result.Ok` means
        input was valid and the wrapped value contains some sort of response
        that will only make sense for a concrete screen (or `None`)
        """

    @abstract
    def get_display_string(self) -> str:
        """
        Returns a string of what should be displayed for this screen
        """
