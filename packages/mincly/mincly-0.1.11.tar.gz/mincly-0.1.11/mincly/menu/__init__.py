from mincly.io.common import (
    Io as _Io,
    Writer as _Writer,
    Reader as _Reader,
    HybridIo as _HybridIo,
)
from mincly.io.standard import (
    StandardTerminalReader as _StandardTerminalReader,
    StandardTerminalWriter as _StandardTerminalWriter,
)
import typing as _t
from ..io import Io as _Io, Reader as _Reader, Writer as _Writer
from ..screen import Screen as _Screen
from ..utils.result import Result as _Result

_T = _t.TypeVar("_T")


class Menu:
    """
    This class represents a menu system for user interaction.
    It behaves using a screen stack.
    """

    def __init__(
        self,
        input_output: _t.Optional[_Io] = None,
        input: _t.Optional[_Reader] = None,
        output: _t.Optional[_Writer] = None,
    ) -> None:
        """
        - `input_output`: An optional `Io` object that provides both input and
                output functionalities. If provided, `input` and `output` are
                ignored

        - `input`: An optional `Reader` object for handling user input.
                If not provided and `input_output` is also not provided, a
                `StandardTerminalReader` will be used by default. If
                `input_output` is provided, this argument is ignored

        - `output`: An optional `Writer` object for handling output to the user.
                If not provided and `input_output` is also not provided, a
                `StandardTerminalWriter` will be used by default. If
                `input_output` is provided, this argument is ignored
        """
        self._io: _Io
        if input_output is not None:
            self._io = input_output
        else:
            input_or_standard = (
                input if input is not None else _StandardTerminalReader()
            )
            output_or_standard = (
                output if output is not None else _StandardTerminalWriter()
            )
            self._io = _HybridIo(input_or_standard, output_or_standard)
        self._screen_stack: _t.List[_Screen[_t.Any]] = []
        self._last_input: _t.Any = None

    def show(self, message: str):
        """
        Shows a message without expecting any input from the user
        """
        self._io.print_overwrite(message)

    def push(self, screen: _Screen[_T]):
        """
        Adds the provided screen, which is added to this Menu instance's stack.

        Screen will only be displayed when calling `get_input()`
        """
        self._screen_stack.append(screen)

    def pop(self):
        """
        Pops current screen from the stack and returns to last found screen. If
        the current screen is the only screen in the stack, this method will
        raise an exception.
        """

        if len(self._screen_stack) < 2:
            raise RuntimeError(
                "Can't navigate back when current screen is root screen."
            )
        self._screen_stack.pop()

    def get_input(self) -> _t.Any:
        """
        Blocks until user provides a valid input. 'Valid input' is defined by
        the `Screen` class that is on the top of the screen stack.
        """
        self.prompt(self._screen_stack[-1])

    def get_last_input(self) -> _t.Any:
        return self._last_input

    def prompt(self, screen: _Screen[_T]) -> _T:
        """
        Displays the provided screen. Blocks until user provides a valid input.

        Provided screen is not added to screen stack and will not be stored by
        this `Menu` instance.
        """
        screen_result: _t.Union[_Result[_T], None] = None

        while screen_result is None or screen_result.is_err():
            self._io.print_overwrite(screen.get_display_string())

            if screen_result is not None and screen_result.is_err():
                self._io.write(f"<ERROR>: {screen_result.unwrap_err()}\n")

            user_input = self._io.read()

            screen_result = screen.process_input(user_input)
        result_value = screen_result.unwrap()
        self._last_input = result_value
        return result_value

    def current_screen_name(self) -> _t.Union[str, None]:
        return self._screen_stack[-1].name
