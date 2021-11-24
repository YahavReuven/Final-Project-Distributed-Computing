from parallelize import Distribute
import hashlib
import math

@Distribute('alex', range(10**8), 10**6, './Results', modules=['math'])
class bruteforce:
    results = {}

    @classmethod
    def parallel_func(cls, number):
        for i in range(2, int(math.sqrt(number) + 1)):
            if number % i == 0:
                return False
        results[number] = True
        return True


# @Distribute('alex', range(40), 10, './Results', modules=['math'])
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

    # @staticmethod
    # def stop_func(str_num):
    #     num = int((str_num.split("-"))[1])
    #     return num == 10


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
project = bruteforce()

input('2')
b = project.get_results()
print(b)