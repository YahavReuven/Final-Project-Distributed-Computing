from parallelize import Distribute
import hashlib
import math
import time
import string
import itertools

# broutefore_iterator = itertools.product(string.ascii_letters + string.digits, repeat=6)
# @Distribute('alex', broutefore_iterator, int(1.5e8), './Results', parallel_func='create_hash',
#             stop_func='check_pass', modules=['hashlib'])
# class Brouteforce:
#     pass_hash = 'ff37814ec1f367f9b0c9fc6b16db6fba'
#
#     @classmethod
#     def create_hash(cls, guess):
#         guess = ''.join(guess)
#         end_pwd = guess.encode('utf-8')
#         digest = hashlib.md5(end_pwd.strip()).hexdigest()
#         return digest
#
#     @classmethod
#     def check_pass(cls, digset):
#         return digset == cls.pass_hash



@Distribute('beni', range(10**8), 10**6, './Results', parallel_func='is_prime', only_if_func='write_num')
class PrimesBellowN:

    @classmethod
    def is_prime(cls, number: int):
        for i in range(2, int(number**0.5 + 1)):
            if number % i == 0:
                return False
        return True

    @staticmethod
    def write_num(prime: bool):
        return prime


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


input('1')
start = time.time()
project = PrimesBellowN()
middle = time.time()
input('2')
end = time.time()
print(end-start, middle-start)

results = project.get_results()
print(results)