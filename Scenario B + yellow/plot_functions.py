import numpy as np
import matplotlib.pyplot as plt

from sim_data import *
from signal_background import *
from simulate_signal import *

# full trajectory plot
def plot_trajectories(t, traj, N):
   # plt.figure(figsize=(10, 6), dpi=200)
    fig, ax = plt.subplots(figsize=(20, 12), dpi=200)
#   draw_signal_background(ax, t)
    for i in range(N):
        y = traj[:, i]
        dy = np.abs(np.diff(y, prepend = y[0]))
        y_masked = np.ma.array(y, mask = dy > (road_length / 2))
        ax.plot(t, y_masked, linewidth=0.7, label=f"vehicle {i}")
    handles, labels = ax.get_legend_handles_labels()
    """
    ax.legend(handles, labels,
              loc = 'center left',
              bbox_to_anchor = (1.02, 0.5),
              borderaxespad = 0,
              fontsize = 'small',
              frameon = False)
    """
    fig.subplots_adjust(right = 0.8)
    ax.axhline(signal_pos, color='r', linestyle='--', label='Stop bar')
    ax.set_xlabel('Time (s)');
    ax.set_ylabel('Position (m)')
    ax.set_title(f'Vehicle Trajectories (N={N})')
  #  ax.legend(loc = 'center left');
    ax.grid(True);
    plt.tight_layout();
    plt.show()
    """
    for i in range(N):
        plt.plot(t, traj[:, i], linewidth=0.7, label=f"vehicle {i}")
    plt.axhline(signal_pos, color='r', linestyle='--', label='Signal @0 m/1000 m')
    plt.xlabel('Time (s)')
    plt.ylabel('Position along ring (m)')
    plt.title(f'Vehicle Trajectories (N={N})')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show() """

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
        _, sms = simulate_signal(N, simulation_time)
        # MFD already discards first 30% internally here:
        stable_sms = sms[int(0.3 * len(sms)):]
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