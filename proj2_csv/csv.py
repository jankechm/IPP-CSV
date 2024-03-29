#!/usr/bin/env python3.6

import sys
"""move the script path to the end of the sys.path to enable access
to std module csv"""
sys.path.append(sys.path.pop(0))
import src.paramparse as paramparse
import src.csv_input as csv_input
import src.xml_output as xml_output

parser = paramparse.ParamParser()
ops = parser.parse()

csv = csv_input.CSV(ops)
csv.open()
data = csv.load_data()

xml = xml_output.XML(ops)
xml.open()
xml.write_data(data)
