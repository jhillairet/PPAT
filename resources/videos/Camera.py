"""
This is a temporary script file.
"""
import numpy as np
from IRFMtb import tsdernier_choc
from pywed import *

path = './'

last_pulse = tsdernier_choc()

# Ask user for a shot number. Default value is the last shot number
try:
    pulse_str = input('\n Pulse number ? [{}]: '.format(last_pulse))
    if pulse_str:
        pulse = int(pulse_str)
    else:
        pulse = last_pulse
except ValueError as e:
    print('Pulse number not correct')

# Download both camera movies
TSRfile(pulse, 'FMPG401', path+'CCD'+str(pulse)+'_Q4Bm'+'.mp4')
TSRfile(pulse, 'FMPG402', path+'CCD'+str(pulse)+'_Q4Am'+'.mp4')

