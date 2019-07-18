from xml.dom import minidom
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
from matplotlib import gridspec

from pppat.libpulse.waveform import get_waveform

# default color style : black style but using the default line color cycle
default_colors_cycle = matplotlib.rcParams['axes.prop_cycle']  # default values
plt.style.use('dark_background')
matplotlib.rcParams['axes.prop_cycle'] = default_colors_cycle  # put back default values

def BigPicture_disp(segmentTrajectory, dpFile, waveforms, pulse_nb=None):
    # Figure window size parameters. Note that NX adjusts the vertical size if too tall.
    fig_Xposition = 0
    fig_Yposition = 0
    fig_width = 1200
    fig_height = 1000

    # Build the signal list together with the plot number they are supposed to be displayed in.
    # First stored in a linear list for memory management efficiency

    signal_list = []
    signal_list.append(['rts:WEST_PCS/Plasma/Ip/waveform.ref', '1', 'Ip'])
    # plasma positions
    signal_list.append(['rts:WEST_PCS/Plasma/Rgeo/waveform.ref', '2', 'Rgeo'])
    signal_list.append(['rts:WEST_PCS/Plasma/Zgeo/waveform.ref', '2', 'Zgeo'])
    signal_list.append(['rts:WEST_PCS/Plasma/Rext/waveform.ref', '2', 'Rext'])
    signal_list.append(['rts:WEST_PCS/Plasma/dXLow/waveform.ref', '2', 'dXLow'])
    # Poloidal and divertor currents
    signal_list.append(['rts:WEST_PCS/Actuators/Poloidal/IA/waveform.ref', '3', 'IA'])
    signal_list.append(['rts:WEST_PCS/Actuators/Poloidal/IBh/waveform.ref', '3', 'IBh'])
    signal_list.append(['rts:WEST_PCS/Actuators/Poloidal/IDh/waveform.ref', '3', 'IDh'])
    signal_list.append(['rts:WEST_PCS/Actuators/Poloidal/IEh/waveform.ref', '3', 'IEh'])
    signal_list.append(['rts:WEST_PCS/Actuators/Poloidal/IFh/waveform.ref', '3', 'IFh'])
    signal_list.append(['rts:WEST_PCS/Actuators/Poloidal/IBb/waveform.ref', '3', 'IBb'])
    signal_list.append(['rts:WEST_PCS/Actuators/Poloidal/IDb/waveform.ref', '3', 'IDb'])
    signal_list.append(['rts:WEST_PCS/Actuators/Poloidal/IEb/waveform.ref', '3', 'IEb'])
    signal_list.append(['rts:WEST_PCS/Actuators/Poloidal/IFb/waveform.ref', '3', 'IFb'])
    signal_list.append(['rts:WEST_PCS/Actuators/Poloidal/IXh/waveform.ref', '4', 'IXh'])
    signal_list.append(['rts:WEST_PCS/Actuators/Poloidal/IXb/waveform.ref', '4', 'IXb'])
    # Density and gaz injection
    signal_list.append(['rts:WEST_PCS/Actuators/Gas/REF1/waveform.ref', '5', 'ne'])
    for ind in range(1, 22):  # les 21 vannes de gaz
        signal_list.append([f'rts:WEST_PCS/Actuators/Gas/valve{ind:02d}/waveform.ref', 
                            '6', f'valve {ind}'])
    # External heating system
    signal_list.append(['rts:WEST_PCS/Actuators/Heating/LHCD/power/1/waveform.ref', '7', 'P_LH1'])
    signal_list.append(['rts:WEST_PCS/Actuators/Heating/LHCD/power/2/waveform.ref', '7', 'P_LH2'])
    signal_list.append(['rts:WEST_PCS/Actuators/Heating/ICRH/power/1/waveform.ref', '7', 'P_ICRH_Q1'])
    signal_list.append(['rts:WEST_PCS/Actuators/Heating/ICRH/power/2/waveform.ref', '7', 'P_ICRH_Q2'])
    signal_list.append(['rts:WEST_PCS/Actuators/Heating/ICRH/power/3/waveform.ref', '7', 'P_ICRH_Q4'])

    signal_list.append(['rts:WEST_PCS/Actuators/Heating/LHCD/phase/1/waveform.ref', '8', 'Phi_LH1'])
    signal_list.append(['rts:WEST_PCS/Actuators/Heating/LHCD/phase/2/waveform.ref', '8', 'Phi_LH2'])
    signal_list.append(['rts:WEST_PCS/Actuators/Heating/ICRH/phase/1/waveform.ref', '8', 'Phi_ICRH_Q1'])
    signal_list.append(['rts:WEST_PCS/Actuators/Heating/ICRH/phase/2/waveform.ref', '8', 'Phi_ICRH_Q2'])
    signal_list.append(['rts:WEST_PCS/Actuators/Heating/ICRH/phase/3/waveform.ref', '8', 'Phi_ICRH_Q4'])

    # Reshaping of the signal list into an array for compatibility with legacy code
    # signal_array[:,1] = DCS signal name
    # signal_array[:,2] = subplot to be plotted in.
    # signal_array[:,3] = name of the waveform, to be displayed in legend
    signal_array = np.array(signal_list)#.reshape((signal_number,3))

    #Build the waveforms from the segment trajectory, the signal names and the name of the DP.xml file
    # get only the waveforms indicated above in the signal_list
    wform = []
    for i, sig in enumerate(signal_array):
        #print(f'i={i}: sig={sig}')
        wform.append(get_waveform(sig[0], waveforms))

    #wform = waveformBuilder(segmentTrajectory,signal_array[:,0],dpFile)

    # Array containing axes y-labels.
    # Should be the same size as the number of subplots times 2 (2 axes per subplot)
    ylabels = {'0': '',  # No label on patch subplot
              '1': '[kA]', '2': '[m]', '3': '[A]', '4': '[A]',
              '5': '[$m^{-2}$]', '6': '[$Pa.m^3.s^{-1}$]', '7': '[MW]', '8':'[deg]'}

    # Figure initialization
    fig = plt.figure()
    fig.canvas.set_window_title(f"The Big Picture - WEST pulse #{pulse_nb}")

    # Axes creation. 2 y axes per suplot using twinx.
    axarr = np.array([])
    gs = gridspec.GridSpec(5, 1, height_ratios=[1,6,6,6,6], hspace=0.05)
    axarr = np.append(axarr, plt.subplot(gs[0]))
    axarr = np.append(axarr, plt.subplot(gs[1]))
    axarr = np.append(axarr, axarr[-1].twinx())
    axarr = np.append(axarr, plt.subplot(gs[2]))
    axarr = np.append(axarr, axarr[-1].twinx())
    axarr = np.append(axarr, plt.subplot(gs[3]))
    axarr = np.append(axarr, axarr[-1].twinx())
    axarr = np.append(axarr, plt.subplot(gs[4]))
    axarr = np.append(axarr, axarr[-1].twinx())

    # Link the x axes to be able to zoom all suplots simultaneously
    axarr[0].get_shared_x_axes().join(axarr[0], axarr[1], axarr[3], axarr[5], axarr[7])

    # convert the segment scenario into a numpy array for compatibility with the code below
    segmentTrajectory = np.array(segmentTrajectory)

    # Prepare each subplot.
    # Could have been done with a loop, but some subplots display all-zero waveforms (heating).
    # Others do not, for compacity purposes (21 gas valves)
    # Even axis numbers: left-hand y axes
    # Odd axis numbers: right-hand y axes

    # Segments overview (patch plot)
    axarr[0].plot([0], [0], 
                  'x-', label=signal_array[i,2], linewidth=3, markersize=10)

    segments_patches = []
    for ii in (np.arange(len(segmentTrajectory))):

        segment_duration = float(segmentTrajectory[ii,2])
        segment_start_time = float(segmentTrajectory[ii,1]) - segment_duration
        rect = mpatches.Rectangle([segment_start_time,0.0], segment_duration,
                                   1.0, ec='none')
        segments_patches.append(rect)

    colors = np.linspace(0, 1, len(segments_patches))
    p_collec = PatchCollection(segments_patches, cmap=plt.cm.Dark2)
    p_collec.set_array(np.array(colors))

    axarr[0].add_collection(p_collec)
    axarr[0].set_ylim([0,1])

    for ii in (np.arange(len(segmentTrajectory))):
        segment_duration = float(segmentTrajectory[ii,2])
        segment_start_time = float(segmentTrajectory[ii,1]) - segment_duration
        if (segmentTrajectory[ii,0] == 'Init'):
            text_segment = 'Init'
        else:
            text_segment = segmentTrajectory[ii,0][7:]

        axarr[0].text(segment_start_time + segment_duration/2.0, 0.2,
                      text_segment, color='white', ha='center')
    axarr[0].tick_params(axis='x', bottom='off', labelbottom='off')
    axarr[0].tick_params(axis='y', left='off', labelleft='off')

    # -- Plasma current (subplot 1, left axis)
    for i in np.where(signal_array[:,1]=='1')[0]:
        # Plot signal
        axarr[1].plot(wform[i].times, wform[i].values/1e3,  # in kA
                      'x-', label=signal_array[i,2], linewidth=2, markersize=10)
    # Display legend near the relevant axis (left or right). To be improved.
    axarr[1].legend(loc=2, fontsize=11)
    #advance the color cycler in order to NOT have the same color for twinx
    axarr[2]._get_lines.prop_cycler.__next__()
    
    # -- R,Z (subplot 1, right axis)
    for i in np.where(signal_array[:,1] == '2')[0]:
        if wform[i]:  # avoid case where it's None
            # Do not display non-existent waveforms (unused shape control modes).
            if len(wform[i].values != 0) > 0:
                
                axarr[2].plot(wform[i].times, wform[i].values,
                             'x--', linewidth=2, label=signal_array[i,2])
    axarr[2].legend(loc=1,fontsize=11)

    # -- Coil currents (subplot 2, left axis)
    for i in np.where(signal_array[:,1] == '3')[0]:    
        ip = wform[0].values
        current = wform[i].values
 
        # The poloidal current values are given proportional to the Ip.
        # 1st we interpolate the plasma current to the time of the current
        #
        # however it is possible that no plasma current are planned
        # for example during poloidal/divertor tests or cleaning pulses. 
        # In this case the poloidal current are not normalized
        if ip.size != 0: # Ip has been defined
            ip = np.interp(wform[i].times, wform[0].times, wform[0].values)
            current = current * ip

        axarr[3].plot(wform[i].times, current, 
                      'x-', label=signal_array[i,2], linewidth=2) 

            
 
        
    axarr[3].legend(loc=2, fontsize=8)
    
    # -- Divertor coil currents (subplot 2, right axis)
    for i in np.where(signal_array[:,1] == '4')[0]:
        axarr[4].plot(wform[i].times, wform[i].values,
                      'x--', label=signal_array[i,2], linewidth=2)
    axarr[4].legend(loc=1,fontsize=11)

    # -- Density request (subplot 3, left axis)
    for i in np.where(signal_array[:,1]=='5')[0]:
        if len(np.where(wform[i].values!=0)[0])>0:
            axarr[5].plot(wform[i].times,wform[i].values,
                          'x-', label=signal_array[i,2], linewidth=2)
    axarr[5].legend(loc=2, fontsize=11)

    # -- Gas valve opening requests (subplot 3, right axis)
    #advance the color cycler in order to NOT have the same color for twinx
    axarr[6]._get_lines.prop_cycler.__next__()
    
    for i in np.where(signal_array[:,1] == '6')[0]:
        if len(np.where(wform[i].values != 0)[0]) > 0:
            axarr[6].plot(wform[i].times, wform[i].values, 
                          'x--', label=signal_array[i,2], linewidth=2)
    axarr[6].legend(loc=1, fontsize=10)

    # -- Heating powers (subplot 4, left axis)
    for i in np.where(signal_array[:,1] == '7')[0]:
        axarr[7].plot(wform[i].times, wform[i].values/1e6,  # in MW
                      'x-', label=signal_array[i,2], linewidth=2)
    axarr[7].legend(loc=2, fontsize=10)

    # -- Heating phases (subplot 4, right axis)
    for i in np.where(signal_array[:,1] == '8')[0]:
        axarr[8].plot(wform[i].times, wform[i].values, 
                      'x--', label=signal_array[i,2], linewidth=2)
    axarr[8].legend(loc=1, fontsize=12)

    # -- generic to all subplots
    for (ind_ax, ax) in enumerate(axarr):
        # Display white vertical lines to mark segment transitions
        for segment in segmentTrajectory:
            segment_time = float(segment[1])
            ax.axvline(segment_time, color='w', ls='--', lw=0.5)

        # Y-axis labels
        ax.set_ylabel(ylabels[str(ind_ax)])

        # Set yaxis labels just beyond automatic limits to avoid having 
        # horizontal lines stuck to the top or the bottom of the subplot.
        ylim_inf, ylim_sup = ax.get_ylim()
        ax.set_ylim([ylim_inf - 0.1*abs(ylim_sup - ylim_inf),
                     ylim_sup + 0.1*abs(ylim_sup - ylim_inf)])
        
    # Set figure geometry
    fig.canvas.manager.window.setGeometry(fig_Xposition,fig_Yposition,
                                          fig_width,fig_height)

    # Reduce spaces between subplots to compactify the display
    fig.subplots_adjust(left=0.12, bottom=0.04, right=0.90, top=0.98,
                        wspace=0.15, hspace=0.05)
    
    axarr[0].set_xlim(left=32)  # zoom to t>ignitron
    
    #fig.tight_layout()
    plt.show()
