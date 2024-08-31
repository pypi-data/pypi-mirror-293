from capyutils import Result as _Result, Ok as _Ok
from mincly.screen.common import Screen as _Screen
import typing as _t


class InputScreen(_Screen[str]):
    """
    Represents screen that handles raw string input (similar to Python's
    `input()`)

    - `preamble`: Text that is displayed before prompting user input. Note that
      no newlines or whitespace are added to this text.
    """

    def __init__(self, preamble: str, screen_name: _t.Optional[str] = None) -> None:
        super().__init__(screen_name)
        self._preamble = preamble

    def process_input(self, user_input: str) -> _Result[str]:
        return _Ok(user_input)

    def get_display_string(self) -> str:
        return self._preamble
