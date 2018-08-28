# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 17:05:46 2018

@author: JH218595
"""
from xml.etree import ElementTree
import numpy as np
import logging
logger = logging.getLogger(__name__)

class DCSSettings():
    def __init__(self, filename):
        """
        DCS Settings

        Parameters
        ----------
        filename: str
            filename is is the path of a DCS-formatted supervision file
            (typically Sup.xml).

        """
        try:
            ## getting root of xml file
            self.tree = ElementTree.parse(filename)
            self.root = self.tree.getroot()
            logger.info(f'DCS file {filename} openned')

        except FileNotFoundError:
            logger.error('DCS XML file not found !')

    @property
    def nominal_scenario(self):
        """
        scenario = get_nominal_scenario()

        Returns the nominal scenario of a pulse from a DCS-format settings.

        Returns
        -------
        scenario : n x 3 Numpy array
            Array describing the nominal scenario.

        Example :
        >> DCS_settings = DCSSettings('Sup.xml')
        >> scenario = DCS_settings.nominal_scenario()

        >> scenario =
        [['Init' '34.0' '34.0']
         ['segment1' '34.1' '0.1']]

        The first column is the name of the segment as defined in Xedit by the session leader
        The second column is the absolute time at which the segment ends (the first segment starts
        at 0.0s. The third column is the duration of the segment. Note that the duration information
        is theorticaly redundant but is kept for practical purposes to avoid making substractions
        every time the duration information is needed.

        Note that the nominal scenario is, by convention, the sequence of segments which contain
        the most segments with number less than a 100. Segments with number > 100 are (also by
        convention) either backup segments or stop segments.


        Bug reports and suggestions are welcome.

        ---
        C. Reux - January 2017. Based on initial work by H. Joshi
        J. Hillairet 2018
        """
        # code refactoring. Changes:
        # arrTargetSeg -> self.target_segments
        # arrSearchSeg -> self.segment_trajectories
        # arrSegment -> self.nominal_scenario

        # Search all possible scenarios
        all_scenarios = self.search_all('Init', 'TheEnd')

        def clean_array(array):
            """ convenient function to remove '->' and 'TheEnd' from a list """
            cleaned_array = [value for value in array if
                      not value.startswith('->') and
                      not value.startswith('TheEnd')]
            return cleaned_array
        
        # Search the nominal scenario among all possible scenarios
        # The nominal scenario is defined as the one containing the most segments
        # with ID numbers < 100
        longest=0
        # Loop over all possible scenarios
        for i in range(0,len(all_scenarios)):
            arrSearch_temp = clean_array(all_scenarios[i])
            count_nominal = 1
            # Loop over the segments in the chosen scenario
            for ii in range(1,len(arrSearch_temp)):
                # Count the number of segments with ID < 100
                segment_id = float(arrSearch_temp[ii][7:])
                if segment_id<100:
                    count_nominal = count_nominal+1
            shortest = count_nominal
            if( shortest > longest):
                longest = shortest
                choice = i

        # Get the nominal scenario
        nominal_trajectory = clean_array(all_scenarios[choice])

        # Determination of all segments and transition ways
        nominal_segment = self.prepare_arrSegment(nominal_trajectory, self.target_segments)
        # transform the flat list into a list of tuples: (segment_name, t_start, t_end) 
        nominal_segment = list(zip(*[iter(nominal_segment)]*3))
        return nominal_segment


    @property
    def target_segments(self):
        """
        Returns a list of all the segments and all the ways to transit from
        them to other segments. Contains the segment name, the target segment,
        the name of the jump condition, the (maximum) time at which the jump
        can take place.
        The list is organized as follow:

        [[segment_name, target_segment, jump_condition, jump_time],
         [segment_name, target_segment, jump_condition, jump_time],
         ...]

        Returns
        -------
        target_segments : list
            all segments and transition ways
        """
        seg_sr = 1
        main_segment = []
        target_segments = []

        for segments in self.root.findall('SegmentList'):
            for segment in segments:
                name = segment.get('name')
                main_segment.append(name)

                targets = []
                # Search for the watchdog jump condition
                # (i.e. the longest possible duration of the segment)
                for control in segment:
                    if (control.get('program')=='Watchdog'):
                        # Careful: startTime is actually the time at which
                        # the watchdog jump condition kicks in. This is
                        # actually the end of the segment, not its beginning
                        start_time = control.get('startTime')

                # Loop over other jump conditions
                for control in segment:
                    target_segment = control.get('targetSegment')
                    program = control.get('program')

                    # Avoid redundant scenarios if several jump conditions
                    # lead to the same segments. Note that in reality, their
                    # startTime may be different.
                    # This is not taken into account.
                    if not target_segment in targets:
                        # Adding target segment properties in arrTargetSeg array
                        #if (program == "Watchdog" or program == "StartUp" ):
                        targets.append(target_segment)
                        target_segments.append([name, target_segment, program, start_time, seg_sr])
                        seg_sr += 1

        return target_segments

    def prepare_arrSegment(self, arrSearch, arrTargetSeg):
        arrSegment = []
        #### After selection of trajectory and fill arrSegment with segments and time information
        #### re declare arrSegment array to freshly append selected choice of trajectory
        startTime=0.0
        for i in range(0,len(arrSearch)):
            segment_done = 0
            for j in range(0,len(arrTargetSeg)):
                # Note: only one transition is considered at the moment
                # This assumes that all transitions happen at Watchdog time.
                if (arrSearch[i] == arrTargetSeg[j][0]) and not segment_done:
                    startTime = startTime+float(arrTargetSeg[j][3])
                    arrSegment.append(arrSearch[i])
                    arrSegment.append(startTime)
                    arrSegment.append(float(arrTargetSeg[j][3]))
                    segment_done = 1

        return arrSegment

    def search_all(self, start, end, path=[], seg_traj=None):
        """
        Search into all the possible segments for the ones which start and end
        by the defined segment names.

        Aguments
        --------
        start : str
            segment start name
        end : str
            segment end name
        path: list, optional
            segment path trajectory (ex: 'A->D->G->E'), used for recursion only
            default value is []
        seg_traj: list, optional
            segment trajectories list, used for recursion only
            default value is None

        Returns
        -------
        path: list
            final segment path trajectory
        """
        # Recursive search of all scenarios
        if not seg_traj:
            seg_traj = self.segment_trajectories
        ar = ['->']
        path = path + [start]+ar
        if start == end:
            return [path]

        if start not in seg_traj:
            return []

        paths = []
        for node in seg_traj[start]:
            if node not in path:
                newpaths = self.search_all(node, end, path, seg_traj)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    @property
    def segment_trajectories(self):
        """
        Creates an array which segment names as indexes to avoid only one
        occurrence of each segment.
        arrSearSeg gives the segments which it is possible to jump to
        starting from the index segment.
        """
        segment_trajectories = dict()

        for segment in self.target_segments:
            segment_name = segment[0]
            segment_target = segment[1]
            # set dict[segment_name]=empty list if segment_name not already in dict.
            # then append the target into the list
            segment_trajectories.setdefault(segment_name, []).append(segment_target)

            pass

        return segment_trajectories

if __name__ == '__main__':
    """ Testing purpose """
    DCS_settings = DCSSettings('../resources/pulse_setup_examples/52865/Sup.xml')
    ns = DCS_settings.nominal_scenario
    print(ns)
