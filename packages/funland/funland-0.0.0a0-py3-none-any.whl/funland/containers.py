"""
Handy containers \n
for functional chaining in \n
python codebases.
"""
from functools import reduce
from typing import (
    Any,
    Callable,
    Generator,
    Generic,
    Optional,
    Type,
    TypeVar,
    Union,
    List,
    Tuple,
)

T = TypeVar("T")
U = TypeVar("U")

DEFAULT = object()


class Container(Generic[T]):
    """
    Simple container (and parent class for all other containers)

    No additional work is handled on function calls, apart from returning
    a new container with an updated result. Essentially, this container
    just allows for a nice api for function chaining.

    It can be used like so:

    ```python
    def make_loud(x: str) -> str:
        return x.upper() + "!!!"

    x = (
        Container("hello world!")
        .map(make_loud)
        .unwrap()
    )

    print(x)
    # >> prints out "HELLO WORLD!!!!"
    ```
    """


    def __init__(self: Any, *values: T) -> None:
        """
        Initialise a monad with the given list
        """
        self.value: List[T]
        if len(values) == 1 and isinstance(values[0], Generator):
            self.value = list(values[0])
        else:
            self.value = list(values)

    def map(
        self,
        func: Union[Callable[..., T], Tuple[Callable[..., T], Union[int, str]]],
        *args,
        **kwargs,
    ) -> "Container":
        """

        Apply function to the container's value. Any additional positional
        or keyword arguments are passed into the function call.

        Standard use:
        ```python
        def say_hello(name: str, greeting: str = "Yo") -> str:
            return greeting + " " + name

        x = (
            Container("Joe")
            .map(say_hello)
        )

        x == Container("Yo Joe")
        ```

        The container's value will by default be passed in as the first
        positional argument. You can override this behaviour by giving
        a tuple of a function and the position (zero indexed as int) or
        keyword (as str) to pass in the value as.

        For instance:
        ```python
        def say_hello(name: str, greeting: str = "Yo") -> str:
            return greeting + " " + name

        x = (
            Container("Hi")
            .map((say_hello, "greeting"), name="Rye")
        )

        y = (
            Container("Hi")
            .map((say_hello, 1), "Rye")
        )

        x == Container("Hi Rye") == y
        ```
        """
        return Container(
            self._value_map(i, func, *args, **kwargs) for i in self.value
        )

    def filter(self, func: Callable, *args, **kwargs) -> "Container":
        """
        Filter list to only elements with truthy return:

        ```python
        x = (
            Array(1, 2, 3, 4)
            .filter(lambda x: x % 2 == 0)
        )

        x == Array(2, 4)
        ```

        Note that you can use the same keyword and positional argument logic
        that words with `map` for containers:

        ```python
        def no_remainder(divide_by: int, value: int) -> bool:
            return value % divide_by == 0

        x = (
            Array(1, 2)
            .filter((no_remainder, "value"), divide_by=2)
        )

        x == Array(2)
        ```
        """
        return Container(
            i for i in self.value if self._value_map(i, func, *args, **kwargs)
        )

    def reduce(self, func: Callable, initial: Any = None) -> "Container":
        """
        Applies reduce over list, returning result
        in a Container.

        Optional `initial` argument to pass down into reduce.
        """
        if initial is None:
            return Container(reduce(func, self.value))
        return Container(reduce(func, self.value, initial))

    def _value_map(
        self,
        value,
        func: Union[Callable[..., T], Tuple[Callable[..., T], Union[int, str]]],
        *args,
        **kwargs,
    ) -> T:
        """
        Internal function, applies "map" to contained value, not returning
        the value in a container. This means any additional work can be handled
        by parent classes, without having to handle the argument and keyword argument
        passing in of values.

        Usage note: This *doesn't* get value from `self.value` and instead expects
        it to passed in as an argument. This is for calls within children like Array
        where it may be used on objects other than the value.
        """
        args_list: list = list(args)
        if isinstance(func, tuple):
            func, keyword = func
            if isinstance(keyword, int):
                args_list.insert(keyword, value)
            else:
                kwargs = {keyword: value} | kwargs
            return func(*args_list, **kwargs)
        return func(value, *args_list, **kwargs)


    def unwrap(self) -> T:
        """
        Return the container's value.

        ```python
        Container(4).unwrap() == 4
        ```
        """
        return self.value

    def __eq__(self, other: Any) -> bool:
        """
        Equality operator, true if containers are of same type
        and values are equal.
        """
        if not isinstance(other, type(self)):
            return False
        return self.value == other.value

    def __str__(self) -> str:
        """
        String representation
        """
        return f"{self.__class__.__name__}({', '.join(str(i) for i in self.value)})"

    def __repr__(self) -> str:
        """
        Representaion for REPLs
        """
        return self.__str__()


class Maybe(Container, Generic[T]):
    """
    Container to handle None values.

    Write functions without considering possibility of None values.
    If Container value is None, it will skip execution of function and
    remain as None.

    Simple example:
    ```python
    nope = (
        Maybe(None, 4)
        .map(lambda x: x + 3)
        .unwrap()
    )

    nope == [None, 7]
    ```

    For Maybe containers, `unwrap` can additionally be given an "or"
    value which will be defaulted to if containers value is None.
    """

    def map(
        self,
        func: Union[Callable[..., T], Tuple[Callable[..., T], Union[int, str]]],
        *args,
        **kwargs,
    ) -> "Maybe":
        """
        Execute function on value, unless None in which case
        execution is skipped.

        (see Container 'map' documentation for more details)
        """
        return Maybe(
            self._value_the(i, func, *args, **kwargs) if i is not None
            else None for i in self.value
        )

    def unwrap(self, default: Optional[U] = None) -> Union[T, U, None]:
        """
        Return the container's value.

        ```python
        Maybe(4).unwrap() == [4]
        ```

        ```python
        Maybe(None).unwrap(default=3) == [3]
        """
        return [i if i is not None else default for i in self.value]



class Result(Container, Generic[T]):
    """
    Container to handle errors. Handle exceptions on unwrap:

    ```python
    x = (
        Result(3)
        .map(lamba x / 0)
    )

    x.unwrap() # thows ZeroDivisionError
    x.unwrap_or(4) == 4
    ```
    """
    _error: List[Optional[Exception]] = None

    def map(self, func, *args, **kwargs) -> "Result":
        """
        Execute function on value, if error is raised,
        returned Monad will have value of "None" and an exception.

        Otherwise, exception will be None, and value will be return.

        If exception already exists, function won't be executed.

        Note, that this container does not in itself protect you from
        mutation, if you're function mutates the value into a
        non-recoverable state, this could cause errors.

        To avoid mutation, see mutation_free wrapper in metafunctions.
        """
        new_values = []
        exceptions = []

        for value in self.values:
            try:
                new_values.append(self._value_map(value, func, *args, **kwargs))
                exceptions.append(None)
            except Exception as exception:
                new_values.append(None)
                exceptions.append(exception)

        return_container = Result(*new_values)
        return_container._exceptions = exceptions

        return return_container

    def unwrap(self, default: Any = DEFAULT, *exceptions: Type[Exception]) -> T:
        """
        If exception has not been raise, will return value, otherwise
        if no default is given, will raise the last exception.

        Exceptions can be handled by passing in a default like so:
        ```python
        zero_problem = (
            Result(3)
            .map(lambda x: x/0)
            .unwrap(default=4)
        )
        zero_problem == 4
        ```

        Catching *all* exceptions is unlikely to be what you want to do
        in most cases, in which case you can specify the exceptions you
        want to catch:

        ```python
        zero_problem = (
            Result(3)
            .map(lambda x: x/0)
            .unwrap(default=4, ZeroDivisionError, AssertionError)
        )
        zero_problem == 4
        ```
        """
        if self.exception is None:
            return self.value
        if default is DEFAULT:
            raise self.exception
        if not exceptions:
            return default
        if type(self.exception) in exceptions:
            return default
        raise self.exception

    def recover(self, func) -> "Result":
        """
        If Result is in error state, apply function to last
        non-error state value.

        Example:
        ```python
        x = (
            Result(3)
            .map(lamba x: x / 0)
            .recover(lambda x: x + 1)
        )
        x == 4  # <- recover function applied to 3
        ```
        """
        raise NotImplementedError

    def in_error_state(self) -> bool:
        """
        Function to return bool based on whether container is
        in error state from previous error.

        Returns True if in error state, and False otherwise.
        """
        return self.exception is not None

    def __str__(self) -> str:
        """
        Custom string representation
        """
        return "NOT-IMPLEMENTED-YET"
