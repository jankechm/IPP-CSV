import sys
import xml.etree.ElementTree as ET
import xml.dom.minidom as MD
import re

import src.err as err

class XML(object):
    """XML output"""
    def __init__(self, ops):
        self._ops = ops

    def open(self):
        if (self._ops['output']):
            try:
                self._out = open(self._ops['output'], mode='w',
                    encoding='utf-8', newline='')
            except OSError as e:
                err.Error.terminate(
                    'Cannot open output file\n\n',
                    err.ErrorCodes.OUTPUT_FILE_OPENING_ERR)
        else:
            self._out = sys.stdout
    
    def _replace_by_entity_ref(self, content):
        entity_refs = {
            '&':'&amp;', '<':'&lt;', '>':'&gt;', "'":'&apos;', '"':'&quot;'}
        for key, val in entity_refs.items():
            content = content.replace(key, val)
        return content
    
    def write_data(self, table):
        self._table = table

        if (self._ops['header']):
            self._out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        if (self._ops['root_elem']):
            self._out.write('<{0}>\n'.format(self._ops['root_elem']))
            self._write_contents()
            self._out.write('</{0}>\n'.format(self._ops['root_elem']))
        else:
            self._write_contents(indent=0)

    def _write_contents(self, indent=1):
        indent_str = '    '
        row_name = self._ops['row_elem']
        row_num = self._ops['index_attr_cnt']

        for row, row_val in self._table.items():
            if (self._ops['index_attr']):
                self._out.write(
                    '{1}<{0} index="{2}">\n'.format(
                        row_name, indent_str * indent, row_num))
            else:
                self._out.write(
                    '{1}<{0}>\n'.format(row_name, indent_str * indent))
            col_num = 1
            for col, col_val in row_val.items():
                #replace problematic chars by entity references
                col_val = self._replace_by_entity_ref(col_val)

                col_elem = '{2}<{0}>{1}</{0}>\n'
                self._out.write(col_elem.format(col, col_val,
                    indent_str * (indent + 1)))
                col_num += 1
            self._out.write('{1}</{0}>\n'.format(row_name, 
                indent_str * indent))
            row_num += 1