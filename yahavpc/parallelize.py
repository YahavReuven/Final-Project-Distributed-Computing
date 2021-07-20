# TODO: change name of file
import csv
from itertools import islice
import sys
from typing import Callable
from collections.abc import Iterable  # TODO: maybe also Callable

import manager
import consts
from consts import Returns

iteration_manager = manager.IterationManager()


def init():
    # TODO: load json containing information
    iteration_manager.task_number = 0  # TODO: get from json sent with the code
    iteration_manager.results_path = "./test"  # TODO: change demo path


def pmap_function(fn: Callable, iterable: Iterable, iteration_size: int, *, stop_function: Callable = None, **kwargs) -> Returns:

    iteration_manager.iteration_size = iteration_size

    sliced_iterable = islice(iterable, iteration_manager.start, iteration_manager.end)

    results_full_path = iteration_manager.results_path + consts.RESULTS_NAME_AND_TYPE
    with open(results_full_path, 'w') as results_file:
        # TODO: when there isn't such directory

        writer = csv.writer(results_file)
        headers = consts.RESULTS_HEADERS
        writer.writerow(headers)

        iteration_index = iteration_manager.start  # TODO: a bit ugly

        for parameter_value in sliced_iterable:
            computed_return_value = fn(parameter_value, **kwargs)

            if stop_function:
                result = stop_function(computed_return_value)
                if result:
                    writer.writerow((iteration_index, computed_return_value))
                    return Returns.stopped
                iteration_index += 1
                continue

            writer.writerow((iteration_index, computed_return_value))
            iteration_index += 1

        if iteration_index < iteration_manager.end - 1:
            return Returns.exhausted

        return Returns.normal



def pmap(fn: Callable, iterable: Iterable, iteration_size: int, *, stop_function: Callable = None, **kwargs):
    result = pmap_function(fn, iterable, iteration_size, stop_function=stop_function, **kwargs)
    print(result)
    # TODO: write result to file
    sys.exit()



# ----------------------------------------------------------------------------------------------
#
#   test
#
#



# ------------ test -------------------
# def test(number, b):
#     return number
#
# def stop(number):
#     return number == 3
#
# init()
#
# pmap(test, range(10), 6, stop_function=stop, b="hi")
# print('hello')




