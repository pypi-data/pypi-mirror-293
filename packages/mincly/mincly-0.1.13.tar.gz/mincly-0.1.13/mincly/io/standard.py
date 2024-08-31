from .common import Writer as _Writer, Reader as _Reader, HybridIo as _HybridIo


class StandardTerminalWriter(_Writer):
    """
    Basic output to terminal. `write()` is Python's builtin `print()` and
    `clear()` prints empty lines to create separation
    """

    def __init__(
        self,
        add_newline_to_prints: bool = False,
        always_flush: bool = True,
        newlines_added_on_clear: int = 5,
    ) -> None:
        self._print_options = {}
        self._print_options["end"] = "\n" if add_newline_to_prints else ""
        if always_flush:
            self._print_options["flush"] = True
        self._clear_lines = max(0, newlines_added_on_clear)

    def write(self, message: str):
        """
        Prints message to terminal. Avoid using ANSI control sequence characters
        in `value`
        """
        print(message, **self._print_options)

    def clear(self):
        """
        Prints newlines to screen to create separation from previous prints.
        """
        print("\n" * self._clear_lines, end="")


class StandardTerminalReader(_Reader):
    """Basic input from terminal. Uses Python's builtin `input()`."""

    def read(self) -> str:
        """
        Retrieves input using Python's builtin `input` method. Takes into
        account the user's input and newline character (ENTER) for the next call
        to `clear()`.
        """
        return input()


class StandardTerminalIo(_HybridIo):
    """
    Hybrid of `StandardTerminalReader` and `StandardTerminalWriter`.
    """

    def __init__(self) -> None:
        super().__init__(StandardTerminalReader(), StandardTerminalWriter())
