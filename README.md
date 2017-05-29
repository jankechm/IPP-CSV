# CSV to XML converter

Converts CSV file to XML file.

## Description

Each CSV line corresponds to defined pair element (see argument __-l__). The CSV columns will be nested in this element as subelements. The problematic chars like '&', '<', '>', ... are converted to '&amp', '&lt', '&gt', ...

## Syntax

```
csv.py  [--help] [--input filename] [--output filename] [-n]
        [-r root-element] [-s separator] [-h [subst]]
        [-c column-element] [-l line-element] [-i] [--start [n]] [-e]
        [--missing-field val] [--all-columns]
```

## Optional arguments

Argument | Description
------------ | -------------
__--help__ | show the help message
__--input *filename*__ | input file (default: stdin)
__--output *filename*__ | output file (default: stdout)
__-n__ | do not generate XML header
__-r *root-element*__ | name of the XML root element; if not defined, the output is not wrapped with root element
__-s *separator*__ | separator of the CSV cells (1 char)
__-c *column-element*__ | name of the element for CSV cells (default: "col"); each element is numbered from 1
__-l *line-element*__ | name of the element for CSV lines (default: "row")
__-i__ | add attribute "index" to line-element (must be combined with __-l__)
__--start *n*__ | set the counter of the __index__ attribute (must be combined with __-i__) to *n* (default: 1)
