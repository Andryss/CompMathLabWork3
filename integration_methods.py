from functions import *


class IntegrationResult:
    integral_value: float
    number_of_steps: int
    is_integrated_with_dead_points: bool

    def __init__(self, iv, nos, iiwdp):
        self.integral_value = iv
        self.number_of_steps = nos
        self.is_integrated_with_dead_points = iiwdp


class IntegrationMethod:
    _string: str = ""

    def integrate(self, func: Function, left: float, right: float, number_of_steps: int = 4) -> float:
        raise Exception("Method isn't overridden")

    @staticmethod
    def has_dead_points_on_interval(func: Function, left: float, right: float) -> bool:
        for point in func.dead_points():
            if left <= point.value <= right:
                return True
        return False

    def integrate_with_precision(self, func: Function, left: float, right: float, precision: float,
                                 start_number_of_steps: int = 4, steps_limit: int = 1_000_000) -> IntegrationResult:
        assert left < right, "Invalid interval"
        if IntegrationMethod.has_dead_points_on_interval(func, left, right):
            return IntegrationResult(
                IntegrationMethod.integrate_with_dead_points(func, left, right),
                None,
                True
            )
        prev_result: float = self.integrate(func, left, right, number_of_steps=start_number_of_steps)
        cur_result: float
        while start_number_of_steps < steps_limit:
            start_number_of_steps *= 2
            cur_result = self.integrate(func, left, right, number_of_steps=start_number_of_steps)
            if abs(prev_result - cur_result) <= precision:
                return IntegrationResult(
                    cur_result,
                    start_number_of_steps,
                    False
                )
            prev_result = cur_result
        raise Exception(f"Can't reach precision {precision}")

    @staticmethod
    def integrate_with_dead_points(func: Function, left: float, right: float) -> float:
        points = [left]
        for dead_point in func.dead_points():
            if dead_point.value < left or dead_point.value > right:
                continue
            if dead_point.left_func is None or dead_point.right_func is None:
                raise Exception(f"Integral doesn't exists at point {dead_point.value}")
            points.append(dead_point)
        points.append(right)
        result = 0.0
        for i in range(1, len(points) - 1):
            helper = points[i]

            if isinstance(points[i-1], DeadPointIntegrationHelper):
                result += helper.left_func(points[i-1].value + (helper.value - points[i-1].value)/2)
            else:
                result += helper.left_func(points[i-1])

            if isinstance(points[i+1], DeadPointIntegrationHelper):
                result += helper.right_func(helper.value + (points[i+1].value - helper.value)/2)
            else:
                result += helper.right_func(points[i+1])
        return result

    def __str__(self):
        return self._string


class LeftRectangleMethod(IntegrationMethod):
    _string: str = "left rectangle method"

    def integrate(self, func: Function, left: float, right: float, number_of_steps: int = 4) -> float:
        assert number_of_steps != 0, "0 number of steps?????"
        step: float = (right - left) / number_of_steps
        start: float = left
        result: float = 0
        for i in range(number_of_steps):
            result += func.at(start)
            start += step
        return result * step


class RightRectangleMethod(IntegrationMethod):
    _string: str = "right rectangle method"

    def integrate(self, func: Function, left: float, right: float, number_of_steps: int = 4) -> float:
        assert number_of_steps != 0, "0 number of steps?????"
        step: float = (right - left) / number_of_steps
        start: float = left + step
        result: float = 0
        for i in range(number_of_steps):
            result += func.at(start)
            start += step
        return result * step


class MiddleRectangleMethod(IntegrationMethod):
    _string: str = "middle rectangle method"

    def integrate(self, func: Function, left: float, right: float, number_of_steps: int = 4) -> float:
        assert number_of_steps != 0, "0 number of steps?????"
        step: float = (right - left) / number_of_steps
        start: float = left + step / 2
        result: float = 0
        for i in range(number_of_steps):
            result += func.at(start)
            start += step
        return result * step


class TrapezoidMethod(IntegrationMethod):
    _string: str = "trapezoid method"

    def integrate(self, func: Function, left: float, right: float, number_of_steps: int = 4) -> float:
        assert number_of_steps != 0, "0 number of steps?????"
        step: float = (right - left) / number_of_steps
        start: float = left + step
        result: float = func.at(left) + func.at(right)
        for i in range(number_of_steps - 1):
            result += 2 * func.at(start)
            start += step
        return result * step / 2


class SimpsonMethod(IntegrationMethod):
    _string: str = "simpson method"

    def integrate(self, func: Function, left: float, right: float, number_of_steps: int = 4) -> float:
        assert number_of_steps % 2 == 0, "can use only even number_of_steps in this method"
        assert number_of_steps != 0, "0 number of steps?????"
        step: float = (right - left) / number_of_steps
        start: float = left + step
        result: float = func.at(left) + func.at(right)
        is_doubled: bool = True
        for i in range(number_of_steps - 1):
            result += 2 * (2 * func.at(start) if is_doubled else func.at(start))
            is_doubled = not is_doubled
            start += step
        return result * step / 3


def get_all_methods() -> list[IntegrationMethod]:
    return [
        LeftRectangleMethod(),
        RightRectangleMethod(),
        MiddleRectangleMethod(),
        TrapezoidMethod(),
        SimpsonMethod()
    ]
