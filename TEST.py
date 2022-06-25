import itertools
import string
import hashlib
from yahavdc import Distribute

password_length = 6
bruteforce_iterator = itertools.product(string.ascii_letters +
                                        string.digits, repeat=password_length)


@Distribute('test', bruteforce_iterator, int(1.5e7), './Results',
            parallel_func='create_hash', stop_func='check_pass',
            modules=['hashlib'])
class Bruteforce:
    pass_hash = 'ff37814ec1f367f9b0c9fc6b16db6fba'

    @classmethod
    def create_hash(cls, guess):
        guess = ''.join(guess)
        end_pwd = guess.encode('utf-8')
        digest = hashlib.md5(end_pwd.strip()).hexdigest()
        return digest

    @classmethod
    def check_pass(cls, digest):
        return digest == cls.pass_hash


project = Bruteforce()
input('waiting...')
results = project.get_results()
print(results)
input('code finished')

@staticmethod
# from yahavdc import Distribute
#
#
# @Distribute('alex', range(10 ** 8), 10 ** 6, './Results', parallel_func='is_prime',
#             only_if_func='write_num')
# class PrimesBellowN:
#
#     @classmethod
#     def is_prime(cls, number: int):
#         for i in range(2, int(number ** 0.5 + 1)):
#             if number % i == 0:
#                 return False
#         return True
#
#     @staticmethod
#     def write_num(prime: bool):
#         return prime
#
#
# project = PrimesBellowN()
# results = project.get_results()
# print(results)
# .
#
#
#
# from yahavdc import Distribute
#
#
# @Distribute(...)
# class Project:
#     ...
#
#
# project = Project()
# # Do something
# results = project.get_results()
