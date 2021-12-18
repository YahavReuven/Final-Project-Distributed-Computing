from parallelize import Distribute
import hashlib
import math
import time
import string
import itertools

broutefore_iterator = itertools.product(string.digits + string.ascii_letters, repeat=2)
@Distribute('alex', broutefore_iterator, 10, './Results', parallel_func='create_hash',
            stop_func='check_pass', modules=['hashlib'])
class Brouteforce:
    pass_hash = '6512bd43d9caa6e02c990b0a82652dca'

    @classmethod
    def create_hash(cls, guess):
        guess = ''.join(guess)
        end_pwd = guess.encode('utf-8')
        digest = hashlib.md5(end_pwd.strip()).hexdigest()
        return digest

    @classmethod
    def check_pass(cls, digset):
        return digset == cls.pass_hash



# @Distribute('alex', range(100), 10, './Results', parallel_func='is_prime', only_if_func='write_num')
# class PrimesBellowN:
#
#     @classmethod
#     def is_prime(cls, number: int):
#         for i in range(2, int(number**0.5 + 1)):
#             if number % i == 0:
#                 return False
#         return True
#
#     @staticmethod
#     def write_num(prime: bool):
#         return prime


# @Distribute('alex', range(40), 10, './Results', parallel_func='main', only_if_func='only', modules=['math'])
# class A:
#
#     @classmethod
#     def main(cls, number):
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
#     @staticmethod
#     def stop(str_num):
#         num = int((str_num.split("-"))[1])
#         return num == 10
#
#     @staticmethod
#     def only(str_num):
#         num = int((str_num.split("-"))[1])
#         return num % 2 == 0


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
start = time.time()
project = Brouteforce()
middle = time.time()
input('2')
end = time.time()
print(end-start, middle-start)

b = project.get_results()
print(b)