# -*- coding: utf-8 -*-
"""
PPPAT - Post Pulse test

Isotopic Ratio
"""
import pywed as pw
import numpy as np
import matplotlib.pyplot as plt
from pppat.libpulse.check_result import CheckResult as Result
from pppat.libpulse.utils import is_online, wait_cursor, post_pulse_test
from pppat.libpulse.utils_west import smooth
import sys  # to test after if imas_west has been imported (sys.modules)

import logging
logger = logging.getLogger(__name__)

# this test is using IMAS database. Check if IMAS is available
try:
    import imas_west
except ModuleNotFoundError as e:
    logger.error('imas_west package cannot be imported!')

# Visible sectroscopy channels to use for the Halha/Dalpha
# Available channels are LODIVIN19, LODIVOU15 and INBUM04 
#CHANNEL_NAME = 'LODIVIN19'  # not available at start of C5
CHANNEL_NAME = 'LODIVOU15'
#CHANNEL_NAME = 'INBUM04'
# min and max values for the isotopic ratio. If lower or higher, trigger an ERROR
RATIO_MAX = 15 # in %
RATIO_MIN = 5  # in %


def imas_density_ratio(pulse_nb):
    """
    Retrive the isotopic ratio data for a given pulse nb

    Arguments
    ---------
    pulse_nb: integer
        WEST pulse number

    Return
    ---------
    density_ratio: array
        Isotopic density ratio. None if data unavailable.
    time: array or None
        Isotopic density ratio time array. None if data unavailable.

    """
    density_ratio, time = None, None

    # if IMAS library has been loaded (ie is available)
    try:   
        # getting spectrometer data take a (very) long time... few tens of seconds
        logger.info(f'Checking the isotopic ratio for pulse {pulse_nb}. Please wait...')
        specv = imas_west.get(pulse_nb, 'spectrometer_visible')

        # find the channel index corresponding to the channel to use for isotopic ratio measurement
        channel_idx = [channel_idx for (channel_idx, channel) in enumerate(specv.channel) if CHANNEL_NAME in channel.name]

        if channel_idx:
            # the specific channel exists, return the data
            logger.info(f'{CHANNEL_NAME} found in channel index: {channel_idx}')
            channel_idx = channel_idx[0]
            time = specv.channel[channel_idx].isotope_ratios.time - 32
            density_ratio = specv.channel[channel_idx].isotope_ratios.isotope[0].density_ratio
        else:
            logger.error(f'channel {CHANNEL_NAME} has not been found the spectrometer_visible data')
    except Exception as e:
        logger.error(f'Isotopic Ratio Error: {e}')

    # will return None, None if any problem occured
    return density_ratio, time


class check_isotopic_ratio(Result):
    """
    Check the isotopic ratio.

    Since the data are very heavy and very slow to obtain,
    this only a in-demande test
    """
    def __init__(self):
        Result.__init__(self)  # Result() constructor. Do not remove.

        self.name = 'Isotopic ratio'
        self.default = False          

    @post_pulse_test  # Do not remove
    def test(self, pulse_nb):
        """
        Plasma isotopica ratio Post-test
        """     
        density_ratio, time = imas_density_ratio(pulse_nb)

        if density_ratio is None:
            # a problem has occured when retrieving the data
            # or IMAS is not available
            self.code = self.UNAVAILABLE
            self.text = 'Visible Spectrometer data not available. Check log for more details'
        elif density_ratio.size == 0 or time.size == 0:
            # empty data
            self.code = self.UNAVAILABLE
            self.text = 'Empty data... Check with the diagnostic responsible'
        else:
            # filter the density ratop for time corresponding to Ip plateau
            #ip, t_ip = pw.tsbase(pulse_nb, 'SMAG_IP', nargout=2)
            idx_time = time > 0 #t_ip[ip > 300][0] # time > 0
            _time = time[idx_time]
            _density_ratio = density_ratio[idx_time]
            
            density_ratio_smoothed = smooth(_density_ratio, 21)
            density_ratio_std = np.std(density_ratio_smoothed)
            density_ratio_mean= np.mean(density_ratio_smoothed)

            self.text = f'Isotopic ratio is {density_ratio_mean*100:.2f}% +/- {density_ratio_std*100:.2f}%'
            logger.info(self.text)

            if density_ratio_mean*100 > RATIO_MAX or density_ratio_mean*100 < RATIO_MIN:
                self.code = self.ERROR
            else:
                self.code = self.OK

    @post_pulse_test  # Do not remove
    def plot(self, pulse_nb):
        """
        Post-test display
        """
        density_ratio, time = imas_density_ratio(pulse_nb)

        if density_ratio is None:
            logger.error('Visible Spectrometer data not available. Check log for more detail!')
        else:
            # filter the density ratop for time corresponding to Ip plateau
            #ip, t_ip = pw.tsbase(pulse_nb, 'SMAG_IP', nargout=2)
            idx_time = time > 0 #t_ip[ip > 300][0] # time > 0
            _time = time[idx_time]
            _density_ratio = density_ratio[idx_time]

            density_ratio_smoothed = smooth(_density_ratio, 21)
            density_ratio_std = np.std(density_ratio_smoothed)
            density_ratio_mean= np.mean(density_ratio_smoothed)
        
            fig, ax = plt.subplots()
            ax.plot(_time, _density_ratio*100)
            ax.plot(_time, density_ratio_smoothed*100)
            
            ax.grid(True)
            ax.set_xlabel('t [s]')
            ax.set_ylabel('Density Ratio [%]')
            ax.set_title(f'#{pulse_nb}')
            fig.show()

if __name__ == '__main__':
    pulse = 56241
    test = check_isotopic_ratio()
    print(test)
    #test.plot(pulse)

    density_ratio, time = imas_density_ratio(pulse)
    print(density_ratio)
    fig, ax = plt.subplots()
    ax.plot(time, density_ratio)