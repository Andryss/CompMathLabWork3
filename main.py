import sys
from PIL import Image

from integration_methods import *


def choose_function() -> Function:
    functions: list[Function] = get_all_functions()
    print("\nChoose the function you want to integrate:")
    for i, function in enumerate(functions):
        print(str(i) + "\t" + function.__str__())
    line = input("(enter the number) ").strip()
    try:
        idx = int(line)
        if idx < 0 or idx >= len(functions):
            raise Exception("not such function")
        return functions[idx]
    except Exception as e:
        raise Exception("can't choose the function: " + e.__str__())


def show_function(function: Function):
    try:
        image = Image.open(function.image_path())
        image.show(function.__str__())
        print(f"\nI drawn a plot for you, look at It before continue.")
    except Exception as e:
        print(f"\nI can't a plot for you: {e.__str__()}")


def read_interval() -> [float, float]:
    line = input("\nEnter the interval boundaries:\n").strip()
    interval = [float(x) for x in line.split()]
    if len(interval) != 2 or interval[1] < interval[0]:
        raise Exception("not an interval")
    return interval


def read_precision() -> float:
    line = input("\nEnter the precision:\n").strip()
    precision = float(line)
    if precision <= 0:
        raise Exception("precision must be positive")
    if precision <= 1e-15:
        raise Exception("precision is too small")
    return precision


def choose_method() -> IntegrationMethod:
    methods: list[IntegrationMethod] = get_all_methods()
    print("\nChoose the method you want to use:")
    for i, method in enumerate(methods):
        print(str(i) + "\t" + method.__str__())
    line = input("(enter the number) ").strip()
    try:
        idx = int(line)
        if idx < 0 or idx >= len(methods):
            raise Exception("not such method")
        return methods[idx]
    except Exception as e:
        raise Exception("can't choose the method: " + e.__str__())


def print_result(method: IntegrationMethod, number_of_steps: int, result: float):
    print("\nHere is the computation result:")
    print(f"In case of using {method}:")
    print(f"1) interval was divided into {number_of_steps} parts")
    print(f"2) integral is equal to {result}")


def run():
    try:
        function: Function = choose_function()
        show_function(function)
        [left, right] = read_interval()

        precision: float = read_precision()
        method: IntegrationMethod = choose_method()
        [result, number_of_steps] = method.integrate_with_precision(function, left, right, precision=precision)
        print_result(method, number_of_steps, result)
    except Exception as e:
        print(e, file=sys.stderr)


if __name__ == '__main__':
    run()
