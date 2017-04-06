import argparse
import sys
import re

import err

class ArgumentParser(argparse.ArgumentParser):
    """Extends the argparse.ArgumentParser class to override
       the behavior of the error method"""

    def error(self, message):
        err.Error.terminate(
            f'{self.prog} error: {message}\n\n', err.Error.ErrorCodes.BAD_ARGS)

class ParamParser(object):
    """Parser of the script input options"""

    __ELEM_REGEX = r"(?!(xml))[a-z][\w\-.]*"
    
    def parse(self):
        self.__parser = ArgumentParser(
            add_help=False, allow_abbrev=False,
            description="Converts CSV file to XML file")
        self.add_args()
        self.__params = self.__parser.parse_args()
        self.process_args()
    
    def add_args(self):
        self.__parser.add_argument(
            '--help', action="store_true", help='show this help message')
        self.__parser.add_argument(
            '--input', type=argparse.FileType('r'), default=sys.stdin,
            metavar='filename', help='input file address (default: stdin)')
        self.__parser.add_argument(
            '--output', type=argparse.FileType('w'), default=sys.stdout,
            metavar='filename', help='output file address (default: stdout)')
        self.__parser.add_argument(
            '-n', action='store_true', help='do not generate XML header')
        self.__parser.add_argument(
            '-r', metavar='root-element', help='name of the XML root element')
        self.__parser.add_argument(
            '-s', default=',', metavar='separator',
            help='separator of the CSV cells')
        self.__parser.add_argument(
            '-h', nargs='?', const='-', metavar='subst',
            help='consider the first record as a CSV header; '
                'replace invalid chars by subst value (default: -)')
        self.__parser.add_argument(
            '-c', default='col', metavar='column-element',
            help='prefix of the element for the unnamed cells')
        self.__parser.add_argument(
            '-l', metavar='line-element',
            help='name of the element for CSV lines')
        self.__parser.add_argument(
            '-i', action='store_true',
            help='add attribute "index" to line-element')
        self.__parser.add_argument(
            '--start', nargs='?', const='1', metavar='n', type=int,
            help='set the counter of the index attr to n (default: 1)')
        self.__parser.add_argument(
            '-e', '--error-recovery', action='store_true',
            help='recover from bad number of columns in the CSV header')
        self.__parser.add_argument(
            '--missing-field', metavar='val',
            help='value for the empty fields; option -e required')
        self.__parser.add_argument(
            '--all-columns', action='store_true', 
            help='even the extra columns are included in the output XML; '
                'option -e required')

    def process_args(self):
        print(self.__params)
        if (self.__params.help):
            if (len(sys.argv) == 2):
                self.__parser.print_help()
            else:
                err.Error.terminate(
                    'Do not combine any args with --help\n\n',
                    err.Error.ErrorCodes.BAD_ARGS)
        if (self.__params.r):
            self.__process_arg(
                '-r', self.__params.r, self.__ELEM_REGEX,
                err.Error.ErrorCodes.BAD_XML_ELEM)
        if (self.__params.h):
            self.__process_arg(
                '-h', self.__params.h, '[\w\-.]',
                err.Error.ErrorCodes.BAD_XML_ELEM_SUBSTITUTED)
        if (self.__params.c):
            self.__process_arg(
                '-c', self.__params.c, self.__ELEM_REGEX,
                err.Error.ErrorCodes.BAD_XML_ELEM)
        if (self.__params.l):
            self.__process_arg(
                '-l', self.__params.l, self.__ELEM_REGEX,
                err.Error.ErrorCodes.BAD_XML_ELEM)
        else:
            self.__line_elem = 'row'
        if (self.__params.i):
            if (self.__params.l):
                self.__index_attr = 'index'
                self.__index_attr_cnt = '1'
                print('-i OK')
            else:
                err.Error.terminate(
                    '-i must be combined with -l\n\n',
                    err.Error.ErrorCodes.BAD_ARGS)
        if (self.__params.start):
            if (self.__params.i and self.__params.l):
                self.__index_attr_cnt = str(self.__params.i)
                print('--start OK')
            else:
                err.Error.terminate(
                    '--start must be combined with -l and -i\n\n',
                    err.Error.ErrorCodes.BAD_ARGS)
        self.__error_recovery = self.__params.error_recovery
        print(f'-e {self.__error_recovery}')
        if (self.__params.missing_field):
            if (self.__params.error_recovery):
                self.__missing_field = self.__params.missing_field
                print('--missing-field OK')
            else:
                err.Error.terminate(
                    '--missing-field must be combined with -e\n\n',
                    err.Error.ErrorCodes.BAD_ARGS)
        if (self.__params.all_columns):
            if (self.__params.error_recovery):
                self.__all_cols = True
                print('--all-cols OK')
            else:
                err.Error.terminate(
                    '--all-columns must be combined with -e\n\n',
                    err.Error.ErrorCodes.BAD_ARGS)

    def __process_arg(self, arg, arg_val, regex, err_code):
        match = re.fullmatch(regex, arg_val, re.I)
        if (match is None):
            err.Error.terminate(
                f'Bad value for {arg}\n\n', err_code)
        else:
            print(f'{arg} OK')
