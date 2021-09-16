from parallelize import Distribute, importer
import importer_DELETE

import os
import math


@Distribute('alex', range(40), 10, './Results', modules=['math'])
class A:

    modules = ['math']

    @classmethod
    def parallel_func(cls, number):
        print(math.sqrt(9))
        cls.b(number)
        return f'{int(number/10)}-{number}'

    @staticmethod
    def b(number):
        print(math.sqrt(4))
        with open(f'./task/additional_results/{int(number/10)}-{number}.txt', 'w') as file:
            file.write("hello: " + str(number))

input('1')
project = A()

input('2')
project.get_results()