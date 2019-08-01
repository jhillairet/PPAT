import numpy as np
import xml.etree.ElementTree as Et
import re

import logging
logger = logging.getLogger(__name__)

class Waveform():
    """
    Waveform data

    A Waveform represent a Signal evolving in time

    """
    def __init__(self, name=None,
                 times=None, reltimes=None,
                 values=None, segments=None):
        self.times = np.array(times)          # absolute time vector
        self.reltimes = np.array(reltimes)    # relative (=inside the segment) time vector
        self.values = np.array(values)        # Value vector
        self.segments = segments    # Segment number of each point
        self.name = name
        
    def __repr__(self):
        " meaningfull representation "
        return f'DCS Waveform: "{self.name}", ({len(self.segments)} segments)'
    
    @property
    def nominal(self):
        """
        Return the waveform without the termination segments (segments # >=900)
        """
        # get the indexes of termination segments
        idxs = []
        for (ids, segment) in enumerate(self.segments):
            # regular expression to find other segments than termination segments
            if re.match('(segment9)[0-9][0-9]', segment) is None:
                idxs.append(ids)
        # create a new waveform
        times = [self.times[i] for i in idxs]
        reltimes = [self.reltimes[i] for i in idxs]
        values = [self.values[i] for i in idxs]
        segments = [self.segments[i] for i in idxs]
        name = self.name
        
        return Waveform(name=name, 
                        times=times, reltimes=reltimes,
                        values=values, segments=segments)
        

def get_waveform(waveform_name, waveforms):
    """
    Retrieve a waveform from a waveform list
    
    Parameters
    ----------
        waveform_name : str
            Name of the waveform to look for
            
        waveforms: list
            List of Waveform objects
            
    Return
    ------
        waveform: Waveform object
            None is the waveform has not been found in the waveforms list
    
    """
    waveform = None
    for wf in waveforms:
        if wf.name == waveform_name:
            waveform = wf
    return waveform
            
def get_all_waveforms(scenario, DP_file):
    """
    extract all the waveforms for the given scenario
    
    Parameters
    ----------
        scenario: List of tuples
            scenario trajectory
        DP_file: string
            path to the DP.xml file
    
    Return
    ------
        scenario_waveforms: List
            List of all waveforms for the given scenario
    """
    sig_names = get_DCS_signal_names(DP_file)
    scenario_waveforms = waveformBuilder(scenario, sig_names, DP_file)
    return scenario_waveforms
    

def get_DCS_signal_names(DP_file):
    """
    Return the list of all the DCS signal names available in the DP_file
    
    Parameters
    ----------
        DP_file: string
            path to the DCS xml file containing the waveform informations 
            (usually DP.xml)
            
    Returns
    -------
        signal_names: list
            List of all DCS signal names available in the DCS xml file
    """
    # xml file parsing.
    tree = Et.parse(DP_file)
    xmlroot = tree.getroot()
    
    signal_names = []
    for SIGNAL in xmlroot.findall('DECLARATIONS/SIGNALS/SIGNAL'):
        signal_names.append(SIGNAL.attrib['name'])
    
    return signal_names

def waveformBuilder(arrSegment, signal_list, infile):
    """
    OUTPUT_WAVEFORM_PACK = waveformBuilder(ARRSEGMENT,SIGNAL_LIST,INFILE)

    Builds waveforms of a given signals following a chosen scenario.

    scenario: list of tuples
        chosen scenario, for example as provided by DCSSettings.nominal_scenario()
        It is a list of tuples formatted this way
        [( , , ),
         ( , , ),
         ( , , )]

    ARRSEGMENT is the chosen scenario as provided by segmentTrajectoryFinder.py
    It is a numpy string array and should be formatted this way:
    [[segmentname1 AbsoluteEndtime1 Duration1]
    [segmentname2 AbolsuteEndtime2 Duration2]
    [segmentname3 AbsoluteEndtime3 Duration3]
    [... ... ...]]

    Example:
    [['Init' '34.0' '34.0']
    ['segment1' '35.5' '1.5']
    ['segment2' '37.0' '2.0']]

    All times in seconds.
    See the documentation of the segmentTrajectoryFinder.py for more details.

    SIGNAL_LIST is a numpy string array of the signals for which the waveforms are to be built.
    Signal names are DCS names.

    INFILE is the path of the DCS xml containing the waveform information
    Usual name is DP.xml

    OUTPUT_WAVFORM_PACK is an array of waveform_packs objects. It contains the reconstructed
    waveform data as well as their position in the segment sequence.
    The class is defined in waveform_pack.py.

    OUTPUT_WAVEFORM_PACK.times is the absolute time vector. Numpy float array
    OUTPUT_WAVEFORM_PACK.reltimes is the relative time vector (i.e. the time of the point inside
    the segment it belongs to. Numpy float array.
    OUTPUT_WAVEFORM_PACK.values is the data vector. Units are defined by DCS and are
    usually SI. Numpy float array.
    OUTPUT_WAVEFORM_PACK.segments is a vector indicating which segment each data point
    belongs to. Numpy string array.

    Features currently implemented:
    - Linear or Step-executed waveforms
    - Absolute or relative waveforms (note: in DCS, relative means relative to the start of the segment)

    Features not yet implemented:
    - Global forward-transition-times for waveforms (JET-like feature). Not yet implemented in Xedit anyway.
    - Proportional control for Inh/b coils (proportional means proportional to Ip).
      The reconstructed waveform in this case will only be the proportional factor F in kA/MA, not Ip*F in kA
    - Envelopes proportional to the reference theyr are related are not functional.

    Bug reports and suggestions are welcome.

    --
    C. Reux - Januray 2017. Based on initial work by H. Joshi

    """

    # xml file parsing.
    tree = Et.parse(infile)
    xmlroot = tree.getroot()

    # List of waveforms for final result storage.
    waveforms = []

    # Loop over all signals requested by the user.
    for signal_to_search in signal_list:

#        # Initialization of a single waveform_pack object, to be appended with others in case several
#        # signals are requested.
#        single_waveform_pack = Waveform()

        ### Declare array to store signal default data from Signal definition in DP file
        #arrSignal = np.array([])

        # Look for signal default and general values in the DCS xml file
        signal_declaration = get_signal_declaration(xmlroot, signal_to_search)

        # Find all signal points for the requested signal type in all segments
        signal_trajectory = search_signal_trajectory(xmlroot, signal_to_search)

        [segments, times, reltimes, values] = prepare_final(xmlroot, arrSegment, signal_trajectory, signal_declaration)

        waveforms.append(Waveform(name=signal_declaration.name, times=times, reltimes=reltimes, values=values, segments=segments))


    return(waveforms)




class Signal():
    """
    Signal class

    A Signal is a physical or engineering property defined for a fixed time.

    time: relative time wrt to the segment

    """
    _defaults = ['name', 'signal_type', 'type', 'dimension', 'default_value',
                 'time', 'segment_name', 'value', 'name', 'exec_rule']
    _default_value = None

    def __init__(self, **kwargs):
        self.__dict__.update(dict.fromkeys(self._defaults, self._default_value))
        self.__dict__.update(kwargs)

    def __repr__(self):
        return f'Signal({self.name}): value({self.segment_name}@t={self.time})={self.value} [{self.exec_rule}]; {self.signal_type}({self.type})={self.default_value} .\n'




def get_signal_declaration(xmlroot, signal_to_search):
    """
    Retrieves the signal declaration in the xml file:
        default values, type, dimension, etc.)

    Parameters
    ----------
        xmlroot: xml.etree.ElementTree.Element
            root of the DP.xml file

        signal_to_search: string
            Signal name to search for

    Return
    -------
        signals: list of Signal()

    """
    signals = []

    for SIGNAL in xmlroot.findall('DECLARATIONS/SIGNALS/SIGNAL'):
        name = SIGNAL.attrib['name']
        if (name == signal_to_search):
            for DEFAULT_VALUE in SIGNAL:
                try:
                    default_value = float(DEFAULT_VALUE.text.strip('\n\ \r\t'))
                except (TypeError, AttributeError, ValueError) as e:  # case if not defined
                    default_value = 0.0

            signal = Signal(name=name,
                            signal_type=SIGNAL.attrib['signal_type'],
                            type=SIGNAL.attrib['type'],
                            dimension=SIGNAL.attrib['dimension'],
                            default_value=default_value)

            signals.append(signal)
    return signals[0] # TODO ? can a signal has multiple declaration

def search_signal_trajectory(xmlroot, signal_to_search):
    """
    Finds all occurrences of a signal in all segments.

    Parameters
    ----------
        xmlroot: xml.etree.ElementTree.Element
            root of the DP.xml file

        signal_to_search: string
            Signal name to search for

    Return
    ------
        signal_trajectory: list
            List of Signals

    """

    # Initialization of the output array for all occurences of a signal in segments.
    signal_trajectory = []

    # Loop over the segments
    for SEGMENT in xmlroot.findall("SEGMENTS/SEGMENT"):
        # Enable the following to check segment detail
        # print(SEGMENT.attrib,SEGMENT.tag)
        segment_name = SEGMENT.attrib['Id']

        # Initial confusion between segment Id and segment name.
        # Aims at keeping the identification set by SLs in Xedit
        # Rename the first segment using the identifier
        if segment_name=='0':
            segment_name='Init'
        else:
            segment_name='segment%s' %(segment_name)

        # Loop over all the waveforms available for a given the segment to find the one
        # the user is interested in.
        for SIGNAL_TRAJECTORIES in SEGMENT:
            for SIGNAL_TRAJECTORY in SIGNAL_TRAJECTORIES:
                # Assign signal name to signalTrajectory variable
                signalTrajectory = SIGNAL_TRAJECTORY.attrib['Name']
                # Execution rule is step (mostly for flags) or Linear (for normal references)
                executionRule = SIGNAL_TRAJECTORY.find('EXECUTION_RULE').attrib['is']
                # Look for the signal we are interested in.
                if (signalTrajectory == signal_to_search):
                    # For the desired signal, gather all time points in the segment and their related information
                    for REFERENCE in SIGNAL_TRAJECTORY:
                        for POINT in REFERENCE:
                            for VALUE in POINT:
                                sig = Signal(segment_name=segment_name,
                                             time=float(POINT.get("time")),
                                             type=VALUE.get("type"),
                                             dimension=VALUE.get("dimension"),
                                             value=float(VALUE.text),#.strip('\n\r\ \t'),
                                             signal_name=signalTrajectory,
                                             exec_rule=executionRule)
                                # Extract all information about a data point
                                signal_trajectory.append(sig)

    return signal_trajectory


### preparing waveform_pack with final result combining arrSegment and arrsignalTrajectory
def prepare_final(xmlroot, arrSegment, arrsignalTrajectory, arrSignal):
    """
    Assembly of the final waveform. Features: Takes into account step or linear executed waveforms.
    """
    #PCS time cycle in seconds. Used for jumps at the beginning of a segment
    PCS_CYCLE_TIME = 0.002

    # Number of explicit data points in all segments.
    nb_signals = len(arrsignalTrajectory)

    # Number of segments in the scenario.
    #rowsSegment = int(len(arrSegment))
    nb_segments = len(arrSegment)

    #  Output arrays containing the waveform data points
    # (absolute time, relative time, data and associated segment).
    times_output = []
    relative_times_output = []
    values_output = []
    segments_output = []
    segmentTime = 0.0

    signal_trajectory_names = []
    for signal in arrsignalTrajectory:
        signal_trajectory_names.append(signal.name)

    # Iterate segments and build the waveform segment by segment.
    for j, segment in enumerate(arrSegment):
        segment_name = segment[0]

        # Guard test to make sure there is at least one explicit data point.
        # Otherwise there is no point determining the waveform type (relative/absolute)
        # or try to build the waveform (default value only)
        if nb_signals > 0:
            waveformType = waveformTypefinder(xmlroot, segment_name, signal_trajectory_names)
        else:
            break

        # First point of the first segment. Whatever signalTrajectory contains,
        # the start of a segment is considered as a real point by the PCS.
        # On any other segment than the first, the signal value at the end
        # of the previous segment is used.
        # On the first segment, the signal default value is used.
        # Note: LastPointIn is used in case points have been defined outside
        # the segment duration. See below.
        if j == 0:
            # Start time of the segment
            segmentTime = 0.0

            # Default value from the signal declaration.
            waveformValue = float(arrSignal.default_value)

            # Segment the point belongs to (i.e. the current segment)
            segments_output.append(segment_name)

            # Absolute time
            times_output.append(segmentTime)

            # Relative time
            relative_times_output.append(segmentTime)

            # Append the value to the vector
            values_output.append(waveformValue)

            # LastValue is used for relative waveforms
            # (can be on the segment immediately after)
            lastValue = waveformValue

            # Starting value of the segment. Used for relative waveforms
            startValueSegment = waveformValue

            # Same remark as lastValue
            lastTime = segmentTime

            # Flag to check if the lastPoint in the segment is inside
            # its time boundaries.
            # Used to ignore any subsequent point after the single one
            # which could be defined outside.
            # See below.
            lastPointIn = True
            #print('First point of first segment')

        # First point of any segment except the first one.
        else:
            segmentTime = float(arrSegment[j-1][1])
            segments_output.append(segment_name)
            times_output.append(segmentTime)
            # First tpoint of the segment. Therefore the relative time is 0.0s.
            relative_times_output.append(0.0)
            values_output.append(waveformValue)
            lastValue = waveformValue
            startValueSegment = waveformValue
            lastTime = segmentTime
            lastPointIn = True
            #print('First point of any segment except first')

        # Other points in the segment (i.e. not the first point)
        # Loop over the explicit points defined in the signal trajectory to search if
        # one of them belongs to the current segment.
        for i, signal in enumerate(arrsignalTrajectory): #range(0, nb_signals):

#            print(f"current signal: {arrsignalTrajectory[i]}")
#            print(f"current segment: {segment}")

            # Case where an explicit point exists in the current segment.
            if (arrsignalTrajectory[i].segment_name == arrSegment[j][0]):
#                print(f'## Found a point in segment {arrSegment[j][0]}:')
#                print(f'Point: time raw rel={arrsignalTrajectory[i].time} -> {arrsignalTrajectory[i].value}')

                # Case for the first segment (absolute time is zero)
                if j == 0:
                    segment_duration = float(arrSegment[j][1])
                # Any other segment
                else:
                    #segment_duration = float(arrSegment[j,1])-float(arrSegment[j-1,1])
                    segment_duration = float(arrSegment[j][2]) #Mod CR 20170517. Old calculation had a rounding error.



                # Case of a normal point defined within the segment time boundaries.
                if (arrsignalTrajectory[i].time <= segment_duration):

                    # Special case if the first defined point in the segment
                    # is also the beginning of the segment
                    # (or one less than one time step away from it)
                    # In this case, a jump is done from the value in
                    # the last segment to the current value within
                    # the duration of one time cycle.
                    if arrsignalTrajectory[i].time < PCS_CYCLE_TIME:
                        waveformTime_rel = arrsignalTrajectory[i].time + PCS_CYCLE_TIME
                        #print('First point in segment is the beginning of the segment')
                        #print('FPITBOS: %d'%(waveformTime_rel))

                    else:
                        waveformTime_rel = arrsignalTrajectory[i].time
                        #print('First point in segment is NOT the beginning of the segment')

                    segmentName = arrSegment[j][0]

                    # Case for the first segment:
                    # the end time of the previous segment (=start time of the
                    # current one) is not yet defined.
                    # In this case, the starting time is imply 0.0s
                    if j == 0:
                        segmentTime = 0.0
                    # Other segments.
                    # The starting segment time is used extensively
                    # to build the absolute time vectors.
                    else:
                        segmentTime = float(arrSegment[j-1][1])

                    # TODO : Attention !
                    # Polo :les courants sont définis de façon relative
                    # par rapport au courant plasma, mais pas toujours !

                    # Treatment of execution mode: linear, relative or step
                    # Case 1: Linear interpolation in between points
                    exec_rule = str.lower(arrsignalTrajectory[i].exec_rule)
                    if exec_rule == 'linear':

                        # Treatment of the waveform type (absolute/relative)
                        # Case for absolute waveform
                        if waveformType == 'absolute':
                            waveformValue = arrsignalTrajectory[i].value
                        # Case for relative waveform(i.e. relative to the value at the beginning of the segment
                        # In the PCS, the measured value is used rather than the reference value (obviously not available
                        # in the pre-analysis tool).
                        elif waveformType == 'relative':
                            waveformValue = arrsignalTrajectory[i].value * startValueSegment
                        else:
                            raise(NotImplementedError('waveformType proportional not implemented'))

                        waveformTime = segmentTime + waveformTime_rel
                        segments_output.append(segmentName)
                        times_output.append(waveformTime)
                        relative_times_output.append(waveformTime_rel)
                        values_output.append(waveformValue)
                        lastValue = waveformValue
                        lastTime = waveformTime
                        lastPointIn = True

                    # Case 2: Step interpolation in between points.
                    # The jump is done in one time cycle.
                    # An escape condition is added in case the point time coincides with the end of the segment.
                    # Keeping such points would finish the step in the next segment, which builds a non-monotonous
                    # time vector. The point is therefore rejected. TO BE COMPARED WITH WHAT DCS ACTUALLY DOES.
                    # Note that two points are added to the waveform: the one juste before the step, and
                    # another one at the top of the step.
                    elif (exec_rule == 'step') and \
                          ((waveformTime_rel + segmentTime) < (float(arrSegment[j][1]) - PCS_CYCLE_TIME)):
                        waveformValue = lastValue
                        waveformTime = segmentTime + waveformTime_rel
                        segments_output.append(segmentName)
                        times_output.append(waveformTime)
                        relative_times_output.append(waveformTime_rel)
                        values_output.append(waveformValue)

                        if waveformType == 'absolute':
                            waveformValue2 = arrsignalTrajectory[i].value
                        elif waveformType == 'relative':
                            waveformValue2 = arrsignalTrajectory[i].value * startValueSegment
                        else:
                            raise(NotImplementedError('waveformType proportional not implemented!'))

                        waveformTime2 = waveformTime + PCS_CYCLE_TIME
                        segments_output.append(segmentName)
                        times_output.append(waveformTime2)
                        relative_times_output.append(waveformTime_rel + PCS_CYCLE_TIME)
                        values_output.append(waveformValue2)
                        lastValue = waveformValue2
                        lastTime = waveformTime2
                        lastPointIn = True

                # Case 3: a linear-executed point is defined after the end of the segment. The linear ramp
                # between the last two points is started but interrupted before the end of the segment.
                # A point is created at the very end of the segment.
                # Any subsequent point is ignored.
                # Step-executed points defined after the end of the segment are obviously ignored.
                elif ((arrsignalTrajectory[i].time > segment_duration) and
                      lastPointIn and exec_rule == 'linear'):
                    segmentName = arrSegment[j][0]
                    segmentTime = float(arrSegment[j-1][1])

                    waveformTime_rel = arrsignalTrajectory[i].time
                    waveformOutTime = segmentTime + waveformTime_rel
                    waveformOutValue = arrsignalTrajectory[i].value

                    waveformTime = float(arrSegment[j][1])

                    # Interpolation at the segment end time between the last available point and the point defined
                    # outside the current segment.
                    if waveformType == 'absolute':
                        waveformValue = np.interp(waveformTime,
                                                  [lastTime, waveformOutTime],
                                                  [lastValue,waveformOutValue])
                    elif waveformType == 'relative':
                        waveformValue = np.interp(waveformTime,
                                                  [lastTime, waveformOutTime],
                                                  [lastValue,waveformOutValue])*startValueSegment
                        print('relative Linear detected')
                    else:
                        raise(NotImplementedError('waveformType proportional not implemented'))

                    segments_output.append(segmentName)
                    times_output.append(waveformTime)
                    relative_times_output.append(waveformTime - segmentTime)
                    values_output.append(waveformValue)
                    lastValue = waveformValue
                    lastTime = waveformTime
                    #LastPointIn is flagged false to ignore all subsequent points.
                    lastPointIn = False

        # Last point in the last segment. In case no point is defined at the end, a extra point is added
        # only for waveform completeness.
        if (j == (nb_segments-1) and not (lastTime == float(arrSegment[j][1]))):
            segmentName = arrSegment[j][0]
            waveformTime = float(arrSegment[j][1])
            waveformValue = lastValue
            segments_output.append(segmentName)
            times_output.append(waveformTime)
            if j == 0:
                #Case where the last segment is also the first one (only one segment)
                relative_times_output.append(waveformTime)
            else:
                relative_times_output.append(waveformTime - float(arrSegment[j-1][1]))
            values_output.append(waveformValue)

#    print(f'segmentTime={segmentTime}')
#    print(f'segments_output={segments_output}')
#    print(f'times_output={times_output}')
#    print(f'relative_times_output={relative_times_output}')
#    print(f'values_output={values_output}')

    return(segments_output, times_output, relative_times_output, values_output)




def waveformTypefinder(xmlroot, current_segment, sigTrajectoryName):
    """
    Determines the waveform type (absolute or relative to the start value of the segment).
    Returns a flag for the waveform type: absolute (1), relative (0) or proportional (2).
    The value is stored in a an int value for each segment and each component
    The int is a bitmask storing the type of a number of waveforms in the component:
    absolute (1), relative (0). Relative means actually proportional for PF coils.
    Which bit corresponds to which waveform is given in the comments of the DP.xml file.
    NOTE: the bit 0 in the DP.xml comments is the bit of least weight.
    NOTE: the proportional type (2) is correctly detected in the present function
    but not yet implemented in the waveform builder.
    """

    TypeBit_SignalNameList = ['rts:WEST_PCS/Actuators/Poloidal/ref_type.ref',\
    'rts:WEST_PCS/Actuators/Gas/ref_type.ref',\
    'rts:WEST_PCS/Actuators/Heating/ref_type.ref',\
    'rts:WEST_PCS/Actuators/Poloidal/env_type.ref',\
    'rts:WEST_PCS/Actuators/Gas/env_type.ref',\
    'rts:WEST_PCS/Actuators/Heating/env_type.ref']
    # The size of the bitmask cannot be guessed by the algorithm.
    # It is needed in order not assign values to extra zeroes
    # if the integer was capped to fixed number of bits.
    # Each of the bitmask sizes refers to the 6 signals referenced above.
    TypeBit_SizeBit = [16,24,10,16,28,10]


    TypeBit_SignalList = np.array([])
    # Iterate on the number of waveform type bitmasks.
    k=0
    for TypeBit_SignalName in TypeBit_SignalNameList:

        # Loop over all segments in the scenario to find the one requested by the user.
        for SEGMENT in xmlroot.findall("SEGMENTS/SEGMENT"):
            # Location of signal in segment
            # Enable following to check segment detail, which helps in error solving
            #       print(SEGMENT.attrib,SEGMENT.tag)
            segment_name = SEGMENT.attrib['Id']
            # As usual, renaming of the first segment.
            if segment_name=='0':
                segment_name='Init'
            else:
                segment_name='segment%s' %(segment_name)

            # If the segment is the one requested by the arguments, loop over the signal trajectories
            # to find the signal requested by the arguments (in Signal Treajectory). No point oing
            # all the time-consuming mapping of only a few waveforms are present in each segment.
            if (current_segment==segment_name):
                for SIGNAL_TRAJECTORIES in SEGMENT:
                    for SIGNAL_TRAJECTORY in SIGNAL_TRAJECTORIES:
                        # Assign the signal name explored by the loop to signalTrajectory
                        signalTrajectory = SIGNAL_TRAJECTORY.attrib['Name']

                        # matching searchSignal's waveform name (nnnn/env_tye.ref) with signalTrajectory's value
                        # When it is found, extract he bit mask
                        if (TypeBit_SignalName == signalTrajectory):
                            for REFERENCE in SIGNAL_TRAJECTORY:
                                # Theoretically, there is only one point for the whole segment, but the
                                # whole structure (point, value, etc.) is still used.
                                for POINT in REFERENCE:
                                    for VALUE in POINT:
                                        # Extract the decimal value of the bitmask
                                        value_decimal = VALUE.text

                                        # Format the string taking into account the size of the bitmask.
                                        # Example: 244 should be actually 00000244 if 8 bits are treated.
                                        format_str = '#0%ib'%(TypeBit_SizeBit[k]+2)

                                        # Convert to binary array
                                        value_binary = format(int(value_decimal),format_str)[2:]
                                        #print(value_binary)
                                        TypeBit_SignalList = np.append(TypeBit_SignalList,value_binary)
    k=k+1


    # Now the bitmask is known, search the relevant bit for the signal given as input.

    if (sigTrajectoryName=='rts:WEST_PCS/Plasma/Ip/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[0][0])
    elif (sigTrajectoryName=='rts:WEST_PCS/Plasma/dXLow/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[0][1])
    elif (sigTrajectoryName=='rts:WEST_PCS/Plasma/Z/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[0][2])
    elif (sigTrajectoryName=='rts:WEST_PCS/Plasma/rext/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[0][3])
    elif (sigTrajectoryName=='rts:WEST_PCS/Plasma/Zgeo/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[0][2])
    elif (sigTrajectoryName=='rts:WEST_PCS/Plasma/Rgeo/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[0][4])
    # Special "relative" Flag for poloidal coil currents: 2 because they are proportional to Ip
    # Arithmetic Trick so that the Absolute flag (1) stays the same but 0 becomes 2
    # NOTE: although correctly detected here, Proportional waveforms are not yet implemented in
    # the waveform builder.
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IXh/waveform.ref'):
        AbsRelBitValue = abs(int(TypeBit_SignalList[0][5])-2)
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IXb/waveform.ref'):
        AbsRelBitValue = abs(int(TypeBit_SignalList[0][6])-2)
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IBh/waveform.ref'):
        AbsRelBitValue = abs(int(TypeBit_SignalList[0][7])-2)
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IDh/waveform.ref'):
        AbsRelBitValue = abs(int(TypeBit_SignalList[0][8])-2)
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IEh/waveform.ref'):
        AbsRelBitValue = abs(int(TypeBit_SignalList[0][9])-2)
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IFh/waveform.ref'):
        AbsRelBitValue = abs(int(TypeBit_SignalList[0][10])-2)
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IFb/waveform.ref'):
        AbsRelBitValue = abs(int(TypeBit_SignalList[0][11])-2)
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IEb/waveform.ref'):
        AbsRelBitValue = abs(int(TypeBit_SignalList[0][12])-2)
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IDb/waveform.ref'):
        AbsRelBitValue = abs(int(TypeBit_SignalList[0][13])-2)
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IBb/waveform.ref'):
        AbsRelBitValue = abs(int(TypeBit_SignalList[0][14])-2)
    # Not for A coil: its relative mode is a real relative mode.
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IA/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[0][15])


    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Gas/REF3/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][0])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Gas/REF2/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][1])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Gas/REF1/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][2])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Gas/valve21/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][3])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Gas/valve20/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][4])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Gas/valve19/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][5])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Gas/valve18/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][6])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Gas/valve17/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][7])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Gas/valve16/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][8])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Gas/valve15/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][9])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Gas/valve14/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][10])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Gas/valve13/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][11])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Gas/valve12/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][12])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Gas/valve11/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][13])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Gas/valve10/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][14])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Gas/valve09/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][15])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Gas/valve08/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][16])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Gas/valve07/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][17])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Gas/valve06/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][18])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Gas/valve05/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][19])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Gas/valve04/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][20])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Gas/valve03/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][21])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Gas/valve02/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][22])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Gas/valve01/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][23])


    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Heating/ICRH/phase/3/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[2][0])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Heating/ICRH/power/3/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[2][1])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Heating/ICRH/phase/2/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[2][2])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Heating/ICRH/power/2/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[2][3])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Heating/ICRH/phase/1/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[2][4])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Heating/ICRH/power/1/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[2][5])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Heating/LHCD/phase/2/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[2][6])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Heating/LHCD/power/2/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[2][7])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Heating/LHCD/phase/1/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[2][8])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Heating/LHCD/power/1/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[2][9])

    elif (sigTrajectoryName=='rts:WEST_PCS/Plasma/Ip/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts:WEST_PCS/Plasma/Ip/max_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[3][0])
    elif (sigTrajectoryName=='rts:WEST_PCS/Plasma/dXLow/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts:WEST_PCS/Plasma/dXLow/max_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[0][1])
    elif (sigTrajectoryName=='rts:WEST_PCS/Plasma/Z/min_envwaveform.ref')\
    or (sigTrajectoryName=='rts:WEST_PCS/Plasma/Z/max_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[0][2])
    elif (sigTrajectoryName=='rts:WEST_PCS/Plasma/rext/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts:WEST_PCS/Plasma/rext/max_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[0][3])
    elif (sigTrajectoryName=='rts:WEST_PCS/Plasma/zgeo/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts:WEST_PCS/Plasma/zgeo/min_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[0][2])
    elif (sigTrajectoryName=='rts:WEST_PCS/Plasma/rgeo/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts:WEST_PCS/Plasma/rgeo/min_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[0][4])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IXh/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IXh/min_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[0][5])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IXb/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IXb/min_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[0][6])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IBh/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IBh/min_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[0][7])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IDh/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IDh/min_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[0][8])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IEh/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IEh/min_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[0][9])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IFh/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IFh/min_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[0][10])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IFb/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IFb/min_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[0][11])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IEb/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IEb/min_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[0][12])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IDb/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IDb/min_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[0][13])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IBb/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IBb/min_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[0][14])
    elif (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IA/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts:WEST_PCS/Actuators/Poloidal/IA/min_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[0][15])


    elif (sigTrajectoryName=='rts\WEST_PCS/Actuators/Gas/envelope4/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts\WEST_PCS/Actuators/Gas/envelope4/max_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][0])
    elif (sigTrajectoryName=='rts\WEST_PCS/Actuators/Gas/envelope3/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts\WEST_PCS/Actuators/Gas/envelope3/max_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][1])
    elif (sigTrajectoryName=='rts\WEST_PCS/Actuators/Gas/envelope2/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts\WEST_PCS/Actuators/Gas/envelope2/max_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][2])
    elif (sigTrajectoryName=='rts\WEST_PCS/Actuators/Gas/envelope1/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts\WEST_PCS/Actuators/Gas/envelope1/max_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][3])
    elif (sigTrajectoryName=='rts\WEST_PCS/Actuators/Gas/REF3/waveform.ref')\
    or (sigTrajectoryName=='rts\WEST_PCS/Actuators/Gas/REF3/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][4])
    elif (sigTrajectoryName=='rts\WEST_PCS/Actuators/Gas/REF2/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts\WEST_PCS/Actuators/Gas/REF2/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][5])
    elif (sigTrajectoryName=='rts\WEST_PCS/Actuators/Gas/REF1/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts\WEST_PCS/Actuators/Gas/REF1/waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[1][6])



    elif (sigTrajectoryName=='rts\WEST_PCS/Actuators/Heating/ICRH/phase/3/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts\WEST_PCS/Actuators/Heating/ICRH/phase/3/max_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[2][0])
    elif (sigTrajectoryName=='rts\WEST_PCS/Actuators/Heating/ICRH/power/3/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts\WEST_PCS/Actuators/Heating/ICRH/phase/3/max_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[2][1])
    elif (sigTrajectoryName=='rts\WEST_PCS/Actuators/Heating/ICRH/phase/2/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts\WEST_PCS/Actuators/Heating/ICRH/phase/3/max_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[2][2])
    elif (sigTrajectoryName=='rts\WEST_PCS/Actuators/Heating/ICRH/power/2/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts\WEST_PCS/Actuators/Heating/ICRH/phase/3/max_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[2][3])
    elif (sigTrajectoryName=='rts\WEST_PCS/Actuators/Heating/ICRH/phase/1/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts\WEST_PCS/Actuators/Heating/ICRH/phase/3/max_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[2][4])
    elif (sigTrajectoryName=='rts\WEST_PCS/Actuators/Heating/ICRH/power/1/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts\WEST_PCS/Actuators/Heating/ICRH/phase/3/max_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[2][5])
    elif (sigTrajectoryName=='rts\WEST_PCS/Actuators/Heating/LHCD/phase/2/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts\WEST_PCS/Actuators/Heating/ICRH/phase/3/max_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[2][6])
    elif (sigTrajectoryName=='rts\WEST_PCS/Actuators/Heating/LHCD/power/2/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts\WEST_PCS/Actuators/Heating/ICRH/phase/3/max_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[2][7])
    elif (sigTrajectoryName=='rts\WEST_PCS/Actuators/Heating/LHCD/phase/1/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts\WEST_PCS/Actuators/Heating/ICRH/phase/3/max_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[2][8])
    elif (sigTrajectoryName=='rts\WEST_PCS/Actuators/Heating/LHCD/power/1/min_env_waveform.ref')\
    or (sigTrajectoryName=='rts\WEST_PCS/Actuators/Heating/ICRH/phase/3/max_env_waveform.ref'):
        AbsRelBitValue = int(TypeBit_SignalList[2][9])

    else:
        AbsRelBitValue = 0

    if AbsRelBitValue == 0:
        return 'absolute'
    elif AbsRelBitValue == 1:
        return 'relative'
    elif AbsRelBitValue == 2:
        return 'proportional'
    else:
        raise(ValueError('Bad waveform type!'))

if __name__ == '__main__':
    """ Testing purpose """
    from DCS_settings import DCSSettings
    DP_file = '../../resources/pulse_setup_examples/52865/DP.xml'
    Sup_file = '../../resources/pulse_setup_examples/52865/Sup.xml'
    signal_list = ['rts:WEST_PCS/Plasma/Ip/waveform.ref',
                   'rts:WEST_PCS/Actuators/Poloidal/IEh/min_env_waveform.ref']

    DCS = DCSSettings(Sup_file)
    ns = DCS.nominal_scenario

    wf = waveformBuilder(DCS.nominal_scenario, signal_list, DP_file)

    sig_names = get_DCS_signal_names(DP_file)
    
    sc_wfs = waveformBuilder(DCS.nominal_scenario, sig_names, DP_file)
    
