import IRFMtb
import tarfile
import pkgutil
import os
import platform
from pppat.libpulse.DCS_settings import DCSSettings
from pppat.libpulse.check_result import CheckResult
from pppat.libpulse.waveform import get_all_waveforms
from importlib import import_module

import logging
logger = logging.getLogger(__name__)


class PulseSettings():
    XEDIT2DCS_DIR_PATH = '/var/tmp/pilotes/XEDIT2DCS/'
    XEDIT2DCS_FILENAMES = {'sup':'Sup.xml', 'dp':'DP.xml'}
    XEDIT2DCS_SERVER = 'nunki.intra.cea.fr'
    
    """
    Pulse setting

    PulseSetting is a model of the pulse settings which is created by the
    session leader. The pulse settings come from two XML files, namely
    DP.xml and SUP.xml. Each WEST pulse is defined following the information
    contained in these two files.
    """
    def __init__(self):
        logger.info('init Pulse Setting')
        
        self.pulse_nb = None  # pulse number
        self.files = None  # dictionnary containing 'dp' and 'sup' xml file paths
        self.waveforms = None  # list of Waveform objects

    def load_from_file(self, pulse_settings_files):
        """
        Load the pulse settings from the Sup.xml and DP.xml files.

        Parameters
        ----------
        pulse_settings_files : dict
            dictionnary which contains the path to the XML files. We expect
            pulse_settings_files['sup'] and pulse_settings_files['dp'] to
            contain the path to these Sup.xml and DP.xml respectively

        Return
        ------
        result: Boolean
            True if the pulse settings have been correctly loaded, else False

        """
        self.files = pulse_settings_files
        
        # Load DCS settings (Sup.xml)
        self.DCS_settings = DCSSettings(self.files['sup'])

        # Load DCS waveforms (DP.xml)
        self.waveforms = get_all_waveforms(self.nominal_scenario, self.files['dp'])

        # TODO : recuperer le numero de choc à partir des fichiers de settings?
        self.pulse_nb = None

        return self.DCS_settings.isLoaded

    @property
    def nominal_scenario(self):
        return self.DCS_settings.nominal_scenario

    @property
    def nominal_trajectory(self):
        return self.DCS_settings.nominal_trajectory

    def load_from_pulse(self, pulse):
        """
        Load the pulse settings from a WEST shot number

        Parameters
        ----------
        pulse: int
            WEST pulse number (pulse>50000)

        Return
        ------
        result: Boolean
            True if the pulse settings have been correctly loaded, else False

        """
        # TODO: ? IRFMtb.tsrfile(pulse, 'FPCSPARAM', 'FPCSPARAM.tgz')
        XEDIT2DCS_archive = 'FXEDIT2DCS.tgz'
        self.pulse_nb = None
        # extract DP.xml and Sup.xml from the tar.gz obtained from the
        # database (if they exist in the database) and load them
        result = IRFMtb.tsrfile(pulse, 'FXEDIT2DCS', XEDIT2DCS_archive)
        if result == 0:
            if tarfile.is_tarfile(XEDIT2DCS_archive):
                with tarfile.open(XEDIT2DCS_archive, mode='r') as tgz:
                    tgz.extract(tgz.getmember(self.XEDIT2DCS_FILENAMES['dp']))
                    tgz.extract(tgz.getmember(self.XEDIT2DCS_FILENAMES['sup']))
                    # load pulse settings
                    # TODO : download/move the file is correct temp directory
                    res_load = self.load_from_file(self.XEDIT2DCS_FILENAMES)
                    # update the pulse number
                    self.pulse_nb = pulse
                    
                    return res_load
#                # TODO: should we clean the xml files when reading from a file?
#                # only if local file! Should not delete files on Nunki !!
#                # clean up the file mess
#                try:
#                    os.remove(XEDIT2DCS_archive)
#                    os.remove('DP.xml')
#                    os.remove('Sup.xml')
#                except Exception as e:
#                    logger.error(f'Problem when deleting the xml files during cleaning: {str(e)}')
              
            else:
                logger.error('Problem to read the xml files!')
                return False
        else:
            logger.error('Problem with the database to get pulse setting files')
            return False

    def load_from_session_leader(self):
        """
        Return
        ------
        result: Boolean
            True if the pulse settings have been correctly loaded, else False

        """
        self.pulse_nb = None
        # Check the DCS settings are available are read them if they are
        computer_name = platform.node()
        if not computer_name == self.XEDIT2DCS_SERVER:
            logger.error('Session leader DCS settings are only available on Nunki!')
            return False
        else:
            # TODO : make a watchdog on the files
            dp_file = os.path.join(self.XEDIT2DCS_DIR_PATH, self.XEDIT2DCS_FILENAMES['dp'])
            sup_file = os.path.join(self.XEDIT2DCS_DIR_PATH, self.XEDIT2DCS_FILENAMES['sup'])
            self.files = {'sup': sup_file, 'dp': dp_file}

            if os.path.exists(dp_file) and os.path.exists(sup_file):
                logger.info('Session leader DCS setting files found!')	
                # load pulse settings
                res_load = self.load_from_file(self.files)
                self.pulse_nb = self.next_pulse()
    
                return res_load
            else:
                logger.error('Unable to read the DCS Settings from session leader')
    
                return False

    def next_pulse(self):
        ' determine the next pulse number '
        return IRFMtb.tsdernier_choc() + 1
        

    def check_all(self, is_online=True):
        """
        Check the pulse settings against various kinds of tests (WOI & other)

        Parameters
        ----------
        is_online: Boolean
            True if the IRFM database is reachable on the network, False if not

        Return
        ------
        check_results : List
            List of CheckResult objects

        """
        check_results = []
        tested_fun_names = []

        # list of the Python file located in the tests pre-pulse directory
        check_filenames = [name for _, name, _ in pkgutil.iter_modules(['tests/pre_pulse'])]
        check_importers = [imp for imp, _, _ in pkgutil.iter_modules(['tests/pre_pulse'])]
        logger.debug(check_filenames)
        logger.debug(check_importers)

        # Run all tests functions located in the pre_pulse directory
        # These function names should start by 'check_' and returns a CheckResult
        # TODO: run these tests in parallel
        logger.info("########## C'est parti mon kiki ! ###########")
        for (importer, file) in zip(check_importers, check_filenames):
            # import the module (here=file)
            i = import_module(importer.path.replace('/', '.') + '.' + file)

            # list all the functions in the module file
            # and run the ones which name starts by 'check_'
            fun_names = dir(i)
            # parameters given to all check functions
            kwargs = {'is_online': is_online, 'waveforms': self.waveforms}
            for fun_name in fun_names:
                if 'check_' in fun_name:
                    tested_fun_names.append(fun_name)
                    logger.debug(f'{fun_name}: Testing...')
                    # Run the function. 
                    # In case of Python error (error in code?)
                    # catch the error and trace it as a failed test
                    # and continue without breaking everything
                    try:
                        # evaluate a check function and retrieve its result
                        result = getattr(i, fun_name)(**kwargs)
                    except Exception as e:  # catch *all* exceptions
                        result = CheckResult(name=fun_name,
                                             code=CheckResult.BROKEN, 
                                             text=str(e))
                        logger.error(f'Error {e} during in {fun_name}')

                    check_results.append(result)
                    logger.info(f'{fun_name}: result={result.code_name}')

        return check_results


if __name__ == '__main__':
    ps = PulseSettings()
#    ps.load_from_file({'sup':'resources/pulse_setup_examples/52865/Sup.xml',
#                       'dp':'resources/pulse_setup_examples/52865/DP.xml'})
    ps.load_from_session_leader()
    

