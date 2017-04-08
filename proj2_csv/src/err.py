import sys
import enum

class Error(object):
    """Class for terminating the script with corresponding return code,
    caused by non-valid input or operation"""
    class ErrorCodes(enum.IntEnum):
        ARGS_ERR = 1
        INPUT_FILE_OPENING_ERR = 2
        OUTPUT_FILE_OPENING_ERR = 3
        XML_ELEM_ERR = 30
        XML_ELEM_SUBSTITUTED_ERR = 31
    
    @staticmethod
    def terminate(message, returnCode):
        """Method terminates script with output message and return code"""
        sys.stderr.write(message)
        sys.exit(returnCode)


