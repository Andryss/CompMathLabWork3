import math
from typing import Callable


class DeadPointIntegrationHelper:
    value: float
    left_func: Callable[[float], float]
    right_func: Callable[[float], float]

    def __init__(self, p, lf, rf):
        self.value = p
        self.left_func = lf
        self.right_func = rf


class Function:
    _string: str = ""
    _func: Callable[[float], float] = lambda x: 0
    _dead_points: list[DeadPointIntegrationHelper] = []
    _image: str = ""

    def __init__(self, s, f, d, i):
        self._string = s
        self._func = f
        self._dead_points = d
        self._image = i

    def at(self, x: float) -> float:
        if x in self._dead_points:
            raise Exception(f"Can't calculate function at {x}")
        return self._func(x)

    def dead_points(self) -> list[DeadPointIntegrationHelper]:
        return self._dead_points

    def image_path(self) -> str:
        return self._image

    def __str__(self):
        return "function: (" + self._string + ")"


def _get_polynomial_function() -> Function:
    return Function(
        "3 * x^3 - 4 * x^2 + 7 * x - 17",
        lambda x: 3 * x**3 - 4 * x**2 + 7 * x - 17,
        [],
        "images/0.png"
    )


def _get_trigonometric_function() -> Function:
    return Function(
        "cos(x^2)",
        lambda x: math.cos(x ** 2),
        [],
        "images/1.png"
    )


def _get_exponential_function() -> Function:
    return Function(
        "e^(-x^2/2) - 0.5",
        lambda x: math.exp(- x**2 / 2) - 0.5,
        [],
        "images/2.png"
    )


def _get_not_integrateable_function() -> Function:
    return Function(
        "1/((x-1) * (x-2) * (x-3))",
        lambda x: 1 / ((x-1) * (x-2) * (x-3)),
        [
            DeadPointIntegrationHelper(1, None, None),
            DeadPointIntegrationHelper(2, None, None),
            DeadPointIntegrationHelper(3, None, None)
        ],
        "images/3.png"
    )


def _get_square_function() -> Function:
    return Function(
        "1/cbrt(3 - 4x)",
        lambda x: 1/((3 - 4*x) ** (1/3)),
        [
            DeadPointIntegrationHelper(
                3/4,
                lambda x: 3/8 * (3 - 4*x)**(2/3),
                lambda x: -3/8 * (4*x - 3)**(2/3)
            )
        ],
        "images/4.png"
    )


def get_all_functions() -> list[Function]:
    return [
        _get_polynomial_function(),
        _get_trigonometric_function(),
        _get_exponential_function(),
        _get_not_integrateable_function(),
        _get_square_function()
    ]
