#!/usr/bin/env python3.6

import sys
"""move the script path to the end of the sys.path to enable access
to std module csv"""
sys.path.append(sys.path.pop(0))
import src.paramparse as paramparse
import src.csv_input as csv_input
import src.xml_output as xml_output

"""seznam = [1, 5, 2, 4, 6, 3]
for index in range(len(seznam)):
    seznam[index] = seznam[index] + 1
print(seznam)"""

parser = paramparse.ParamParser()
parser.parse()
args = parser.processed_args

csv = csv_input.CSV(args)
csv.open()
table = csv.read()

xml = xml_output.XML(args, table)
xml.open()
xml.write()
