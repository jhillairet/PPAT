class CheckResult():
    # define code as constant
    OK = 3
    UNAVAILABLE = 2
    WARNING = 1
    ERROR = 0
    BROKEN = -1
    DIC = {0: 'ERROR', 1: 'WARNING', 2: 'UNAVAILABLE', 3: 'OK', -1: 'BROKEN'}

    def __init__(self, name='', code=0, text='',
                 fail_abs_times=[], fail_values=[], fail_rel_times=[],
                 fail_segments=[], fail_values_unit='', fail_limit=0):
        """
        Test/Validation result object.

        Parameters
        ----------
        name : str
            Name of the check (for WOIs containing more than one check)
        code : int
            0 = error; 1 = warning; 2 = data unavailable (on/offline); 3 = OK
        text : str
            Free explanation text
        fail_abs_times : list or Numpy array
            Absolute times in the scenario at which the check is failed
        fail_values : float, list of Numpy array
            Value at which the check is failed
        fail_rel_times : list or Numpy array
            Relative times in the segment at which the check is failed
        fail_values_unit : str
            Physical unit of the parameter
        fail_segments : int or list of int
            Segments corresponding to the check failures
        fail_limit : int
            Limit tested
        """
        self.name = name
        self.code = code
        self.text = text

        self.fail_values = fail_values
        self.fail_values_unit = fail_values_unit
        self.fail_abs_times = fail_abs_times
        self.fail_rel_times = fail_rel_times
        self.fail_segments = fail_segments
        self.fail_limit = fail_limit

    def __repr__(self):
        return f'Checking: [{self.DIC[self.code]}] for "{self.name}": {self.text}'
    
    @property
    def code_name(self):
        """ convenient representation of the result code as a string """
        return self.DIC[self.code]

from qtpy.QtWidgets import QTableWidgetItem
from qtpy.QtCore import Qt

class CheckResultQTableWidgetItem(QTableWidgetItem):
    """
    QTableWidgetItem representation of a check result
    
    Used to define the UI properties of a result (color, background) as well
    as sorting order (ERROR < WARNING < UNAVAILABLE < OK < BROKEN)
    """
    def __init__(self, result):
        """
        Parameter:
        ----------
         - result: CheckResult
        """
        self.result = result
        super(CheckResultQTableWidgetItem, self).__init__(self.result.code_name)

    def __lt__ (self, other):
        """
        Override method bool QTableWidgetItem.__lt__(self, QTableWidgetItem other) 
        to compare our own case
        """
        if (isinstance(other, CheckResultQTableWidgetItem)):
            selfDataValue  = self.result.code
            otherDataValue = other.result.code
            return selfDataValue < otherDataValue
        else:
            return QTableWidgetItem.__lt__(self, other)