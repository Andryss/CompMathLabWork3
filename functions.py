from typing import Callable


class Function:
    _string: str = ""
    _func: Callable[[float], float] = lambda x: 0

    def __init__(self, s, f):
        self._string = s
        self._func = f

    def at(self, x: float) -> float:
        return self._func(x)

    def __str__(self):
        return "function: (" + self._string + ")"


def _get_polynomial_function() -> Function:
    return Function(
        "3 * x^3 - 4 * x^2 + 7 * x - 17",
        lambda x: 3 * x**3 - 4 * x**2 + 7 * x - 17
    )


# def _get_trigonometric_function() -> Function:
#     return Function(
#         "cos(x^2)",
#         lambda x: math.cos(x ** 2)
#     )
#
#
# def _get_exponential_function() -> Function:
#     return Function(
#         "e^(-x^2/2) - 0.5",
#         lambda x: math.exp(- x**2 / 2) - 0.5
#     )


def get_all_functions() -> list[Function]:
    return [
        _get_polynomial_function(),
        # _get_trigonometric_function(),
        # _get_exponential_function()
    ]
