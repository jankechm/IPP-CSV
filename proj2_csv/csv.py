#!/usr/bin/env python3

#import numpy as np

import paramparse


print("Hello world")
a = 5
print(a)
"""Komentar
hkjh"""
#kinosal = np.zeros((5, 5), dtype=int)
"""kinosal = []
kinosal[2, 2] = 1
kinosal[3, 1:4] = 1
kinosal[4, :] = 1
print(kinosal)"""

"""name = "Marek"
print (f"Hi {name}, how are you?")

seznam = [1, 5, 2, 4, 6, 3]
for index in range(len(seznam)):
    seznam[index] = seznam[index] + 1
print(seznam)"""

parser = paramparse.ParamParser()
parser.parse()