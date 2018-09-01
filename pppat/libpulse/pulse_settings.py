import IRFMtb
import tarfile
from pppat.libpulse.DCS_settings import DCSSettings
import pkgutil
from importlib import import_module
import logging
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

        Return
        ------
        result: Boolean
            True if the pulse settings have been correctly loaded, else False

        """
        # Load DCS settings (Sup.xml)
        self.DCS_settings = DCSSettings(pulse_settings_files['sup'])
        return self.DCS_settings.isLoaded

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
                    res_load = self.load_from_file(pulse_settings_files)  
                    
                    return res_load
                    # TODO : clean up the file mess
#                    os.remove(XEDIT2DCS_archive)
#                    os.remove('DP.xml')
#                    os.remove('Sup.xml')
            else:
                logger.error('Problem to read the xml files!')
                return False
        else:
            logger.error('Problem with the database to get pulse setting files')
            return False
        #IRFMtb.tsrfile(pulse, 'FPCSPARAM', 'FPCSPARAM.tgz')


    def load_from_session_leader(self):
        """
        Return
        ------
        result: Boolean
            True if the pulse settings have been correctly loaded, else False

        """
        # TODO
        logger.error('Not implemented yet!')
        return False
    
    def check_all(self, is_online=True):
        """
        Check the pulse settings against various kinds of tests (WOI & other)
        
        Return
        ------
        check_results : list of ChecCheckResult objects  
        """
        check_results = []
        tested_fun_names = []
        
        # list of the Python file located in the tests pre-pulse directory
        check_filenames = [name for _, name, _ in pkgutil.iter_modules(['tests/pre_pulse'])]
        check_importers = [imp for imp, _, _ in pkgutil.iter_modules(['tests/pre_pulse'])]
        logger.debug(check_filenames)
        logger.debug(check_importers)
        
        # Run all tests functions located in the pre_pulse directory
        # These function names should start by 'check_'
        for (importer, file) in zip(check_importers, check_filenames):
            # all_fun = dir(importer.find_module(file).load_module())
            # check_fun = [n for n in all_fun if n.startswith('check_')]

            # import the module (here=file)
            i = import_module(importer.path.replace('/','.')+'.'+file)

            # list all the functions in the module file
            # and run the ones which name starts by 'check_'
            fun_names = dir(i)
            for fun_name in fun_names:
                if 'check_' in fun_name:
                    tested_fun_names.append(fun_name)
                    logger.info(f'{fun_name}: Testing...')
                    result = getattr(i, fun_name)(is_online=is_online)
                    check_results.append(result)
                    logger.info(f'{fun_name}: result={result.code_name}')

        return check_results
                    
if __name__ == '__main__':
    ps = PulseSettings()
    ps.load_from_file({'sup':'resources/pulse_setup_examples/52865/Sup.xml',
                       'dp':'resources/pulse_setup_examples/52865/DP.xml'})
                
