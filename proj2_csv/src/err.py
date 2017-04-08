import sys
import enum

class Error(object):
    """Class for terminating the script with corresponding return code,
    caused by non-valid input or operation"""
    class ErrorCodes(enum.IntEnum):
        BAD_ARGS = 1
        BAD_XML_ELEM = 30
        BAD_XML_ELEM_SUBSTITUTED = 31
    
    @staticmethod
    def terminate(message, returnCode):
        """Method terminates script with output message and return code"""
        sys.stderr.write(message)
        sys.exit(returnCode)


