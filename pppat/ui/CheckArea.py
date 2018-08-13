from . Qt import QtWidgets, QtCore, QtGui
import xml.etree.ElementTree as ET
import numpy as np
from . import waveform_pack
from .check_functions import *

# Class defining the central area of the GUI: colored squares, output text area
# and check button. Launches the tests.

class CheckArea():
    def __init__(self,parentWidget):

        # The parent widget is passed as an argument at initialization to be able to
        # call other methods from other elements of the GUI.

        self.parent = parentWidget

        # Read the xml configuration file (SL or EiC for instance)
        # This is used later to determine which tests to do.

        xml_doc = ET.parse(str(self.parent.config_file_name))
        xml_root = xml_doc.getroot()

        # Text label initialization ("checks label")
        self.label_Checks = QtWidgets.QLabel(parentWidget)
        self.label_Checks.setGeometry(QtCore.QRect(10, 100, 101, 31))
        font = QtGui.QFont()
        font.setPixelSize(20)
        self.label_Checks.setFont(font)
        self.label_Checks.setObjectName("label_Checks")
        self.label_Checks.setText("Checks")


        # Text area initialization (results and various messages from the software)
        self.textBrowser_results = QtWidgets.QTextBrowser(parentWidget)
        self.textBrowser_results.setGeometry(QtCore.QRect(10, 300, 750, 331))
        font = QtGui.QFont()
        font.setPixelSize(13)
        self.textBrowser_results.setFont(font)
        self.textBrowser_results.setObjectName("textBrowser_results")
        self.textBrowser_results.setText("Checks not run yet. \n")

        # Initizalization of the grid layout widget containing the colored squares
        # and their line title. Presently contains 6 cells:
        # 3 lines (one for WOIs, one for Protections, one for Machine conditions)
        # In the future, could be left completely config-file-driven.

        self.gridLayoutWidget_2 = QtWidgets.QWidget(parentWidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 150, 691, 112))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setObjectName("gridLayout_2")

        # WOI Line in GridLayout_2

        self.label_WOI = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPixelSize(16)
        self.label_WOI.setFont(font)
        self.label_WOI.setObjectName("label_WOI")
        self.label_WOI.setText("Operating Instructions  ")
        self.gridLayout_2.addWidget(self.label_WOI, 1, 0)

        # Horizontal Layout inserted in the second column of the line.
        # Contains all the colored squares for each WOI checked.
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Initialization of a array of instances of toolButton_individual_checks
        # The class is defined at the bottom of this file.

        self.toolB_WOI_list = np.array([],dtype='object')

        # Look for all the WOI to be checked in the config file, and create a
        # toolButton_individual_check object for each of them
        for WOI_check_element in xml_root.find('WOI_LIST').findall('WOI'):

            # Append the array with the new toolButton_individual_check to be created
            self.toolB_WOI_list = np.append(self.toolB_WOI_list,toolButton_individual_check(self.horizontalLayout,self.textBrowser_results))
            # Fill its attributes taken from the config file (name, address of the check script)
            self.toolB_WOI_list[-1].check_name = str(WOI_check_element.find('NAME').text)
            self.toolB_WOI_list[-1].script_address = WOI_check_element.find('SCRIPT_ADDRESS').text
            # Action linked to the click on the colored square (i.e. display the text related to the test)
            self.toolB_WOI_list[-1].toolButton_object.clicked.connect(self.toolB_WOI_list[-1].click_detailed_output)

        # Once the horizontal layout containing all the squares, add it to the global gridLayout
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 1 ,QtCore.Qt.AlignLeft)


        # Same as block above for second line of the checks (check Protections).
        self.label_Protections = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPixelSize(16)
        self.label_Protections.setFont(font)
        self.label_Protections.setObjectName("label_Protections")
        self.label_Protections.setText("Protections  ")
        self.gridLayout_2.addWidget(self.label_Protections, 2, 0)

        self.horizontalLayout2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout2.setObjectName("horizontalLayout2")


        self.toolB_Protection_list = np.array([],dtype='object')

        #for Protection_check_element in xml_root.getElementsByTagName('PROTECTION'):
        for Protection_check_element in xml_root.find('PROTECTION_LIST').findall('PROTECTION'):
            self.toolB_Protection_list = np.append(self.toolB_Protection_list,toolButton_individual_check(self.horizontalLayout2,self.textBrowser_results))
            self.toolB_Protection_list[-1].check_name = Protection_check_element.find('NAME').text
            #self.toolB_Protection_list[-1].attached_output_text = '%s\n -------------------------------- \n' %(Protection_check_element.find('NAME').text)
            self.toolB_Protection_list[-1].script_address = Protection_check_element.find('SCRIPT_ADDRESS').text
            self.toolB_Protection_list[-1].toolButton_object.clicked.connect(self.toolB_Protection_list[-1].click_detailed_output)

        self.gridLayout_2.addLayout(self.horizontalLayout2, 2, 1, QtCore.Qt.AlignLeft)


        # Same as above for the third line (check Machine Configuration)

        self.label_MachineConfig = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPixelSize(16)
        self.label_MachineConfig.setFont(font)
        self.label_MachineConfig.setObjectName("label_MachineConfig")
        self.label_MachineConfig.setText("Machine Configuration  ")
        self.gridLayout_2.addWidget(self.label_MachineConfig, 3, 0)

        self.horizontalLayout3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout3.setObjectName("horizontalLayout3")

        self.toolB_MachineConfig_list = np.array([],dtype='object')


        for MachineConfig_check_element in xml_root.find('MACHINE_CONFIG_LIST').findall('MACHINE_CONFIG'):
            self.toolB_MachineConfig_list = np.append(self.toolB_MachineConfig_list,toolButton_individual_check(self.horizontalLayout3,self.textBrowser_results))
            self.toolB_MachineConfig_list[-1].check_name = MachineConfig_check_element.find('NAME').text
            #self.toolB_MachineConfig_list[-1].attached_output_text = '%s\n -------------------------------- \n' %(MachineConfig_check_element.find('NAME').text)
            self.toolB_MachineConfig_list[-1].script_address = MachineConfig_check_element.find('SCRIPT_ADDRESS').text
            self.toolB_MachineConfig_list[-1].toolButton_object.clicked.connect(self.toolB_MachineConfig_list[-1].click_detailed_output)

        self.gridLayout_2.addLayout(self.horizontalLayout3, 3, 1, QtCore.Qt.AlignLeft)


        # Title of the text area.

        self.label_CheckResults = QtWidgets.QLabel(parentWidget)
        self.label_CheckResults.setGeometry(QtCore.QRect(10, 270, 373, 31))
        font = QtGui.QFont()
        font.setPixelSize(16)
        self.label_CheckResults.setFont(font)
        self.label_CheckResults.setObjectName("label_CheckResults")
        self.label_CheckResults.setText("Check results")

        # "Check Now" Button
        self.pushButton_CheckNow = QtWidgets.QPushButton(parentWidget)
        self.pushButton_CheckNow.setGeometry(QtCore.QRect(130, 100, 100, 35))
        font = QtGui.QFont()
        font.setPixelSize(14)
        self.pushButton_CheckNow.setFont(font)
        self.pushButton_CheckNow.setObjectName("pushButton_CheckNow")
        self.pushButton_CheckNow.setText("Check Now")
        self.pushButton_CheckNow.clicked.connect(self.perform_checks)

    # Method related to the click action on the "Check Now" button
    def perform_checks(self):

        if self.parent.scenarioAreaWidget.isScenarioLoaded:

            # Validation_summary is the global summary of the checks. As soon as at least one is invalid,
            # a message indicating it is displayed in the text area. Otherwise an "OK" is displayed.
            validation_summary_bool = True

            # The online status (i.e. if the user is online or offline in the control room) changes
            # the way checks are done. It is to be sent to the check scripts.
            online_status = self.parent.statusAreaWidget.login_status

            # Iterator to select which colored square is to be updated.
            k=0

            # Iterate on the list of WOIs to be checked (and therefore on each toolButton_individual_check
            for toolB_WOI in self.toolB_WOI_list:

                # Run the check script for a given toolButton_individual_check.
                check_result_array = globals()[toolB_WOI.script_address](self.parent.scenarioAreaWidget.segmentTrajectory,self.parent.scenarioAreaWidget.dpFilename,online_status)

                # Output text: name of the WOI checked.
                self.toolB_WOI_list[k].attached_output_text = '%s\n-------------------------------- \n' %(toolB_WOI.check_name)

                # A given WOI may contain several checks. All the codes for the result of each individual check in a WOI are stored
                # in the result_code array. The color of the colored square is determined taking the "worst" result of all checks.
                # See definition the definition of codes in the class check_result.py.
                # The global validation summary is cheged to False as soon as one check fails.
                # The number of checks for a given WOI is known by the size of the check result array coming from the check routine.

                result_code = []

                for ii in range(0,check_result_array.size):
                    result_code.append(check_result_array[ii].check_result_code)
                    global_result_code = min(result_code)

                if (global_result_code==0):
                    self.toolB_WOI_list[k].toolButton_object.setStyleSheet("background-color:\"red\"")
                    validation_summary_bool = False
                elif (global_result_code==1):
                    self.toolB_WOI_list[k].toolButton_object.setStyleSheet("background-color:\"yellow\"")
                    validation_summary_bool = False
                elif (global_result_code==2):
                    self.toolB_WOI_list[k].toolButton_object.setStyleSheet("background-color:\"purple\"")
                    validation_summary_bool = False
                elif (global_result_code==3):
                    self.toolB_WOI_list[k].toolButton_object.setStyleSheet("background-color:\"green\"")


                # Loop over the different checks of a WOI, and format the text output

                for ii in range(0,check_result_array.size):
                    check_result = check_result_array[ii]

                    # Name of the check. Defined in the check script.
                    self.toolB_WOI_list[k].attached_output_text = "%s%s \n\n" % (self.toolB_WOI_list[k].attached_output_text,check_result.check_name)

                    # If the check passes (=green), just display the explanation text defined in the check script.
                    if (check_result.check_result_code==3):
                        self.toolB_WOI_list[k].attached_output_text = "%s%s \n" % (self.toolB_WOI_list[k].attached_output_text,check_result.check_result_text)

                    # Case if the check fails with a simple warning (=yellow)
                    elif (check_result.check_result_code==1):

                        # Case if the check is related to a particular time point (example: related to a waveform)
                        # In which case, the value of the faulty parameter, the limit breached,
                        # the relative and absolute time and the segment the point belongs to are displayed.
                        if (check_result.check_fail_abs_times.size>0):

                            self.toolB_WOI_list[k].attached_output_text = "%sWARNING: %s at the following time points : \n" % (self.toolB_WOI_list[k].attached_output_text,check_result.check_result_text)
                            for kk in range(0,check_result.check_fail_abs_times.size):
                                self.toolB_WOI_list[k].attached_output_text = \
                                '%s\t%d %s (limit %s %s) at absolute time %d s (relative time %d s in segment [%s]) \n' \
                                %(self.toolB_WOI_list[k].attached_output_text, \
                                check_result.check_fail_values[kk], \
                                check_result.check_fail_values_unit, \
                                check_result.check_fail_limit, \
                                check_result.check_fail_values_unit, \
                                check_result.check_fail_abs_times[kk], \
                                check_result.check_fail_rel_times[kk], \
                                check_result.check_fail_segments[kk])

                        # If the check is not time-related, only the faulty parameter value and the limit are displayed
                        else:
                            self.toolB_WOI_list[k].attached_output_text = "%sWARNING: %s %s %s (limit %s %s)"\
                            %(self.toolB_WOI_list[k].attached_output_text, \
                            check_result.check_result_text, \
                            check_result.check_fail_values[0], \
                            check_result.check_fail_values_unit, \
                            check_result.check_fail_limit, \
                            check_result.check_fail_values_unit)

                    # Case if the checks fails with an error (=red)
                    # Same as the block above, except that the message starts with "ERROR" instead of "WARNING"
                    elif (check_result.check_result_code==0):
                        self.toolB_WOI_list[k].toolButton_object.setStyleSheet("background-color:\"red\"")
                        validation_summary_bool = False

                        if (check_result.check_fail_abs_times.size>0):

                            self.toolB_WOI_list[k].attached_output_text = "%sERROR: %s at the following time points : \n" % (self.toolB_WOI_list[k].attached_output_text,check_result.check_result_text)
                            for kk in range(0,check_result.check_fail_values.size):
                                self.toolB_WOI_list[k].attached_output_text = \
                                '%s\t%d %s (limit %s %s) at absolute time %d s (relative time %d s in segment [%s]) \n' \
                                %(self.toolB_WOI_list[k].attached_output_text, \
                                check_result.check_fail_values[kk], \
                                check_result.check_fail_values_unit, \
                                check_result.check_fail_limit, \
                                check_result.check_fail_values_unit, \
                                check_result.check_fail_abs_times[kk], \
                                check_result.check_fail_rel_times[kk], \
                                check_result.check_fail_segments[kk])
                        else:
                            self.toolB_WOI_list[k].attached_output_text = "%sERROR: %s %s %s (limit %s %s)"\
                            %(self.toolB_WOI_list[k].attached_output_text, \
                            check_result.check_result_text, \
                            check_result.check_fail_values[0], \
                            check_result.check_fail_values_unit, \
                            check_result.check_fail_limit, \
                            check_result.check_fail_values_unit)

                    # Case if check fails because the data is not available due to PPAT being in offline mode.
                    # This is for checks only relevant for online situations (example: the current torus pressure)
                    elif (check_result.check_result_code==2):
                        self.toolB_WOI_list[k].toolButton_object.setStyleSheet("background-color:\"purple\"")
                        validation_summary_bool = False
                        self.toolB_WOI_list[k].attached_output_text = "%sDATA NOT AVAILABLE:%s \n" % (self.toolB_WOI_list[k].attached_output_text,check_result.check_result_text)


                # Iterate and move to next colored square.
                k=k+1

            # Reset the counter to move on the next line of checks.
            k=0
            # Same thing as the block above for Protections instead of WOIs.
            for toolB_Protection in self.toolB_Protection_list:

                # Run the check script for a given toolButton_individual_check.
                check_result_array = globals()[toolB_Protection.script_address](self.parent.scenarioAreaWidget.segmentTrajectory,self.parent.scenarioAreaWidget.dpFilename,online_status)

                # Output text: name of the Protection checked.
                self.toolB_Protection_list[k].attached_output_text = '%s\n-------------------------------- \n' %(toolB_Protection.check_name)

                result_code = []

                for ii in range(0,check_result_array.size):
                    result_code.append(check_result_array[ii].check_result_code)
                    global_result_code = min(result_code)

                if (global_result_code==0):
                    self.toolB_Protection_list[k].toolButton_object.setStyleSheet("background-color:\"red\"")
                    validation_summary_bool = False
                elif (global_result_code==1):
                    self.toolB_Protection_list[k].toolButton_object.setStyleSheet("background-color:\"yellow\"")
                    validation_summary_bool = False
                elif (global_result_code==2):
                    self.toolB_Protection_list[k].toolButton_object.setStyleSheet("background-color:\"purple\"")
                    validation_summary_bool = False
                elif (global_result_code==3):
                    self.toolB_Protection_list[k].toolButton_object.setStyleSheet("background-color:\"green\"")


                for ii in range(0,check_result_array.size):
                    check_result = check_result_array[ii]

                    # Name of the check. Defined in the check script.
                    self.toolB_Protection_list[k].attached_output_text = "%s%s \n\n" % (self.toolB_Protection_list[k].attached_output_text,check_result.check_name)

                    # If the check passes (=green), just display the explanation text defined in the check script.
                    if (check_result.check_result_code==3):
                        self.toolB_Protection_list[k].attached_output_text = "%s%s \n" % (self.toolB_Protection_list[k].attached_output_text,check_result.check_result_text)

                    # Case if the check fails with a simple warning (=yellow)
                    elif (check_result.check_result_code==1):

                        # Case if the check is related to a particular time point (example: related to a waveform)
                        # In which case, the value of the faulty parameter, the limit breached,
                        # the relative and absolute time and the segment the point belongs to are displayed.
                        if (check_result.check_fail_abs_times.size>0):

                            self.toolB_Protection_list[k].attached_output_text = "%sWARNING: %s at the following time points : \n" % (self.toolB_Protection_list[k].attached_output_text,check_result.check_result_text)
                            for kk in range(0,check_result.check_fail_abs_times.size):
                                self.toolB_Protection_list[k].attached_output_text = \
                                '%s\t%d %s (limit %s %s) at absolute time %d s (relative time %d s in segment [%s]) \n' \
                                %(self.toolB_Protection_list[k].attached_output_text, \
                                check_result.check_fail_values[kk], \
                                check_result.check_fail_values_unit, \
                                check_result.check_fail_limit, \
                                check_result.check_fail_values_unit, \
                                check_result.check_fail_abs_times[kk], \
                                check_result.check_fail_rel_times[kk], \
                                check_result.check_fail_segments[kk])

                        # If the check is not time-related, only the faulty parameter value and the limit are displayed
                        else:
                            self.toolB_Protection_list[k].attached_output_text = "%sWARNING: %s %s %s (limit %s %s)"\
                            %(self.toolB_Protection_list[k].attached_output_text, \
                            check_result.check_result_text, \
                            check_result.check_fail_values[0], \
                            check_result.check_fail_values_unit, \
                            check_result.check_fail_limit, \
                            check_result.check_fail_values_unit)

                    # Case if the checks fails with an error (=red)
                    # Same as the block above, except that the message starts with "ERROR" instead of "WARNING"
                    elif (check_result.check_result_code==0):
                        self.toolB_Protection_list[k].toolButton_object.setStyleSheet("background-color:\"red\"")
                        validation_summary_bool = False

                        if (check_result.check_fail_abs_times.size>0):

                            self.toolB_Protection_list[k].attached_output_text = "%sERROR: %s at the following time points : \n" % (self.toolB_Protection_list[k].attached_output_text,check_result.check_result_text)
                            for kk in range(0,check_result.check_fail_values.size):
                                self.toolB_Protection_list[k].attached_output_text = \
                                '%s\t%d %s (limit %s %s) at absolute time %d s (relative time %d s in segment [%s]) \n' \
                                %(self.toolB_Protection_list[k].attached_output_text, \
                                check_result.check_fail_values[kk], \
                                check_result.check_fail_values_unit, \
                                check_result.check_fail_limit, \
                                check_result.check_fail_values_unit, \
                                check_result.check_fail_abs_times[kk], \
                                check_result.check_fail_rel_times[kk], \
                                check_result.check_fail_segments[kk])
                        else:
                            self.toolB_Protection_list[k].attached_output_text = "%sERROR: %s %s %s (limit %s %s)"\
                            %(self.toolB_Protection_list[k].attached_output_text, \
                            check_result.check_result_text, \
                            check_result.check_fail_values[0], \
                            check_result.check_fail_values_unit, \
                            check_result.check_fail_limit, \
                            check_result.check_fail_values_unit)

                    # Case if check fails because the data is not available due to PPAT being in offline mode.
                    # This is for checks only relevant for online situations (example: the current torus pressure)
                    elif (check_result.check_result_code==2):
                        self.toolB_Protection_list[k].toolButton_object.setStyleSheet("background-color:\"purple\"")
                        validation_summary_bool = False
                        self.toolB_Protection_list[k].attached_output_text = "%sDATA NOT AVAILABLE:%s \n" % (self.toolB_Protection_list[k].attached_output_text,check_result.check_result_text)


                # Iterate and move to next colored square.
                k=k+1

            # Reset the counter to move on the next line of checks.
            k=0




            # Same thing as the block above for Machine Configuration instead of Protections or WOIs
            for toolB_MachineConfig in self.toolB_MachineConfig_list:

                # Run the check script for a given toolButton_individual_check.
                check_result_array = globals()[toolB_MachineConfig.script_address](self.parent.scenarioAreaWidget.segmentTrajectory,self.parent.scenarioAreaWidget.dpFilename,online_status)

                # Output text: name of the MachineConfig checked.
                self.toolB_MachineConfig_list[k].attached_output_text = '%s\n-------------------------------- \n' %(toolB_MachineConfig.check_name)

                result_code = []

                for ii in range(0,check_result_array.size):
                    result_code.append(check_result_array[ii].check_result_code)
                    global_result_code = min(result_code)

                if (global_result_code==0):
                    self.toolB_MachineConfig_list[k].toolButton_object.setStyleSheet("background-color:\"red\"")
                    validation_summary_bool = False
                elif (global_result_code==1):
                    self.toolB_MachineConfig_list[k].toolButton_object.setStyleSheet("background-color:\"yellow\"")
                    validation_summary_bool = False
                elif (global_result_code==2):
                    self.toolB_MachineConfig_list[k].toolButton_object.setStyleSheet("background-color:\"purple\"")
                    validation_summary_bool = False
                elif (global_result_code==3):
                    self.toolB_MachineConfig_list[k].toolButton_object.setStyleSheet("background-color:\"green\"")


                for ii in range(0,check_result_array.size):
                    check_result = check_result_array[ii]

                    # Name of the check. Defined in the check script.
                    self.toolB_MachineConfig_list[k].attached_output_text = "%s%s \n\n" % (self.toolB_MachineConfig_list[k].attached_output_text,check_result.check_name)

                    # If the check passes (=green), just display the explanation text defined in the check script.
                    if (check_result.check_result_code==3):
                        self.toolB_MachineConfig_list[k].attached_output_text = "%s%s \n" % (self.toolB_MachineConfig_list[k].attached_output_text,check_result.check_result_text)

                    # Case if the check fails with a simple warning (=yellow)
                    elif (check_result.check_result_code==1):

                        # Case if the check is related to a particular time point (example: related to a waveform)
                        # In which case, the value of the faulty parameter, the limit breached,
                        # the relative and absolute time and the segment the point belongs to are displayed.
                        if (check_result.check_fail_abs_times.size>0):

                            self.toolB_MachineConfig_list[k].attached_output_text = "%sWARNING: %s at the following time points : \n" % (self.toolB_MachineConfig_list[k].attached_output_text,check_result.check_result_text)
                            for kk in range(0,check_result.check_fail_abs_times.size):
                                self.toolB_MachineConfig_list[k].attached_output_text = \
                                '%s\t%d %s (limit %s %s) at absolute time %d s (relative time %d s in segment [%s]) \n' \
                                %(self.toolB_MachineConfig_list[k].attached_output_text, \
                                check_result.check_fail_values[kk], \
                                check_result.check_fail_values_unit, \
                                check_result.check_fail_limit, \
                                check_result.check_fail_values_unit, \
                                check_result.check_fail_abs_times[kk], \
                                check_result.check_fail_rel_times[kk], \
                                check_result.check_fail_segments[kk])

                        # If the check is not time-related, only the faulty parameter value and the limit are displayed
                        else:
                            self.toolB_MachineConfig_list[k].attached_output_text = "%sWARNING: %s %s %s (limit %s %s)"\
                            %(self.toolB_MachineConfig_list[k].attached_output_text, \
                            check_result.check_result_text, \
                            check_result.check_fail_values[0], \
                            check_result.check_fail_values_unit, \
                            check_result.check_fail_limit, \
                            check_result.check_fail_values_unit)

                    # Case if the checks fails with an error (=red)
                    # Same as the block above, except that the message starts with "ERROR" instead of "WARNING"
                    elif (check_result.check_result_code==0):
                        self.toolB_MachineConfig_list[k].toolButton_object.setStyleSheet("background-color:\"red\"")
                        validation_summary_bool = False

                        if (check_result.check_fail_abs_times.size>0):

                            self.toolB_MachineConfig_list[k].attached_output_text = "%sERROR: %s at the following time points : \n" % (self.toolB_MachineConfig_list[k].attached_output_text,check_result.check_result_text)
                            for kk in range(0,check_result.check_fail_values.size):
                                self.toolB_MachineConfig_list[k].attached_output_text = \
                                '%s\t%d %s (limit %s %s) at absolute time %d s (relative time %d s in segment [%s]) \n' \
                                %(self.toolB_MachineConfig_list[k].attached_output_text, \
                                check_result.check_fail_values[kk], \
                                check_result.check_fail_values_unit, \
                                check_result.check_fail_limit, \
                                check_result.check_fail_values_unit, \
                                check_result.check_fail_abs_times[kk], \
                                check_result.check_fail_rel_times[kk], \
                                check_result.check_fail_segments[kk])
                        else:
                            self.toolB_MachineConfig_list[k].attached_output_text = "%sERROR: %s %s %s (limit %s %s)"\
                            %(self.toolB_MachineConfig_list[k].attached_output_text, \
                            check_result.check_result_text, \
                            check_result.check_fail_values[0], \
                            check_result.check_fail_values_unit, \
                            check_result.check_fail_limit, \
                            check_result.check_fail_values_unit)

                    # Case if check fails because the data is not available due to PPAT being in offline mode.
                    # This is for checks only relevant for online situations (example: the current torus pressure)
                    elif (check_result.check_result_code==2):
                        self.toolB_MachineConfig_list[k].toolButton_object.setStyleSheet("background-color:\"purple\"")
                        validation_summary_bool = False
                        self.toolB_MachineConfig_list[k].attached_output_text = "%sDATA NOT AVAILABLE:%s \n" % (self.toolB_MachineConfig_list[k].attached_output_text,check_result.check_result_text)


                # Iterate and move to next colored square.
                k=k+1

            # Reset the counter just in case.
            k=0


            # Write and display the summary text once all the checks are finished.

            Summary_text = "Summary\n-------------------------------- \n"

            if validation_summary_bool:
                self.textBrowser_results.setText("%s All checks OK\n"%Summary_text)
            else:
                self.textBrowser_results.setText("%sSome checks failed. Click individual buttons for more details. \n"%Summary_text)
        else:
            self.textBrowser_results.setText("Unable to perform checks: please load DCS files first!\n")


    def resetChecks(self):
    # Method to reset the checks. Called when a new scenario is loaded
    # Note that only the text of toolButton_individual_checks objects is reset. Some other parameters are not reset
    # This could be improved in the future (or by graying out the "check now" button)
        self.textBrowser_results.setText("New plasma scenario. Please run checks.\n")

        for k in range(len(self.toolB_WOI_list)):
            self.toolB_WOI_list[k].attached_output_text = ''
            self.toolB_WOI_list[k].toolButton_object.setStyleSheet("background-color:\"black\"")

        for k in range(len(self.toolB_Protection_list)):
            self.toolB_WOI_list[k].attached_output_text = ''
            self.toolB_WOI_list[k].toolButton_object.setStyleSheet("background-color:\"black\"")

        for k in range(len(self.toolB_MachineConfig_list)):
            self.toolB_WOI_list[k].attached_output_text = ''
            self.toolB_WOI_list[k].toolButton_object.setStyleSheet("background-color:\"black\"")


    # Method to reset the checks. Called when the watchdog detects a DCS file change.
    # Same as the method above. Only the text message changes.
    # Note that only the text of toolButton_individual_checks objects is reset. Some other parameters are not reset
    # This could be improved in the future (or by graying out the "check now" button)
    def resetScenario(self):
        self.textBrowser_results.setText("XML DCS files changed or removed. Please re-load files.\n")

        for k in range(len(self.toolB_WOI_list)):
            self.toolB_WOI_list[k].attached_output_text = ''
            self.toolB_WOI_list[k].toolButton_object.setStyleSheet("background-color:\"black\"")

        for k in range(len(self.toolB_Protection_list)):
            self.toolB_WOI_list[k].attached_output_text = ''
            self.toolB_WOI_list[k].toolButton_object.setStyleSheet("background-color:\"black\"")

        for k in range(len(self.toolB_MachineConfig_list)):
            self.toolB_WOI_list[k].attached_output_text = ''
            self.toolB_WOI_list[k].toolButton_object.setStyleSheet("background-color:\"black\"")

    # Method to reset the checks. Called when the load DCS file operation fails (no file found or cancelled by user)
    # Same as the method above. Only the text message changes.
    # Note that only the text of toolButton_individual_checks objects is reset. Some other parameters are not reset
    # This could be improved in the future (or by graying out the "check now" button)
    def WrongDCSFile(self):
        self.textBrowser_results.setText("Sup.xml or DP.xml file not found.\nPlease reload or find the files manually.")

        for k in range(len(self.toolB_WOI_list)):
            self.toolB_WOI_list[k].attached_output_text = ''
            self.toolB_WOI_list[k].toolButton_object.setStyleSheet("background-color:\"black\"")

        for k in range(len(self.toolB_Protection_list)):
            self.toolB_WOI_list[k].attached_output_text = ''
            self.toolB_WOI_list[k].toolButton_object.setStyleSheet("background-color:\"black\"")

        for k in range(len(self.toolB_MachineConfig_list)):
            self.toolB_WOI_list[k].attached_output_text = ''
            self.toolB_WOI_list[k].toolButton_object.setStyleSheet("background-color:\"black\"")


# Class defining a toolButton check object
# Attributes:
# - A toolButton to be colored as a function of the check result (red, yellow, green or purple)
# - The text to be displayed in the text area
# - The address of the text area to display the output text in.
# Method:
# - Display the text attribute in the text area (result of a check)
class toolButton_individual_check:
    def __init__(self,parentWidget,text_frame):
        self.check_name = ''
        self.script_address = ''
        self.toolButton_object = QtWidgets.QToolButton()
        self.toolButton_object.setStyleSheet("background-color:\"black\"")
        self.toolButton_object.setObjectName('')
        self.toolButton_object.setText("...")
        self.attached_output_text = ''
        self.text_frame = text_frame
        parentWidget.addWidget(self.toolButton_object, QtCore.Qt.AlignLeft)

    def click_detailed_output(self):
        object_name = self
        self.text_frame.setText(self.attached_output_text)
