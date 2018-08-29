import IRFMtb
import tarfile
import logging
import os
from pppat.libpulse.DCS_settings import DCSSettings

logger = logging.getLogger(__name__)


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

    def load_from_file(self, pulse_settings_files):
        """
        Load the pulse settings from the Sup.xml and DP.xml files. 
        
        Parameters
        ----------
        pulse_settings_files : dict
            dictionnary which contains the path to the xml files. We expect
            pulse_settings_files['sup'] and pulse_settings_files['dp'] to 
            contain the path to these Sup.xml and DP.xml respectively
        """
        # Load DCS settings (Sup.xml)
        self.DCS_settings = DCSSettings(pulse_settings_files['sup'])   

    def load_from_pulse(self, pulse):
        """
        Load the pulse settings from a WEST shot number
        
        Parameters
        ----------
        pulse: int
            WEST pulse number (pulse>50000)
        
        """
        XEDIT2DCS_archive = 'FXEDIT2DCS.tgz'
        # extract DP.xml and Sup.xml from the tar.gz obtained from the 
        # database (if they exist in the database) and load them
        result = IRFMtb.tsrfile(pulse, 'FXEDIT2DCS', XEDIT2DCS_archive)
        if result == 0:
            if tarfile.is_tarfile(XEDIT2DCS_archive):
                with tarfile.open(XEDIT2DCS_archive, mode='r') as tgz:
                    tgz.extract(tgz.getmember('DP.xml'))
                    tgz.extract(tgz.getmember('Sup.xml'))
                    pulse_settings_files = {'sup':'Sup.xml', 
                                            'dp':'DP.xml'}
                    # load pulse settings
                    self.load_from_file(pulse_settings_files)  
                    
#                    # clean up the file mess
#                    os.remove(XEDIT2DCS_archive)
#                    os.remove('DP.xml')
#                    os.remove('Sup.xml')
                    
        #IRFMtb.tsrfile(pulse, 'FPCSPARAM', 'FPCSPARAM.tgz')
                      




    def load_from_session_leader(self):
        pass
    
    def validate(self):
        """
        Validate the pulse settings against various kinds of tests (WOI & other)
        """
        pass
    
                    
                
                
