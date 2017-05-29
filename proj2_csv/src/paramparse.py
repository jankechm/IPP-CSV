import argparse
import sys
import re

import src.err as err
import src.csv_input as csv_input
import src.xml_output as xml_output

class ArgumentParser(argparse.ArgumentParser):
    """Extends the argparse.ArgumentParser class to override
       the behavior of the error method"""

    def error(self, message):
        err.Error.terminate(
            f'{self.prog} error: {message}\n\n', err.ErrorCodes.ARGS_ERR)

class ParamParser(object):
    """Parser of the script input options"""

    _XML_ELEM_REGEX = r"(?!(xml))[a-z][\w\-.]*"
    _CSV_SEPARATOR_REGEX = r'(.|TAB)'
    _XML_ELEM_SUBST_REGEX = r'[\w\-.]*'

    _processed_args = dict()
    
    def parse(self):
        self._parser = ArgumentParser(
            add_help=False, allow_abbrev=False,
            description="Converts CSV file to XML file")
        self._add_args()
        self._parsed_args = self._parser.parse_args()
        self._process_args()
        return self._processed_args
    
    def _add_args(self):
        self._parser.add_argument(
            '--help', action="store_true", help='show this help message')
        self._parser.add_argument(
            '--input', metavar='filename', help='input file (default: stdin)')
        self._parser.add_argument(
            '--output', metavar='filename',
            help='output file (default: stdout)')
        self._parser.add_argument(
            '-n', action='store_false', help='do not generate XML header')
        self._parser.add_argument(
            '-r', metavar='root-element', help='name of the XML root element')
        self._parser.add_argument(
            '-s', default=',', metavar='separator',
            help='separator of the CSV cells')
        self._parser.add_argument(
            '-h', nargs='?', const='-', metavar='subst',
            help='consider the first record as a CSV header; '
                'replace invalid chars by subst value (default: -)')
        self._parser.add_argument(
            '-c', default='col', metavar='column-element',
            help='prefix of the element for the unnamed cells')
        self._parser.add_argument(
            '-l', metavar='line-element',
            help='name of the element for CSV lines')
        self._parser.add_argument(
            '-i', action='store_true',
            help='add attribute "index" to line-element')
        self._parser.add_argument(
            '--start', nargs='?', const='1', metavar='n', type=int,
            help='set the counter of the index attr to n (default: 1)')
        self._parser.add_argument(
            '-e', '--error-recovery', action='store_true',
            help='recover from bad number of columns in the CSV header')
        self._parser.add_argument(
            '--missing-field', metavar='val',
            help='value for the empty fields; option -e required')
        self._parser.add_argument(
            '--all-columns', action='store_true', 
            help='even the extra columns are included in the output XML; '
                'option -e required')

    def _process_args(self):
        self._process_help()
        self._process_input()
        self._process_output()
        self._process_arg_n()
        self._process_arg_r()
        self._process_arg_s()
        self._process_arg_h()
        self._process_arg_c()
        self._process_arg_l()
        self._process_arg_i()
        self._process_arg_start()
        self._process_arg_e()
        self._process_arg_missing_field()
        self._process_arg_all_columns()

    def _check_arg_val(self, arg, arg_val, regex, err_code):
        match = re.fullmatch(regex, arg_val, re.I)
        if (match is None):
            err.Error.terminate(
                f'Bad value for {arg}\n\n', err_code)

    def _process_help(self):
        if (self._parsed_args.help):
            if (len(sys.argv) == 2):
                self._parser.print_help()
                sys.exit(0)
            else:
                err.Error.terminate(
                    'Do not combine any args with --help\n\n',
                    err.ErrorCodes.ARGS_ERR)

    def _process_input(self):
        self._processed_args['input'] = self._parsed_args.input
       
    def _process_output(self):
        self._processed_args['output'] = self._parsed_args.output

    def _process_arg_n(self):
        self._processed_args['header'] = self._parsed_args.n

    def _process_arg_r(self):
        if (self._parsed_args.r):
            self._check_arg_val(
                '-r', self._parsed_args.r, self._XML_ELEM_REGEX,
                err.ErrorCodes.XML_ELEM_ERR)
            self._processed_args['root_elem'] = self._parsed_args.r
        else:
            self._processed_args['root_elem'] = None

    def _process_arg_s(self):
        if (self._parsed_args.s):
            self._check_arg_val(
                '-s', self._parsed_args.s, self._CSV_SEPARATOR_REGEX,
                err.ErrorCodes.ARGS_ERR)
            if (self._parsed_args.s == 'TAB'):
                self._processed_args['delimiter'] = '\t'
            else:
                self._processed_args['delimiter'] = self._parsed_args.s

    def _process_arg_h(self):
        if (self._parsed_args.h):
            self._check_arg_val(
                '-h', self._parsed_args.h, self._XML_ELEM_SUBST_REGEX,
                err.ErrorCodes.XML_ELEM_SUBSTITUTED_ERR)
            self._processed_args['subst'] = self._parsed_args.h

    def _process_arg_c(self):
        if (self._parsed_args.c):
            self._check_arg_val(
                '-c', self._parsed_args.c, self._XML_ELEM_REGEX,
                err.ErrorCodes.XML_ELEM_ERR)
            self._processed_args['col_elem'] = self._parsed_args.c
        else:
            self._processed_args['col_elem'] = 'col'

    def _process_arg_l(self):
        if (self._parsed_args.l):
            self._check_arg_val(
                '-l', self._parsed_args.l, self._XML_ELEM_REGEX,
                err.ErrorCodes.XML_ELEM_ERR)
            self._processed_args['row_elem'] = self._parsed_args.l
        else:
            self._processed_args['row_elem'] = 'row'

    def _process_arg_i(self):
        if (self._parsed_args.i):
            if (self._parsed_args.l):
                self._processed_args['index_attr'] = 'index'
                self._processed_args['index_attr_cnt'] = 1
            else:
                err.Error.terminate(
                    '-i must be combined with -l\n\n',
                    err.ErrorCodes.ARGS_ERR)
        else:
            self._processed_args['index_attr'] = ''

    def _process_arg_start(self):
        if (self._parsed_args.start):
            if (self._parsed_args.i and self._parsed_args.l):
                self._processed_args['index_attr_cnt'] = (
                    self._parsed_args.start)
            else:
                err.Error.terminate(
                    '--start must be combined with -l and -i\n\n',
                    err.ErrorCodes.ARGS_ERR)
        else:
            self._processed_args['index_attr_cnt'] = 1

    def _process_arg_e(self):
        self._processed_args['error_recovery'] = (
            self._parsed_args.error_recovery)

    def _process_arg_missing_field(self):
        if (self._parsed_args.missing_field):
            if (self._parsed_args.error_recovery):
                self._processed_args['missing_field'] = (
                    self._parsed_args.missing_field)
            else:
                err.Error.terminate(
                    '--missing-field must be combined with -e\n\n',
                    err.ErrorCodes.ARGS_ERR)

    def _process_arg_all_columns(self):
        if (self._parsed_args.all_columns):
            if (self._parsed_args.error_recovery):
                self._processed_args['all_cols'] = True
            else:
                err.Error.terminate(
                    '--all-columns must be combined with -e\n\n',
                    err.ErrorCodes.ARGS_ERR)

    @property
    def processed_args(self):
        return self._processed_args