import sys
import xml.etree.ElementTree as ET
import xml.dom.minidom as MD
import re

import src.err as err

class XML(object):
    """XML"""
    def __init__(self, ops, table, file=None):
        self._file_path = file
        self._ops = ops
        self._table = table

    def open(self):
        if (self._ops['output']):
            try:
                self._out = open(self._ops['output'], mode='w',
                    encoding='utf-8', newline='')
            except OSError as e:
                err.Error.terminate(
                    'Cannot open output file\n\n',
                    err.Error.ErrorCodes.OUTPUT_FILE_OPENING_ERR)
        else:
            self._out = sys.stdout
        #return self._out

    """def write(self):
        elems = []
        root = ET.Element("root")
        doc = ET.SubElement(root, "doc")
        #elems.append(doc)

        ET.SubElement(doc, "fie ld?1", name="bla>hč&").text = "čau some value1"
        ET.SubElement(doc, "field2", name="asdfasd").text = "some vlaue2"
        #elems.extend((fld1, fld2))
        #elems.append(fld1)
        #elems.append(fld2)
        
        tree = ET.ElementTree(root)
        tree.write("file.xml", encoding='unicode', xml_declaration=True)

        #xml = ET.tostring(root, encoding='utf-8')
        xml = ''
        #print(ET.tostring(root, encoding="unicode"))
        for elem in doc:
            xml += str(ET.tostring(elem, encoding="unicode"))
        print(xml)
        try:
            reparsed = MD.parseString(xml)
        except Exception as e:
            pass
        print('<?xml version="1.0" encoding="UTF-8"?>')
        pretty = reparsed.toprettyxml(indent="  ")
        ind1 = pretty.find('\n')
        pretty = pretty[ind1+1:]
        print(pretty)"""
        #print(root)

    def write(self):
        #print()
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
                col_elem = '{2}<{0}>{1}</{0}>\n'
                self._out.write(col_elem.format(col, col_val, indent_str * (indent + 1)))
                col_num += 1
            self._out.write('{1}</{0}>\n'.format(row_name, indent_str * indent))
            row_num += 1