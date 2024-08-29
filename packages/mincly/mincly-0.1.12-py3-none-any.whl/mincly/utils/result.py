import typing as _t

_T = _t.TypeVar("_T")


class Result(_t.Generic[_T]):
    """
    Util class to wrap around fallible values instead of raising Exceptions. Do
    not instantiate direcly, instead, use `Err` and `Ok` util functions from
    this package
    """

    def __init__(self, value: _t.Union[_T, BaseException]):
        self._value = value

    def is_ok(self) -> bool:
        """
        Returns `True` if this `Result` is of the `Ok` type
        """
        return not self.is_ok()

    def is_err(self) -> bool:
        """
        Returns `True` if this `Result` is of the `Err` type
        """
        return isinstance(self._value, BaseException)

    def unwrap(self) -> _T:
        """
        Returns the wrapped value if this `Result` is `Ok`, else, if this
        `Result` is `Err`, then raises the UnwrappedException, instead.
        """
        if isinstance(self._value, BaseException):
            raise UnwrappedException() from self._value
        else:
            return self._value

    def try_unwrap(self) -> _t.Union[_T, None]:
        """
        Returns the wrapped value if this `Result` is `Ok`, else, if this
        `Result` is `Err`, returns `None`.
        """
        if not isinstance(self._value, BaseException):
            return self._value
        else:
            return None

    def unwrap_err(self) -> BaseException:
        """
        Returns the wrapped exception if this `Result` is `Err`, else, if this
        `Result` is `Ok`, then raises a `UnwrapedException`.
        """
        if isinstance(self._value, BaseException):
            return self._value
        else:
            raise TypeError("Can't unwrap error type in instance of Ok result.")

    @staticmethod
    def Err(error: _t.Union[BaseException, str]) -> "Result[_T]":
        """
        Instantiate Error Result which wraps around exception. If `error` is a
        string, will instantiate an `Exception` with `error` as error message.

        If the wrapped type is not important for type checkers, use
        `Result.Err(error)`. If it is, explictly provide the type (e.g.
        `Result[str].Err(error)`)
        """
        if isinstance(error, str):
            return Result(Exception(error))
        return Result(error)

    @staticmethod
    def Ok(value: _T) -> "Result[_T]":
        """
        Instantiate Ok Result which wraps around a `value` (use `None` if value
        is irrelevant)

        Explictly provide the type (e.g. `Result[str].Ok("A string.")`) to let
        type checkers know the type of the wrapped value
        """
        return Result(value)


a = Result[str].Ok("Hey!")
