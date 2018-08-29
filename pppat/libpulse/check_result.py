class CheckResult():
    # define code as constant
    OK = 3
    UNAVAILABLE = 2
    WARNING = 1
    ERROR = 0
    DIC = {0: 'ERROR', 1: 'WARNING', 2: 'UNAVAILABLE', 3: 'OK'}

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
        return f'Result of test "{self.name}": code={self.code} [{self.DIC[self.code]}]:{self.text}'