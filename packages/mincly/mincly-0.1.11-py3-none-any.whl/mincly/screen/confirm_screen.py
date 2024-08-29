import re as _re
import typing as _t
from .common import Screen as _Screen
from ..utils.result import Result as _Result


class ConfirmScreen(_Screen[bool]):
    def __init__(
        self,
        message: str,
        true_regex: str = r"^[Yy]|[Yy][Ee][Ss]$",
        default_no_input: _t.Union[bool, None] = None,
        screen_name: _t.Union[str, None] = None,
    ) -> None:
        super().__init__(screen_name)
        self.message = message
        self.true_regex = _re.compile(true_regex)
        self.default = default_no_input

    """
    Represents a screen that prompts the user for a yes/no confirmation.

    -`message`: The prompt to display to the user.
    
    -`true_regex`: A regular expression pattern that defines what constitutes a
    "yes" response (a response which would yield `True`). Defaults to a typical
    `y` or `yes` case insensitive response.
    
    -`default_no_input`: The default value to return if the user provides no
    input. If `None`, an error will be returned instead.
    
    -`screen_name`: An optional name for the screen, used for identification.
    """

    def get_display_string(self) -> str:
        return self.message

    def process_input(self, user_input: str) -> _Result[bool]:
        if self.true_regex.match(user_input):
            return _Result[bool].Ok(True)
        elif len(user_input) < 1:
            return (
                _Result[bool].Err("Empty input")
                if self.default is None
                else _Result[bool].Ok(self.default)
            )
        else:
            return _Result[bool].Ok(False)
