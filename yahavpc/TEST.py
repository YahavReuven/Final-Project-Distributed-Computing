from parallelize import Distribute

import math


@Distribute('alex', range(40), 10, './Results', modules=['math'])
class A:

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

    @staticmethod
    def stop_func(num):
        return num % 2 == 0


# class A:
#
#     @classmethod
#     def parallel_func(cls, number):
#         print(math.sqrt(9))
#         cls.b(number)
#         return f'{int(number/10)}-{number}'
#
#     @staticmethod
#     def b(number):
#         print(math.sqrt(4))
#         with open(f'./task/additional_results/{int(number/10)}-{number}.txt', 'w') as file:
#             file.write("hello: " + str(number))
#
#
input('1')
project = A()

input('2')
b = project.get_results()
print(b)