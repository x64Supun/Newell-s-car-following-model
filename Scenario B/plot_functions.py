import numpy as np
import matplotlib.pyplot as plt

from sim_data import road_length, tau, l_vehicle, delta_t, v_f, simulation_time, cycle_time, green_ratio, signal_pos, time_window, loc_window

from simulate_signal import *
from sim_data import time_window, loc_window
from signal_background import *


# background color according to the signal color
def draw_signal_background(ax, t, cycle=cycle_time, green_frac=green_ratio):
    n_cycles = int(np.ceil(t[-1] / cycle))
    for k in range(n_cycles):
        t0 = k*cycle
        tg = t0 + green_frac*cycle
        ax.axvspan(t0, tg,  facecolor='green', alpha=0.2)
        ax.axvspan(tg,  t0+cycle, facecolor='red',   alpha=0.2)


# trajectory plot without the wrap-up vertical lines
def plot_trajectories_2(t, traj, N, road_length=1000.0):
    fig, ax = plt.subplots(figsize=(10,6), dpi=200)
#   draw_signal_background(ax, t)

    for i in range(N):
        y = traj[:, i]
        # compute jumps
        dy = np.abs(np.diff(y, prepend=y[0]))
        # mask any point that follows a big jump; in this case wrap around
        y_masked = np.ma.array(y, mask=dy > (road_length/2))
        ax.plot(t, y_masked, linewidth=0.7, label=f"vehicle {i}")
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels,
              loc='center left',
              bbox_to_anchor=(1.02, 0.5),
              borderaxespad=0,
              fontsize='small',
              frameon=False)
    fig.subplots_adjust(right=0.8)
    ax.axhline(signal_pos, color='r', linestyle='-', label='Stop bar')
    """
    plot_time_colored_bar(ax, t_z, signal_pos, cycle_time, green_ratio, lw=2)
    plot_time_colored_bar(ax, t_z, signal_pos + 500.0, cycle_time, green_ratio, lw=2)
    plot_time_colored_bar(ax, t_z, signal_pos + 1000.0, cycle_time, green_ratio, lw=2)
    """
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Position (m)')
    ax.set_title(f'Vehicle Trajectories (N={N})')
#   ax.legend(loc = 'center left');
    ax.grid(True)
    plt.tight_layout()
    plt.show()

# SMS vs. time plot
def plot_sms(t, sms):
    plt.figure(figsize=(10, 6))
    plt.plot(t, sms, linewidth=1.2)
    plt.xlabel('Time (s)')
    plt.ylabel('Space‐mean Speed (m/s)')
    plt.title('Space‐Mean Speed vs Time')
    plt.ylim(0, v_f * 1.1)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# MFD plot
def plot_mfd():
    Ns = np.arange(1, 121)
    q_vals = []
    for N in Ns:
        _, sms = simulate_signal_4(N, simulation_time)
        # MFD already discards first 50% internally here:
        stable_sms = sms[int(0.5 * len(sms)):]
        v_avg = stable_sms.mean()
        q = N * v_avg * 3600 / road_length
        q_vals.append(q)

    plt.figure(figsize=(10, 6))
    plt.plot(Ns, q_vals, 'b-', linewidth=2)
    plt.xlabel('Density (veh/km)')
    plt.ylabel('Flow (veh/h)')
    plt.title('Fundamental Diagram (Signalized Ring)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()