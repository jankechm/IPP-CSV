import sys
"""move the script path to the end of the sys.path to enable access
to std module csv"""
sys.path.append(sys.path.pop(0))
import csv

class Converter(object):
    """Convertor of CSV to XML"""

    def __init__(self, args):
        self._args = args
        print(args)
        print(csv.list_dialects())
