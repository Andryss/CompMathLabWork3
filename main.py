import sys
import numpy as np
import pandas as pd

from functions import *
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


def read_interval() -> [float, float]:
    line = input("\nEnter the interval boundaries:\n").strip()
    interval: [float, float]
    try:
        interval = [float(x) for x in line.split()]
        if len(interval) != 2 or interval[1] < interval[0]:
            raise Exception("not an interval")
    except Exception as _:
        interval = read_interval_from_file(line)
    return interval


def read_interval_from_file(filename: str):
    frame: pd.DataFrame
    try:
        frame = pd.read_csv(filename, header=None)
        validate_interval_precision(frame)
    except Exception as e:
        raise Exception("file \"" + filename + "\" can't be opened: " + e.__str__())
    return frame.values


def validate_interval_precision(frame: pd.DataFrame):
    if len(frame) != 1 or len(frame[0]) != 2 or not isinstance(frame[0][0], np.float) \
            or not isinstance(frame[0][1], np.float) or frame[0][1] < frame[0][0]:
        raise Exception("must contains only two float numbers (forming interval)")


def read_precision() -> float:
    line = input("\nEnter the precision:\n").strip()
    precision: float
    try:
        precision = float(line)
        if precision <= 0:
            raise Exception("precision must be positive")
    except Exception as _:
        precision = read_precision_from_file(line)
    return precision


def read_precision_from_file(filename: str):
    frame: pd.DataFrame
    try:
        frame = pd.read_csv(filename, header=None)
        validate_file_precision(frame)
    except Exception as e:
        raise Exception("file \"" + filename + "\" can't be opened: " + e.__str__())
    return frame[0][0]


def validate_file_precision(frame: pd.DataFrame):
    if len(frame) != 1 or len(frame[0]) != 1 or not isinstance(frame[0][0], np.float) or frame[0][0] <= 0:
        raise Exception("must contains only one number (positive float)")


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
        [left, right] = read_interval()

        precision: float = read_precision()
        method: IntegrationMethod = choose_method()
        [result, number_of_steps] = method.integrate_with_precision(function, left, right, precision=precision)
        print_result(method, number_of_steps, result)
    except Exception as e:
        print(e, file=sys.stderr)


if __name__ == '__main__':
    run()
