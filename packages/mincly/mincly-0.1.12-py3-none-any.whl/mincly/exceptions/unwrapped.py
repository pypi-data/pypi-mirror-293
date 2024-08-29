class UnwrappedException(Exception):
    def __init__(self) -> None:
        super().__init__(
            f"Unwrapped Result instance that was holding an exception instead of a value."
        )
