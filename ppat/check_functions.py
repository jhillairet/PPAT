#! /Applications/Python-3.3.5/bin/python3.3
# /usr/bin/python

import os,sys
from xml.dom import minidom
import numpy as np
import re
import check_result
import waveform_pack
from waveformBuilder import *
import pywed as pw


def WOI_1p1(segmentTRajectory,infile,online_status):

    check_result_array = np.array([],dtype='object')
    check_result_array = np.append(check_result_array,check_result.check_result())

    check_result_array[0].check_fail_values_unit = 'Pa'
    check_result_array[0].check_name = 'A - Total residual pressure'

    if online_status:

        ttore = pw.tsmat(0,'EXP=T=S;General;TTORE')
        if (np.size(ttore)==3):

            TorusP = ttore[0]*10**(ttore[1])

            if (TorusP <1e-5):
                check_result_array[0].check_result_code = 3
                check_result_array[0].check_result_text = 'OK'
                check_result_array[0].check_fail_abs_times = np.array([])
                check_result_array[0].check_fail_values =  np.array([])
                check_result_array[0].check_fail_rel_times = np.array([])
                check_result_array[0].check_fail_segments = np.array([])


            elif (TorusP>=1e-5) and (TorusP<1e-4):
                check_result_array[0].check_result_code = 1
                check_result_array[0].check_result_text = 'Torus pressure above lower limit'
                check_result_array[0].check_fail_abs_times = np.array([])
                check_result_array[0].check_fail_values =  np.array([TorusP])
                check_result_array[0].check_fail_rel_times = np.array([])
                check_result_array[0].check_fail_segments = np.array([])
                check_result_array[0].check_fail_limit = 1e-5

            elif (TorusP>=1e-4):
                check_result_array[0].check_result_code = 0
                check_result_array[0].check_result_text = 'Torus pressure above upper limit'
                check_result_array[0].check_fail_abs_times = np.array([])
                check_result_array[0].check_fail_values =  np.array([TorusP])
                check_result_array[0].check_fail_rel_times = np.array([])
                check_result_array[0].check_fail_segments = np.array([])
                check_result_array[0].check_fail_limit = 1e-4
        else:
            check_result_array[0].check_result_code = 2
            check_result_array[0].check_result_text = 'Vacuum vessel Pressure'
            check_result_array[0].check_fail_abs_times = np.array([])
            check_result_array[0].check_fail_values =  np.array([])
            check_result_array[0].check_fail_rel_times = np.array([])
            check_result_array[0].check_fail_segments = np.array([])


    else:
        check_result_array[0].check_result_code = 2
        check_result_array[0].check_result_text = 'Vacuum vessel Pressure'
        check_result_array[0].check_fail_abs_times = np.array([])
        check_result_array[0].check_fail_values =  np.array([])
        check_result_array[0].check_fail_rel_times = np.array([])
        check_result_array[0].check_fail_segments = np.array([])

    return check_result_array


def WOI_2p2(segmentTrajectory,infile,online_status):

    check_result_array = np.array([],dtype='object')
    check_result_array = np.append(check_result_array,check_result.check_result())

    if online_status:
        PB30 = pw.tsmat(0,'EXP=T=S;General;PB30')
        signal_array = np.array([])
        signal_array = np.append(signal_array,'rts:WEST_PCS/Actuators/Heating/ICRH/power/1/waveform.ref')
        signal_array = np.append(signal_array,'rts:WEST_PCS/Actuators/Heating/ICRH/power/2/waveform.ref')
        signal_array = np.append(signal_array,'rts:WEST_PCS/Actuators/Heating/ICRH/power/3/waveform.ref')

        #To be finished later

def WOI_3p2(segmentTRajectory,infile,online_status):
    #Toroidal field coil current
    check_result_array = np.array([],dtype='object')
    check_result_array = np.append(check_result_array,check_result.check_result())

    check_result_array[0].check_fail_values_unit = 'A'
    check_result_array[0].check_name = 'A - Maximal toroidal field in standard operation mode'

    if online_status:
        ITOR = pw.tsmat(0,'EXP=T=S;General;Itor')
        if (np.size(ITOR)==1):

            if (ITOR<=1250):
                check_result_array[0].check_result_code = 3
                check_result_array[0].check_result_text = 'OK'
                check_result_array[0].check_fail_abs_times = np.array([])
                check_result_array[0].check_fail_values =  np.array([])
                check_result_array[0].check_fail_rel_times = np.array([])
                check_result_array[0].check_fail_segments = np.array([])
                check_result_array[0].check_fail_limit = 1250

            elif (ITOR>1250) and (ITOR<=1350):
                check_result_array[0].check_result_code = 1
                check_result_array[0].check_result_text = 'Standard Toroidal Field coil current limit exceeded. \
                Special approval required. Please check WOI'
                check_result_array[0].check_fail_abs_times = np.array([])
                check_result_array[0].check_fail_values = np.array([ITOR])
                check_result_array[0].check_fail_rel_times = np.array([])
                check_result_array[0].check_fail_segments = np.array([])
                check_result_array[0].check_fail_limit = 1250
            elif (ITOR>1350):
                check_result_array[0].check_result_code = 1
                check_result_array[0].check_result_text = 'Toroidal Field coil current limit exceeded.'
                check_result_array[0].check_fail_abs_times = np.array([])
                check_result_array[0].check_fail_values = np.array([ITOR])
                check_result_array[0].check_fail_rel_times = np.array([])
                check_result_array[0].check_fail_segments = np.array([])
                check_result_array[0].check_fail_limit = 1350
        else:
            check_result_array[0].check_result_code = 2
            check_result_array[0].check_result_text = 'Toroidal field coil current'
            check_result_array[0].check_fail_abs_times = np.array([])
            check_result_array[0].check_fail_values =  np.array([])
            check_result_array[0].check_fail_rel_times = np.array([])
            check_result_array[0].check_fail_segments = np.array([])

    else:
        check_result_array[0].check_result_code = 2
        check_result_array[0].check_result_text = 'Toroidal field coil current'
        check_result_array[0].check_fail_abs_times = np.array([])
        check_result_array[0].check_fail_values =  np.array([])
        check_result_array[0].check_fail_rel_times = np.array([])
        check_result_array[0].check_fail_segments = np.array([])

    return check_result_array



def WOI_3p7(segmentTrajectory,infile,online_status):


    check_result_array = np.array([],dtype='object')
    check_result_array = np.append(check_result_array,check_result.check_result())

    #Max Ip test

    Ip_limit = 1e6

    signal_array = np.array([])
    signal_array = np.append(signal_array,'rts:WEST_PCS/Plasma/Ip/waveform.ref')
    wform = waveformBuilder(segmentTrajectory,signal_array,infile)
    t_Ip = wform[0].times
    t_Ip_rel = wform[0].reltimes
    Ip = wform[0].values
    segments = wform[0].segments


    fail_indexes = np.where(Ip>Ip_limit)

    fail_times = t_Ip[fail_indexes]
    fail_reltimes = t_Ip_rel[fail_indexes]
    fail_values = Ip[fail_indexes]
    fail_segments = segments[fail_indexes]


    check_result_array[0].check_fail_values_unit = 'A'
    check_result_array[0].check_fail_limit = Ip_limit
    check_result_array[0].check_name = 'A - Plasma Current'

    if fail_indexes[0].size==0:
        check_result_array[0].check_result_code = 3
        check_result_array[0].check_result_text = 'OK'
        check_result_array[0].check_fail_abs_times = np.array([])
        check_result_array[0].check_fail_values =  np.array([])
        check_result_array[0].check_fail_rel_times = np.array([])
        check_result_array[0].check_fail_segments = np.array([])


    else:
        check_result_array[0].check_result_code = 0
        check_result_array[0].check_result_text = 'Maximum plasma current exceeded'
        check_result_array[0].check_fail_abs_times = fail_times
        check_result_array[0].check_fail_values = fail_values
        check_result_array[0].check_fail_rel_times = fail_reltimes
        check_result_array[0].check_fail_segments = fail_segments


    return check_result_array

def WOI_4p1(segmentTrajectory,infile,online_status):

    check_result_array = np.array([],dtype='object')
    check_result_array = np.append(check_result_array,check_result.check_result())

    #Min density test

    density_lower_limit = 1e18

    signal_array = np.array([])
    signal_array = np.append(signal_array,'rts:WEST_PCS/Actuators/Gas/REF1/waveform.ref')
    wform = waveformBuilder(segmentTrajectory,signal_array,infile)
    t_density = wform[0].times
    t_density_rel = wform[0].reltimes
    density = (wform[0].values)*1e18
    segments = wform[0].segments


    fail_indexes = np.where(density<density_lower_limit)

    fail_times = t_density[fail_indexes]
    fail_reltimes = t_density_rel[fail_indexes]
    fail_values = density[fail_indexes]
    fail_segments = segments[fail_indexes]


    check_result_array[0].check_fail_values_unit = 'm^-2'
    check_result_array[0].check_fail_limit = density_lower_limit
    check_result_array[0].check_name = 'B - Plasma density range'

    if fail_indexes[0].size==0:
        check_result_array[0].check_result_code = 3
        check_result_array[0].check_result_text = 'OK'
        check_result_array[0].check_fail_abs_times = np.array([])
        check_result_array[0].check_fail_values =  np.array([])
        check_result_array[0].check_fail_rel_times = np.array([])
        check_result_array[0].check_fail_segments = np.array([])


    else:
        check_result_array[0].check_result_code = 1
        check_result_array[0].check_result_text = 'Density too low (risk of runaway electrons)'
        check_result_array[0].check_fail_abs_times = fail_times
        check_result_array[0].check_fail_values = fail_values
        check_result_array[0].check_fail_rel_times = fail_reltimes
        check_result_array[0].check_fail_segments = fail_segments


    return check_result_array


def WOI_5p1(segmentTrajectory,infile,online_status):

    check_result_array = np.array([],dtype='object')
    check_result_array = np.append(check_result_array,check_result.check_result())
    check_result_array = np.append(check_result_array,check_result.check_result())
    check_result_array = np.append(check_result_array,check_result.check_result())

    phase_limit=180

    signal_array = np.array([])
    signal_array = np.append(signal_array,'rts:WEST_PCS/Actuators/Heating/ICRH/phase/1/waveform.ref')
    signal_array = np.append(signal_array,'rts:WEST_PCS/Actuators/Heating/ICRH/phase/2/waveform.ref')
    signal_array = np.append(signal_array,'rts:WEST_PCS/Actuators/Heating/ICRH/phase/3/waveform.ref')
    signal_array = np.append(signal_array,'rts:WEST_PCS/Actuators/Heating/ICRH/power/1/waveform.ref')
    signal_array = np.append(signal_array,'rts:WEST_PCS/Actuators/Heating/ICRH/power/2/waveform.ref')
    signal_array = np.append(signal_array,'rts:WEST_PCS/Actuators/Heating/ICRH/power/3/waveform.ref')



    wform = waveformBuilder(segmentTrajectory,signal_array,infile)


    for k in range(0,3):

        t_phase= wform[k].times
        t_phase_rel = wform[k].reltimes
        phase = wform[k].values
        segments = wform[k].segments


        maxpower = max(wform[k+3].values)

        check_result_array[k].check_fail_values_unit = 'deg'
        check_result_array[k].check_fail_limit = phase_limit
        check_result_array[k].check_name = 'ICRH Antenna %d - phase'%(k+1)


        fail_indexes = np.where((phase<170) | (phase>190))

        fail_times = t_phase[fail_indexes]
        fail_reltimes = t_phase_rel[fail_indexes]
        fail_values = phase[fail_indexes]
        fail_segments = segments[fail_indexes]


        if (fail_indexes[0].size==0) or (maxpower==0):
            check_result_array[k].check_result_code = 3
            check_result_array[k].check_result_text = 'OK'
            check_result_array[k].check_fail_abs_times = np.array([])
            check_result_array[k].check_fail_values =  np.array([])
            check_result_array[k].check_fail_rel_times = np.array([])
            check_result_array[k].check_fail_segments = np.array([])


        else:
            check_result_array[k].check_result_code = 0
            check_result_array[k].check_result_text = 'Wrong phasing'
            check_result_array[k].check_fail_abs_times = fail_times
            check_result_array[k].check_fail_values = fail_values
            check_result_array[k].check_fail_rel_times = fail_reltimes
            check_result_array[k].check_fail_segments = fail_segments


    return check_result_array


def WOI_5p2(segmentTrajectory,infile,online_status):

    check_result_array = np.array([],dtype='object')
    check_result_array = np.append(check_result_array,check_result.check_result())
    check_result_array = np.append(check_result_array,check_result.check_result())
    check_result_array = np.append(check_result_array,check_result.check_result())

    signal_array = np.array([])
    signal_array = np.append(signal_array,'rts:WEST_PCS/Actuators/Heating/ICRH/power/1/waveform.ref')
    signal_array = np.append(signal_array,'rts:WEST_PCS/Actuators/Heating/ICRH/power/2/waveform.ref')
    signal_array = np.append(signal_array,'rts:WEST_PCS/Actuators/Heating/ICRH/power/3/waveform.ref')

    wform = waveformBuilder(segmentTrajectory,signal_array,infile)


    for k in range(0,3):

        check_result_array[k].check_fail_values_unit = 'W'
        check_result_array[k].check_name = 'ICRH Antenna %d - power'%(k+1)

        t_ICRHpower= wform[k].times
        t_ICRHpower_rel = wform[k].reltimes
        ICRHpower = wform[k].values
        segments = wform[k].segments
        # Computes ICRH maximum duration of power on. Takes the points immediately before and after the first
        # and the last point where a non-zero power is set. This gives the maximum envelope of the ICRH duration.

        ICRHpower_on_indexes = np.where(ICRHpower>0)
        if (ICRHpower_on_indexes[0].size > 0):
            ICRHduration = t_ICRH_power[min(ICRHpower_on_indexes[-1]+1,t_ICRHpower.size)]-t_ICRHpower[max(0,ICRHpower_on_indexes[0]-1)]

            if (ICRHduration<30):
                check_result_array[k].check_fail_limit = 3e6
            if (ICRHduration>30) and (ICRHduration<60):
                check_result_array[k].check_fail_limit = 2e6
            if (ICRHduration>60):
                check_result_array[k].check_fail_limit = 1e6

            fail_indexes = np.where(ICRHpower>check_result_array[k].check_fail_limit)
            fail_times = t_ICRHpower[fail_indexes]
            fail_reltimes = t_ICRHpower_rel[fail_indexes]
            fail_values = ICRHpower[fail_indexes]
            fail_segments = segments[fail_indexes]

            if (fail_indexes[0].size==0):
                check_result_array[k].check_result_code = 3
                check_result_array[k].check_result_text = 'OK'
                check_result_array[k].check_fail_abs_times = np.array([])
                check_result_array[k].check_fail_values =  np.array([])
                check_result_array[k].check_fail_rel_times = np.array([])
                check_result_array[k].check_fail_segments = np.array([])


            else:
                check_result_array[k].check_result_code = 0
                check_result_array[k].check_result_text = 'Too high ICRH power on antenna'%(k+1)
                check_result_array[k].check_fail_abs_times = fail_times
                check_result_array[k].check_fail_values = fail_values
                check_result_array[k].check_fail_rel_times = fail_reltimes
                check_result_array[k].check_fail_segments = fail_segments
        else:
            #In case no ICRH power (no time points with PICRH>0), the check is passed.

            check_result_array[k].check_result_code = 3
            check_result_array[k].check_result_text = 'OK'
            check_result_array[k].check_fail_abs_times = np.array([])
            check_result_array[k].check_fail_values =  np.array([])
            check_result_array[k].check_fail_rel_times = np.array([])
            check_result_array[k].check_fail_segments = np.array([])


    return check_result_array


def WOI_5p4(segmentTrajectory,infile,online_status):

    check_result_array = np.array([],dtype='object')
    check_result_array = np.append(check_result_array,check_result.check_result())
    check_result_array = np.append(check_result_array,check_result.check_result())
    check_result_array = np.append(check_result_array,check_result.check_result())
    check_result_array = np.append(check_result_array,check_result.check_result())

    signal_array = np.array([])
    signal_array = np.append(signal_array,'rts:WEST_PCS/Actuators/Heating/LHCD/phase/1/waveform.ref')
    signal_array = np.append(signal_array,'rts:WEST_PCS/Actuators/Heating/LHCD/phase/2/waveform.ref')
    signal_array = np.append(signal_array,'rts:WEST_PCS/Actuators/Heating/LHCD/power/1/waveform.ref')
    signal_array = np.append(signal_array,'rts:WEST_PCS/Actuators/Heating/LHCD/power/2/waveform.ref')
    signal_array = np.append(signal_array,'rts:WEST_PCS/Actuators/Gas/REF1/waveform.ref')


    wform = waveformBuilder(segmentTrajectory,signal_array,infile)

    t_density= wform[4].times
    t_density_rel = wform[4].reltimes
    density = wform[4].values
    segments = wform[4].segments

    phase_upper_limit = np.array([0,-90])
    phase_lower_limit = np.array([-180,-180])


    for k in range(0,2):

        maxpower = max(wform[k+2].values)
        check_result_array[k].check_fail_values_unit = 'deg'
        check_result_array[k].check_name = 'LH coupler %d - minimum phase'%(k+1)
        check_result_array[k].check_fail_limit = phase_lower_limit[k]

        t_LHphase= wform[k].times
        t_LHphase_rel = wform[k].reltimes
        LHphase = wform[k].values
        segments = wform[k].segments


        fail_indexes = np.where(LHphase<phase_lower_limit[k])

        fail_times = t_LHphase[fail_indexes]
        fail_reltimes = t_LHphase_rel[fail_indexes]
        fail_values = LHphase[fail_indexes]
        fail_segments = segments[fail_indexes]

        if (fail_indexes[0].size==0) or (maxpower==0):
            check_result_array[k].check_result_code = 3
            check_result_array[k].check_result_text = 'OK'
            check_result_array[k].check_fail_abs_times = np.array([])
            check_result_array[k].check_fail_values =  np.array([])
            check_result_array[k].check_fail_rel_times = np.array([])
            check_result_array[k].check_fail_segments = np.array([])


        else:
            check_result_array[k].check_result_code = 0
            check_result_array[k].check_result_text = 'Phase too low'
            check_result_array[k].check_fail_abs_times = fail_times
            check_result_array[k].check_fail_values = fail_values
            check_result_array[k].check_fail_rel_times = fail_reltimes
            check_result_array[k].check_fail_segments = fail_segments

    for k in range(2,4):

        maxpower = max(wform[k].values)
        check_result_array[k].check_fail_values_unit = 'deg'
        check_result_array[k].check_name = 'LH coupler %d - maximum phase'%(k-1)
        check_result_array[k].check_fail_limit = phase_upper_limit[k-2]

        t_LHphase= wform[k-2].times
        t_LHphase_rel = wform[k-2].reltimes
        LHphase = wform[k-2].values
        segments = wform[k-2].segments


        fail_indexes = np.where(LHphase>phase_upper_limit[k-2])

        fail_times = t_LHphase[fail_indexes]
        fail_reltimes = t_LHphase_rel[fail_indexes]
        fail_values = LHphase[fail_indexes]
        fail_segments = segments[fail_indexes]

        if (fail_indexes[0].size==0) or (maxpower==0):
            check_result_array[k].check_result_code = 3
            check_result_array[k].check_result_text = 'OK'
            check_result_array[k].check_fail_abs_times = np.array([])
            check_result_array[k].check_fail_values =  np.array([])
            check_result_array[k].check_fail_rel_times = np.array([])
            check_result_array[k].check_fail_segments = np.array([])


        else:
            check_result_array[k].check_result_code = 0
            check_result_array[k].check_result_text = 'Phase too high'
            check_result_array[k].check_fail_abs_times = fail_times
            check_result_array[k].check_fail_values = fail_values
            check_result_array[k].check_fail_rel_times = fail_reltimes
            check_result_array[k].check_fail_segments = fail_segments


    return check_result_array



def WOI_6p1(segmentTrajectory,infile,online_status):

    check_result_array = np.array([],dtype='object')
    check_result_array = np.append(check_result_array,check_result.check_result())
    signal_array = np.array([])
    signal_array = np.append(signal_array,'rts:WEST_PCS/Actuators/Poloidal/IXb/waveform.ref')

    wform = waveformBuilder(segmentTrajectory,signal_array,infile)

    t_IXb= wform[0].times
    t_IXb_rel = wform[0].reltimes
    IXb = wform[0].values
    segments = wform[0].segments


    FirstNonZero_indexes = np.where(IXb>0)[0]


    if len(FirstNonZero_indexes)>0:
        FirstNonZero_index = FirstNonZero_indexes[0]
        LastZero_index = FirstNonZero_index - 1
        TimeXpointStart = np.interp(0.0,IXb[LastZero_index:FirstNonZero_index],t_IXb[LastZero_index:FirstNonZero_index])
        LastNonZero_indexes = np.where(IXb>0)[0]
        LastNonZero_index = LastNonZero_indexes[-1]
        FinalZero_index = LastNonZero_index + 1
        TimeXpointStop = np.interp(0.0,IXb[LastNonZero_index:FinalZero_index],t_IXb[LastNonZero_index:FinalZero_index])
        DurationXpoint = TimeXpointStop - TimeXpointStart

    else:
        DurationXpoint = 0.0

    MaximumDurationXpoint = 10.0

    check_result_array[0].check_fail_values_unit = 's'
    check_result_array[0].check_name = 'Plasma duration in lower X-point configuration'
    check_result_array[0].check_fail_limit = MaximumDurationXpoint

    if (DurationXpoint<=10.0):
        check_result_array[0].check_result_code = 3
        check_result_array[0].check_result_text = 'OK'
        check_result_array[0].check_fail_abs_times = np.array([])
        check_result_array[0].check_fail_values =  np.array([])
        check_result_array[0].check_fail_rel_times = np.array([])
        check_result_array[0].check_fail_segments = np.array([])
    else:
        check_result_array[0].check_result_code = 0
        check_result_array[0].check_result_text = 'Lower X-point phase too long: Lower divertor coils ON during'
        check_result_array[0].check_fail_abs_times = np.array([])
        check_result_array[0].check_fail_values = np.array([DurationXpoint])
        check_result_array[0].check_fail_rel_times = np.array([])
        check_result_array[0].check_fail_segments = np.array([])

    return check_result_array


def WOI_6p2(segmentTrajectory,infile,online_status):

    check_result_array = np.array([],dtype='object')
    check_result_array = np.append(check_result_array,check_result.check_result())
    signal_array = np.array([])
    signal_array = np.append(signal_array,'rts:WEST_PCS/Actuators/Poloidal/IXh/waveform.ref')

    wform = waveformBuilder(segmentTrajectory,signal_array,infile)

    t_IXh= wform[0].times
    t_IXh_rel = wform[0].reltimes
    IXh = wform[0].values
    segments = wform[0].segments



    FirstNonZero_indexes = np.where(IXh>0)[0]


    if len(FirstNonZero_indexes)>0:
        FirstNonZero_index = FirstNonZero_indexes[0]
        LastZero_index = FirstNonZero_index - 1
        TimeXpointStart = np.interp(0.0,IXh[LastZero_index:FirstNonZero_index],t_IXh[LastZero_index:FirstNonZero_index])
        LastNonZero_indexes = np.where(IXh>0)[0]
        LastNonZero_index = LastNonZero_indexes[-1]
        FinalZero_index = LastNonZero_index + 1
        TimeXpointStop = np.interp(0.0,IXh[LastNonZero_index:FinalZero_index],t_IXh[LastNonZero_index:FinalZero_index])
        DurationXpoint = TimeXpointStop - TimeXpointStart

    else:
        DurationXpoint = 0.0

    MaximumDurationXpoint = 10.0

    check_result_array[0].check_fail_values_unit = 's'
    check_result_array[0].check_name = 'Plasma duration in upper X-point configuration'
    check_result_array[0].check_fail_limit = MaximumDurationXpoint

    if (DurationXpoint<=10.0):
        check_result_array[0].check_result_code = 3
        check_result_array[0].check_result_text = 'OK'
        check_result_array[0].check_fail_abs_times = np.array([])
        check_result_array[0].check_fail_values =  np.array([])
        check_result_array[0].check_fail_rel_times = np.array([])
        check_result_array[0].check_fail_segments = np.array([])
    else:
        check_result_array[0].check_result_code = 0
        check_result_array[0].check_result_text = 'Upper X-point phase too long: Upper divertor coils ON during'
        check_result_array[0].check_fail_abs_times = np.array([])
        check_result_array[0].check_fail_values = np.array([DurationXpoint])
        check_result_array[0].check_fail_rel_times = np.array([])
        check_result_array[0].check_fail_segments = np.array([])

    return check_result_array



def WOI_6p3(segmentTrajectory,infile,online_status):

    check_result_array = np.array([],dtype='object')
    check_result_array = np.append(check_result_array,check_result.check_result())
    signal_array = np.array([])
    signal_array = np.append(signal_array,'rts:WEST_PCS/Plasma/Ip/waveform.ref')

    wform = waveformBuilder(segmentTrajectory,signal_array,infile)

    t_Ip= wform[0].times
    t_Ip_rel = wform[0].reltimes
    Ip = wform[0].values
    segments = wform[0].segments

    FirstNonZero_indexes = np.where(Ip>0)[0]


    if len(FirstNonZero_indexes)>0:
        FirstNonZero_index = FirstNonZero_indexes[0]
        LastZero_index = FirstNonZero_index - 1
        time_FirstNonZero = t_Ip[FirstNonZero_index]
        time_LastZero = t_Ip[LastZero_index]
        TimeXpointStart = np.interp(0.0,Ip[LastZero_index:FirstNonZero_index],t_Ip[LastZero_index:FirstNonZero_index])
        LastNonZero_indexes = np.where(Ip>0)[0]
        LastNonZero_index = LastNonZero_indexes[-1]
        FinalZero_index = LastNonZero_index + 1
        TimeXpointStop = np.interp(0.0,Ip[LastNonZero_index:FinalZero_index],t_Ip[LastNonZero_index:FinalZero_index])
        DurationXpoint = TimeXpointStop - TimeXpointStart

    else:
        DurationXpoint = 0.0

    MaximumDurationXpoint = 10.0

    check_result_array[0].check_fail_values_unit = 's'
    check_result_array[0].check_name = 'Plasma duration'
    check_result_array[0].check_fail_limit = MaximumDurationXpoint

    if (DurationXpoint<=10.0):
        check_result_array[0].check_result_code = 3
        check_result_array[0].check_result_text = 'OK'
        check_result_array[0].check_fail_abs_times = np.array([])
        check_result_array[0].check_fail_values =  np.array([])
        check_result_array[0].check_fail_rel_times = np.array([])
        check_result_array[0].check_fail_segments = np.array([])
    else:
        check_result_array[0].check_result_code = 0
        check_result_array[0].check_result_text = 'Pulse too long: Plasma Current > 0 during'
        check_result_array[0].check_fail_abs_times = np.array([])
        check_result_array[0].check_fail_values = np.array([DurationXpoint])
        check_result_array[0].check_fail_rel_times = np.array([])
        check_result_array[0].check_fail_segments = np.array([])

    return check_result_array



def protection_bidon(segmentTrajectory,infile):



    check_result_ip = check_result.check_result()

    check_result_ip.check_fail_values_unit = ''
    check_result_ip.check_result_code = 2
    check_result_ip.check_result_text = 'OK'
    check_result_ip.check_fail_abs_times = np.array([])
    check_result_ip.check_fail_values = np.array([])
    check_result_ip.check_fail_limit = 42

    return check_result_ip


def config_bidon(segmentTrajectory,infile):

    ip_limit = 1.5e6
    ip = 2.0

    fail_times = np.array([-5])
    fail_values = np.array([])

    check_result_ip = check_result.check_result()

    #Solve this tuple problem: why does where returns a tuple instead of a simple array ?
    check_result_ip.fail_values_unit = ''

    if ip>ip_limit:
        check_result_ip.check_result_code = 2
        check_result_ip.check_result_text = 'OK'
        check_result_ip.check_fail_abs_times = np.array([])
        check_result_ip.check_fail_values = np.array([])

    else:
        check_result_ip.check_result_code = 0
        check_result_ip.check_result_text = 'Machine config wrong'
        check_result_ip.check_fail_abs_times = fail_times
        check_result_ip.check_fail_values = fail_values
        check_result_ip.check_fail_limit = 42

    return check_result_ip
