class PulseSettings():
    """
    Pulse setting

    PulseSetting is a model of the pulse setting which is created by the
    session leader. The pulse settings come from two XML files, namely
    DP.xml and SUP.xml. Each WEST pulse is defined following the information
    contained in these two file.
    """
    def __init__(self):
        logger.info('init Pulse Setting')


    def open_from_file(self, dp_path, sup_path):
        pass

    def open_from_shot(self, shot):
        pass

    def open_from_session_leader(self):
        pass