# TODO: change name of file
import csv
from itertools import islice

import manager

iteration_manager = manager.IterationManager()
iteration_manager.iteration_number = 0 #TODO: get from json sent with the code
iteration_manager.results_path = "C:\\Projects\\python\\final_project\\" #TODO: change demo path

# def init()
#    global iteration_manager


def pmap(fn, iterable, iteration_size, *args, **kwargs):

    global iteration_manager



    iteration_manager.iteration_size = iteration_size

    sliced_iterable = islice(iterable, iteration_manager.start, iteration_manager.end)

    with open(iteration_manager.results_path + "results.csv", 'w') as results:  # TODO: when there isn't such directory
        writer = csv.writer(results)
        headers = ["ITERATION", "RETURN_VALUE"]  # TODO: not sure if to keep here or move to iteration manager
        writer.writerow(headers)

        iteration_index = iteration_manager.start  # TODO: a bit ugly

        for parameter_value in sliced_iterable:
            computed_return_value = fn(parameter_value, *args, **kwargs)
            # print(computed_return_value)
            writer.writerow((iteration_index, computed_return_value))
            iteration_index += 1





#----------------------------------------------------------------------------------------------
#
#   test
#
#



# ------------ test -------------------
# def test(number, a, b):
#     return number
#
#
# pmap(hello, range(10), 5, 4, b="hi")




