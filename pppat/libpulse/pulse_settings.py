import IRFMtb
import tarfile
from pppat.libpulse.DCS_settings import DCSSettings
from pppat.libpulse.check_result import CheckResult
from pppat.libpulse.waveform import *
import pkgutil
from importlib import import_module
import logging
logger = logging.getLogger(__name__)
import os


class PulseSettings():
    XEDIT2DCS_FILES_PATH = '/var/tmp/pilotes/XEDIT2DCS/'
    XEDIT2DCS_FILENAMES = {'sup':'Sup.xml', 'dp':'DP.xml'}

    """
    Pulse setting

    PulseSetting is a model of the pulse settings which is created by the
    session leader. The pulse settings come from two XML files, namely
    DP.xml and SUP.xml. Each WEST pulse is defined following the information
    contained in these two files.
    """
    def __init__(self):
        logger.info('init Pulse Setting')

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
        # Load DCS settings (Sup.xml)
        self.DCS_settings = DCSSettings(pulse_settings_files['sup'])
        nominal_scenario = self.DCS_settings.nominal_scenario
        # Load DCS waveforms (DP.xml)
        self.waveforms = get_all_waveforms(nominal_scenario, pulse_settings_files['dp'])

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
                    tgz.extract(tgz.getmember(self.XEDIT2DCS_FILENAMES['dp']))
                    tgz.extract(tgz.getmember(self.XEDIT2DCS_FILENAMES['sup']))
                    # load pulse settings
                    res_load = self.load_from_file(self.XEDIT2DCS_FILENAMES)

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
        

#        self.LoadFolderName = '/Home/%s/XEDIT2DCS/data/output'%(self.parent.statusAreaWidget.login_name)
#
#        # DP.xml and Sup.xml are supposed to be in th same folder.
#        self.supFilename = '%s/Sup.xml'%(self.LoadFolderName)
#        self.dpFilename = '%s/DP.xml'%(self.LoadFolderName)
#    
        # if both files exist
        dp_file = os.path.join(self.XEDIT2DCS_FILES_PATH, self.XEDIT2DCS_FILENAMES['dp'])
        sup_file = os.path.join(self.XEDIT2DCS_FILES_PATH, self.XEDIT2DCS_FILENAMES['sup'])
        logger.info(f'Check availability of {dp_file} and {sup_file}')
        logger.info(os.path.exists(dp_file))
        logger.info(os.path.exists(sup_file))
        if os.path.exists(dp_file) and os.path.exists(sup_file):
            logger.info('Session leader DCS setting files found!')
            
            return True
        else:
            logger.error('Unable to read the DCS Settings from session leader')

            return False

#            # the sequence of segments (=segment trajectory) is retrieved from the Sup.xml file.
#            # At the moment, only the nominal scenario i.e. the scenario containing the most segments
#            # with numbers < 100 is retrieved.
#            self.segmentTrajectory = segmentTrajectoryFinder(self.supFilename)
#
#            # Update the scenario display with the nominal scenario
#            self.updateScenarioDisplay()
#
##            # Check if a watchdog already exists in order not to create a new one for each folder change               
##            if not hasattr(self, 'FolderWatcher'):
##                # No pre existing watchdog
##                self.FolderWatcher = ModifFolderWatcher(self.parent,self.LoadFolderName)
##                
##            else:
##                # preexisting watchdog: stop and recreate a new one.
##                self.FolderWatcher.resetModifFolderWatcher(self.LoadFolderName)
#
#            # Resets text area and colored squares
#            self.parent.CheckAreaWidget.resetChecks()
#
#            # Update the next shot number
#            self.parent.OnlineSituationAreaWidget.updateNextShot()
#
#            # Update the last modification time
#            self.parent.OnlineSituationAreaWidget.updateModTime()
#
#        # Case if the user cancels the load operation or if the file has not been found
##            # Displays a text message saying the load operation has not been completed.
##            self.parent.CheckAreaWidget.WrongDCSFile()
##            # Updates the next shot number
##            self.parent.OnlineSituationAreaWidget.updateNextShot()
##            # Erases the scenario display
##            self.parent.scenarioAreaWidget.resetScenarioDisplay()
##            # Unloads the DCS file
##            self.unloadDCS()
##            # Removes the changetime for current file.
##            self.parent.OnlineSituationAreaWidget.removeModTime()


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

#class ModifFolderWatcher(QtCore.QThread):
#    """
#    Watcher class to monitor file changes on DP.xml or Sup.xml
#    Methods:
#    - modified: actions to perform when a folder/file change is detected
#    - resetFolderWatcher: actions to perform when the user changes the folder to be monitored
#    """
#    def __init__(self,parentWidget,folderName):
#        """
#        Overloaded init to be able to pass the parent widget (for addressing purposes)
#        and the folder to be monitored.
#        """
#        super(ModifFolderWatcher, self).__init__()
#        self.folderName = folderName
#        self.parent = parentWidget
#        # Start the observer process (standard way to do it for the watchdog package)
#        self.observer = Observer()
#        self.event_handler = MyHandler(self.folderName)
#        self.observer.schedule(self.event_handler, self.folderName, recursive=True)
#        self.observer.start()
#        # Method called when a change is detected
#        self.connect(self.event_handler, QtCore.Signal("FolderModified"), self.modified) #PyQt4
#
#
#    def modified(self):
#        """
#        Performs actions when a file change is detected.
#        - Stops the watcher to avoid signal saturation.
#        - Resets the results of checks in the checkArea (returns colored squares to black)
#        - Resets the scenario display area
#        - Update the next shot number
#        - Unload the DCS files to prevent any subsequent check or BigPicture by the user
#        - Remove the changetime from the onlineSituation Area (because the DCS file has to be reloaded
#        """
#        #self.emit(QtCore.SIGNAL("fileModified1"))
#        self.observer.stop()
#        self.parent.CheckAreaWidget.resetScenario()
#        self.parent.scenarioAreaWidget.resetScenarioDisplay()
#        self.parent.OnlineSituationAreaWidget.updateNextShot()
#        self.parent.scenarioAreaWidget.unloadDCS()
#        self.parent.OnlineSituationAreaWidget.removeModTime()
#
#    def resetModifFolderWatcher(self,folderName):
#        """
#        Stops the pre-existing watcher and starts a new one with a new folder to be monitored
#        Similar procedure as in the init.
#        """
#        self.observer.stop()
#        self.folderName = folderName
#        self.observer = Observer()
#        self.event_handler = MyHandler(self.folderName)
#        self.observer.schedule(self.event_handler, self.folderName, recursive=True)
#        self.observer.start()
#        self.connect(self.event_handler, QtCore.Signal("FolderModified"), self.modified)



if __name__ == '__main__':
    ps = PulseSettings()
#    ps.load_from_file({'sup':'resources/pulse_setup_examples/52865/Sup.xml',
#                       'dp':'resources/pulse_setup_examples/52865/DP.xml'})
    ps.load_from_session_leader()
    

