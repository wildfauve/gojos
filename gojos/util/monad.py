from typing import List
import traceback
from pymonad.operators.either import Either
from typing import TypeVar, Callable, Union, Any, Generic

from . import fn

T = TypeVar('T')


class EitherMonad(Generic[T]):
    pass

class MEither(Either):
    def __or__(self, fns):
        """
        Acts as a Monadic OR, determining the function to execute based on the Either.
        Provide 2 terminating functions (failure_fn, success_fn)
        """
        return self.either(fns[0], fns[1])

    # Lifts the either; returning the wrapped value regardless of Left or Right
    def lift(self):
        return self.value if self.is_right() else self.monoid[0]

    def error(self):
        return self.monoid[0]


def Left(value: Either) -> Either[T, T]:  # pylint: disable=invalid-name
    """ Creates a value of the first possible type in the Either monad. """
    return MEither(None, (value, False))


def Right(value: Either) -> Either[T, T]:  # pylint: disable=invalid-name
    """ Creates a value of the second possible type in the Either monad. """
    return MEither(value, (None, True))


def maybe_value_ok(value: Either) -> bool:
    return value.is_right()


def maybe_value_fail(value: Either) -> bool:
    return value.is_left()


def monadic_try(name: str = None,
                status: int = None,
                exception_test_fn: Callable[[Either], Either] = None,
                error_cls: Any = None,
                error_result_fn: Callable = None):
    """
    Monadic Try Decorator.  Decorate any function which might return an exception.  When the function does not return an exception,
    the decorator wraps the result in a Right(), otherwise, it wraps the exception in a Left()

    Args:
        name: The name to be provided to the error object
        status: The status to be provided to the error object
        exception_test_fn: A function which takes the result.
                           When the result is Right, but the data may result in a Left.
                           The fn must return a value wrapped in an Either.
                           This fn can also be obtained from the expectation_fn to the main fn in the first instance
        error_result_fn:   A function whose result will be returned in the exception flow.  It takes a built exception (either str or error_cls).
                           If it takes an injected arg (error_result_fn_arg from main fn), it should be partially applied.

    The @monadic_try(name="step") is really syntax sugar for:
        $ monadic_try(name="x")(fn)(args)

        Hence the 3 nested functions
    """

    def inner(fn):
        def try_it(*args, **kwargs):
            try:
                result = Right(fn(*args, **kwargs))
                test_fn = kwargs.get('exception_test_fn', exception_test_fn)
                return test_fn(result) if test_fn else result
            except Exception as e:
                ex_cls = kwargs.get('error_cls', None) or error_cls

                error_result = Left(ex_cls(message=str(e),
                                           name=(kwargs.get('name', None) or name or fn.__name__),
                                           code=status, klass=str(e.__class__),
                                           traceback=traceback.format_exc())) if ex_cls else Left(str(e))

                return_fn = kwargs.get('error_result_fn', error_result_fn)
                if not return_fn:
                    return error_result

                injected_arg = kwargs.get('error_result_fn_arg', None)
                return return_fn(injected_arg, error_result)

        return try_it

    return inner


def any_error(try_result: Either) -> Union[str, None]:
    return try_result.either(lambda res: str(res.error()), lambda res: None)


def either_to_status(monad: EitherMonad):
    if not isinstance(monad, MEither):
        return "ok"
    return "ok" if monad.is_right() else "fail"
