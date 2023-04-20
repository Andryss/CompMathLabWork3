import math
from typing import Callable


class Function:
    _string: str = ""
    _func: Callable[[float], float] = lambda x: 0
    _dead_points: list[float] = []

    def __init__(self, s, f, d):
        self._string = s
        self._func = f
        self._dead_points = d

    def at(self, x: float) -> float:
        if x in self._dead_points:
            raise Exception(f"Can't calculate function at {x}")
        return self._func(x)

    def dead_points(self) -> list[float]:
        return self._dead_points

    def __str__(self):
        return "function: (" + self._string + ")"


def _get_polynomial_function() -> Function:
    return Function(
        "3 * x^3 - 4 * x^2 + 7 * x - 17",
        lambda x: 3 * x**3 - 4 * x**2 + 7 * x - 17,
        []
    )


def _get_trigonometric_function() -> Function:
    return Function(
        "cos(x^2)",
        lambda x: math.cos(x ** 2),
        []
    )


def _get_exponential_function() -> Function:
    return Function(
        "e^(-x^2/2) - 0.5",
        lambda x: math.exp(- x**2 / 2) - 0.5,
        []
    )


def _get_not_integrateable_function() -> Function:
    return Function(
        "1/((x-1) * (x-2) * (x-3))",
        lambda x: 1 / ((x-1) * (x-2) * (x-3)),
        [1, 2, 3]
    )


def get_all_functions() -> list[Function]:
    return [
        _get_polynomial_function(),
        _get_trigonometric_function(),
        _get_exponential_function(),
        _get_not_integrateable_function()
    ]
