"""
Core functions for AutoSeachLib.
"""


def hello_world() -> str:
    """Print and return a hello world greeting.

    Returns:
        str: The greeting message.

    Example:
        >>> hello_world()
        Hello World from AutoSeachLib!
        'Hello World from AutoSeachLib!'
    """
    message = "Hello World from AutoSeachLib!"
    print(message)
    return message


def add_strings(a: str, b: str) -> str:
    """Concatenate two strings together.

    Args:
        a: The first string.
        b: The second string.

    Returns:
        str: The concatenated result of a and b.

    Raises:
        TypeError: If either argument is not a string.

    Example:
        >>> add_strings("Hello, ", "World!")
        'Hello, World!'
    """
    if not isinstance(a, str):
        raise TypeError(f"Expected str for argument 'a', got {type(a).__name__}")
    if not isinstance(b, str):
        raise TypeError(f"Expected str for argument 'b', got {type(b).__name__}")
    return a + b
