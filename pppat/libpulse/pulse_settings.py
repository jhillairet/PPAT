import IRFMtb
import tarfile
import pkgutil
import os
import platform
from pppat.libpulse.DCS_settings import DCSSettings
from pppat.libpulse.check_result import CheckResult
from pppat.libpulse.waveform import get_all_waveforms, get_all_waveforms_dict, get_waveform
from pppat.libpulse.utils import HiddenPrints
from importlib import import_module
import numpy as np

import logging
logger = logging.getLogger(__name__)


class PulseSettings():
    XEDIT2DCS_DIR_PATH = '/var/tmp/pilotes/XEDIT2DCS/'
    XEDIT2DCS_FILENAMES = {'sup':'Sup.xml', 'dp':'DP.xml'}
    XEDIT2DCS_SERVER = 'nunki.intra.cea.fr'
    XEDIT2DCS_PUBLIC_PATH = '/Home/cgc/WEST_PCS'  # path where the last DCS files are copied to
    
    """
    WEST Pulse Settings

    PulseSettings is a model of the WEST pulse settings which is created by the
    Session Leader using the XEdit2DCS tool. XEdit2DCS creates two XML files, 
    namely DP.xml and SUP.xml. Each WEST pulse is defined following the 
    information contained in these two files.
    """
    def __init__(self, pulse_nb: int=None):
        """
        WEST Pulse Settings 

        Parameters
        ----------
        pulse_nb : int, optional
            WEST pulse number. Default is None.

        """
        logger.info('Init Pulse Setting')
        
        self.pulse_nb = pulse_nb  # pulse number
        self.files = None  # dictionnary containing 'dp' and 'sup' xml file paths
        self.waveforms = None  # list of nominal Waveform objects
        self.waveforms_dict = None  # dict of nominal waveforms indexed by waveform names
        
        # directly load the pulse settings if the pulse number is provided       
        if pulse_nb is not None:
            if pulse_nb == 0:
                res = self.load_next_pulse_settings()
            elif pulse_nb > 50000:
                res = self.load_from_pulse(pulse_nb)

    def load_from_file(self, pulse_settings_files: dict) -> bool:
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

        # Load nominal DCS waveforms (DP.xml)
        self.waveforms = get_all_waveforms(self.nominal_scenario, self.files['dp'])
        self.waveforms_dict = get_all_waveforms_dict(self.nominal_scenario, self.files['dp'])

        # TODO : recuperer le numero de choc à partir des fichiers de settings?
        self.pulse_nb = None

        return self.DCS_settings.isLoaded

    @property
    def nominal_scenario(self) -> list:
        """
        Nominal trajectory with segments' associated start times and durations 

        Returns
        -------
        nominal_scenario: list of tuples
            Nominal scenario, ie segment names and time properties
            [(segment_name, t_start, duration), ...]

        """
        return self.DCS_settings.nominal_scenario

    @property
    def nominal_trajectory(self) -> list:
        """
        Nominal Trajectory of the waveforms of the DCS pulse Setting

        Returns
        -------
        nominal_trajectory: list of str
            Nominal Trajectory of the waveforms of the DCS pulse Setting. 
            List of string containing the name of each segments.

        """
        return self.DCS_settings.nominal_trajectory

    def load_from_pulse(self, pulse: int) -> bool:
        """
        Load the DCS pulse settings from a given WEST pulse number

        Parameters
        ----------
        pulse: int
            WEST pulse number (pulse>50000)

        Return
        ------
        result: bool
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

    def load_next_pulse_settings(self) -> bool:
        """
        Load DCS Settings for the next pulse prepared by the SL.
        
        The settings files have been generated by XEdit2DCS and are stored in
        IRFM server. If the user is the EiC, then the files are directly read from the DCS server. 
        Otherwise, the files are read from a public directory where they have been copied to.

        Returns
        -------
        result: bool
            True if the pulse settings have been correctly loaded, else False
    
        """
        computer_name = platform.node()
        if computer_name == self.XEDIT2DCS_SERVER:
            # user is under the DCS server, we assume he's the EiC
            logger.info(f'User is connected on {self.XEDIT2DCS_SERVER}. EiC assumed.')
            dp_file = os.path.join(self.XEDIT2DCS_DIR_PATH, self.XEDIT2DCS_FILENAMES['dp'])
            sup_file = os.path.join(self.XEDIT2DCS_DIR_PATH, self.XEDIT2DCS_FILENAMES['sup'])
        else:
            logger.info(f'User is not connected on {self.XEDIT2DCS_SERVER}...')
            logger.info(f'...Read public DCS Settings from {self.XEDIT2DCS_PUBLIC_PATH}')            
            dp_file = os.path.join(self.XEDIT2DCS_PUBLIC_PATH, self.XEDIT2DCS_FILENAMES['dp'])
            sup_file = os.path.join(self.XEDIT2DCS_PUBLIC_PATH, self.XEDIT2DCS_FILENAMES['sup'])
   
        self.files = {'sup': sup_file, 'dp': dp_file}

        if os.path.exists(dp_file) and os.path.exists(sup_file):
            logger.info('Session leader DCS setting files found!')	
            # load pulse settings
            res_load = self.load_from_file(self.files)
            self.pulse_nb = self.next_pulse()

            return res_load
        else:
            logger.error('Unable to read the DCS Settings')

            return False
            

    def next_pulse(self) -> int:
        """
        Return the next pulse number (pulse under preparation)

        Returns
        -------
        next_pulse: int
            Next pulse number (the future pulse, which is under preparation)

        """
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

    @property
    def fuelling_valves(self):
        """
        Returns the list of fueling valves numbers used in a pulse
        """
        # get the gaz valve distribution matrix (for all valves)
        G_dist = [get_waveform(f'rts:WEST_PCS/Actuators/Gas/REF1/G_dist_{i}.ref', self.waveforms).nominal for i in range(1, 22)]
        # test if any of the valve has non null values during nominal segments
        valve_nbs = []
        for (idx, G) in enumerate(G_dist):
            if np.any(G_dist[idx].values > 0):
                valve_nbs.append(idx + 1)        
        return valve_nbs

    @property
    def waveform_names(self) -> list:
        """
        Return a list of the waveform names

        Returns
        -------
        wf_names: list of str
            List of waveform names 

        """
        wf_names = [wf.name for wf in self.waveforms]
        return wf_names

    
    @property
    def waveforms_values(self, wf_names=None) -> dict:
        """
        Times and values for all the waveforms for the nominal trajectory. 
        
        Parameter
        ---------
        wf_names: list of str [optionnal]
            list of the waveform name to select. Default is None, which means
            all the waveforms data will be returned

        Returns
        -------
        wf_values: dict of dict
            times and values for all the waveforms for the nominal trajectory
            

        """
        if not wf_names:
            wf_names = self.waveform_names
        wf_values = dict()
        for wf_name in wf_names:
            wf_values[wf_name] = {'times': self.waveforms[wf_name].times, 
                                  'values': self.waveforms[wf_name].values}
        return wf_values

      

def export_for_tools_dc(pulse: int):
    """
    Print all waveforms times and values for the nominal trajectory. 

    Parameters
    ----------
    pulse : int
        WEST pulse number

    """   
    with HiddenPrints():    
        ps = PulseSettings(pulse)
    
    for wf in ps.waveforms:
        # the nickname is the concatenation of the waveform name (except 1st element)
        # with '/' replaced by a '.' for matlab structure compatibility
        wf_nickname = wf.name.replace('/', '.').replace('rts:', '').replace('.ref','')
        print(f'wf.{wf_nickname}.time = {wf.times}')
        print(f'wf.{wf_nickname}.value = {wf.values}')
           

if __name__ == '__main__':
#    ps = PulseSettings()
##    ps.load_from_file({'sup':'resources/pulse_setup_examples/52865/Sup.xml',
##                       'dp':'resources/pulse_setup_examples/52865/DP.xml'})
#    54535 # V9
#    54534 # V1 + V11
#    54533 # V2
#    54532 # V11
#    
#    ctr_enable = get_waveform('rts:WEST_PCS/Actuators/Gas/REF1/ctr_enable.ref', ps.waveforms)
#    ref_type = get_waveform('rts:WEST_PCS/Actuators/Gas/ref_type.ref', ps.waveforms)
#    measure_choice = get_waveform('rts:WEST_PCS/Actuators/Gas/REF1/measure_choice.ref', ps.waveforms)
    pulse = 0
    ps = PulseSettings(pulse)
    print(ps)
    export_for_tools_dc(pulse)
