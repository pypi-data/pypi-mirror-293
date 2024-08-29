import typing as _t
from .common import Screen as _Screen
from ..utils.result import Result as _Result

_T = _t.TypeVar("_T")


class SelectScreen(_Screen[_T]):
    """
    Screen for user to select from one of many options.

    - `numbered_options` is any iterable of tuples of `(description: str, value:
      T)`. The user will be shown all numbered options in order, with a number
      indicating which number the user should provide to choose that option
      (starting with 1). `value` will be the returned value, should the user
      pick the associated option.

    - `keyword_options` works the same way as `numbered_options`, but instead of
      showing the user multiple items ordered from 1 onwards, they are instead
      associated with the given dictionary's keys. (e.g. `{"Open": ("opens
      something": "open_file")}` would return `"open_file"` if the user typed in
      `"Open"`)

    - `header` displays an header message above the selection listing

    - `name` the name of the screen, which acts as an identifier, should it be
      useful for the program's logic
    """

    def __init__(
        self,
        numbered_options: _t.Optional[_t.Sequence[_t.Tuple[str, _T]]] = None,
        keyword_options: _t.Optional[_t.Dict[str, _t.Tuple[str, _T]]] = None,
        header: str = "Pick an option:",
        name: _t.Union[str, None] = None,
    ) -> None:
        super().__init__(name)
        if numbered_options is None and keyword_options is None:
            raise ValueError(
                "SelectScreen can't be built with no options. At least one of numbered_options or keyword_options needs to not be 'None'"
            )
        self.numbered_options = numbered_options or tuple()
        self.keyword_options = keyword_options or dict()
        self.header = header if header.endswith("\n") else header + "\n"

    def process_input(self, user_input: str) -> _Result[_T]:
        if len(user_input) < 1:
            return _Result[_T].Err("Empty input")

        if user_input.isdecimal():
            nth_option = int(user_input) - 1
            if nth_option < 0 or nth_option >= len(self.numbered_options):
                return _Result[_T].Err(f"Invalid numbered option '{user_input}'")
            _, option = self.numbered_options[nth_option]
            return _Result[_T].Ok(option)

        _, option = self.keyword_options.get(user_input, ("", None))
        if option is None:
            return _Result[_T].Err(f"Invalid keyword option '{user_input}'")

        return _Result[_T].Ok(option)

    def get_display_string(self) -> str:
        display_string = f"{self.header}"

        for nth, (option_description, _) in enumerate(self.numbered_options, start=1):
            display_string += f" {nth} - {option_description}\n"

        if len(self.numbered_options) > 0:
            display_string += "\n"

        for key, (option_description, _) in self.keyword_options.items():
            display_string += f" {key} - {option_description}\n"

        if len(self.keyword_options) > 0:
            display_string += "\n"

        return display_string
