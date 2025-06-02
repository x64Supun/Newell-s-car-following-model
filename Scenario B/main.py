import numpy as np
import matplotlib.pyplot as plt
from IPython.display import Video, display
from matplotlib.patches import Wedge

from sim_data import road_length, tau, l_vehicle, delta_t, v_f, simulation_time, cycle_time, green_ratio, signal_pos, signal_pos_1, signal_pos_2

from simulate_signal import simulate_signal_4
from plot_fixed_positions import *
from plot_functions import *
from signal_background import *
from video_output import *

if __name__ == '__main__':

    N = int(input("Enter number of vehicles (1–120): "))
    initial_pos = np.linspace(0, road_length, N, endpoint=False)  % road_length
    # 1) run simulation
    traj_full, sms_full = simulate_signal_4(N, simulation_time)

    final_pos = traj_full[-1]
    # 2) drop the first 30% of records
    # skip = int(0.3 * traj_full.shape[0])
    t = np.arange(traj_full.shape[0]) * delta_t
    traj = traj_full
    sms = sms_full

    # 3) build the corresponding time axis
    # t = np.arange(traj_full.shape[0]) * delta_t

    # 4) single‐density plots

    plot_fixed_circle_positions(initial_pos, final_pos)
    plot_trajectories_2(t, traj, N)
    plot_sms(t, sms)

    t0, t1 = time_window
    mask_time = (t >= t0) & (t <= t1)
    t_z = t[mask_time]
    traj_z = traj[mask_time]

# zoomed in by just TIME
    fig, ax = plt.subplots(figsize=(10, 8))
#   draw_signal_background(ax, t_z)
    for i in range(N):
        y = traj_z[:, i]
        dy = np.abs(np.diff(y, prepend=y[0]))
        y_masked = np.ma.array(y, mask = dy > (road_length / 2))
        ax.plot(t_z, y_masked, label=f'Vehicle {i}')
#   ax.axhline(signal_pos, color='r', ls='-', label='Stop bar')
#   ax.axhline(signal_pos_1, color='r', ls='-', label='Stop bar')
#   ax.axhline(signal_pos_2, color='r', ls='-', label='Stop bar')
    plot_time_colored_bar(ax, t_z, signal_pos, cycle_time, green_ratio, lw=3)
    plot_time_colored_bar(ax, t_z, signal_pos + 500.0, cycle_time, green_ratio, lw=3)
    plot_time_colored_bar(ax, t_z, signal_pos + 1010.0, cycle_time, green_ratio, lw=3)
#   draw_signal_background(ax, t)
    ax.set_xlim(t0, t1)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Position (m)')
    ax.set_title(f'Time-zoomed Trajectories: t ∈ [{t0},{t1}] s')
  # ax.legend(loc = 'center left')
    ax.grid(True)
#   ax.tight_layout()
    plt.show()


# zoom in by the POSITION and TIME
    x0, x1 = loc_window
    fig, ax = plt.subplots(figsize=(10, 8), dpi=200)
#   shade the entire time axis according to the signal
#   draw_signal_background(ax, t)

    for i in range(N):
        y = traj[:, i]
        dy = np.abs(np.diff(y, prepend=y[0]))
        wrap_mask = dy > (road_length / 2)
        window_mask = (y < x0) | (y > x1)
        mask = wrap_mask | window_mask
        y_masked = np.ma.array(y, mask = mask)
      # mask_space = (traj[:, i] >= x0) & (traj[:, i] <= x1)
      # ax.plot(t[mask_space], traj[mask_space, i],
            #   linestyle='--', label=f'Vehicle {i}')
        ax.plot(t, y_masked, ls = '--', label = f'Vehicle {i}')
    # draw the stop bar
#   ax.axhline(signal_pos, color='r', ls='-', label='Stop bar')
#   ax.axhline(signal_pos_2, color='r', ls='-', label='Stop bar')

    ax.set_xlim(t0, t1)
    ax.set_ylim(x0 - 25, x1 + 25)
#   plot_time_colored_bar(ax, t_z, signal_pos + 1010.0, cycle_time, green_ratio, lw=2) custom horizontal line
    plot_time_colored_bar(ax, t_z, signal_pos + 1010.0, cycle_time, green_ratio, lw=3)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Position (m)')
    ax.set_title(f'Trajectories: x ∈ [{x0},{x1}] m')
#   ax.legend(loc='center left')
    ax.grid(True)
#   plt.tight_layout()
    plt.show()

# MFD
    plot_mfd()

# simulation video
    """
    make_traffic_video_5(
        trajectories=traj,
        road_length=road_length,
        dt=delta_t,
        l_vehicle = 5.0,
        output_filename="traffic.mp4",
        fps=10,
        #figsize=(6, 6),
        #dot_size=80,
    )
    """