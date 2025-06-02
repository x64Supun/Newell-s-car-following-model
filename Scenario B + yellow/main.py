import numpy as np
import matplotlib.pyplot as plt
from IPython.display import Video, display
from matplotlib.patches import Wedge

from simulate_signal import *
from plot_fixed_positions import *
from plot_functions import *
from signal_background import *
from video_output import *

from sim_data import *

if __name__ == '__main__':

    N = int(input("Enter number of vehicles (1–120): "))
    initial_pos = np.linspace(0, road_length, N, endpoint=False)  % road_length
    # 1) run simulation
    traj_full, sms_full = simulate_signal_2(N, simulation_time)

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
    plot_trajectories(t, traj, N)
    plot_sms(t, sms)

    t0, t1 = time_window
    mask_time = (t >= t0) & (t <= t1)
    t_z = t[mask_time]
    traj_z = traj[mask_time]


    t0, t1 = time_window
    mask_time = (t >= t0) & (t <= t1)
    t_z = t[mask_time]
    traj_z = traj[mask_time]

    # zoomed in by TIME
    fig, ax = plt.subplots(figsize=(10, 8), dpi = 200)
#   draw_signal_background(ax, t_z)
    for i in range(N):
        y = traj_z[:, i]
        dy = np.abs(np.diff(y, prepend = y[0]))
        y_masked = np.ma.array(y, mask = dy > (road_length / 2))
        ax.plot(t_z, y_masked, label=f'Vehicle {i}')
#   ax.axhline(signal_pos, color='r', ls='--', label='Stop bar')
#   draw_signal_background(ax, t)
    plot_signal_bar(ax, t, y_level=signal_pos, dt=delta_t)
    plot_signal_bar(ax, t, y_level=signal_pos + 500.0, dt=delta_t)
    plot_signal_bar(ax, t, y_level=signal_pos + 1010.0, dt=delta_t)
    ax.set_xlim(t0, t1)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Position (m)')
    ax.set_title(f'Trajectories: t ∈ [{t0},{t1}] s')
   # ax.legend(loc = 'center left')
    ax.grid(True)
   # ax.tight_layout()
    plt.show()


# zoom in by the POSITION and TIME
    x0, x1 = loc_window  # spatial window in metres
    idx0 = np.searchsorted(t, t0)
    idx1 = np.searchsorted(t, t1) + 1  # inclusive upper bound

    fig, ax = plt.subplots(figsize=(12, 6), dpi=200)
#   draw_signal_background(ax, t)  # shade the *full* time axis

    for i in range(N):
        y_window = traj[idx0:idx1, i]

        dy = np.abs(np.diff(y_window, prepend=y_window[0]))
        wrap_mask = dy > (road_length / 2)
        window_mask = (y_window < x0) | (y_window > x1)
        local_mask = wrap_mask | window_mask

        y_masked = np.ma.array(y_window, mask=local_mask)

        y_full = np.ma.masked_all_like(t)
        y_full[idx0:idx1] = y_masked

        ax.plot(t, y_full, ls='--', label=f'Vehicle {i}')

    # stop bar and cosmetics
#   ax.axhline(signal_pos, color='r', ls='--', label='Stop bar')
    plot_signal_bar(ax, t, y_level=signal_pos + 1004.0, dt=delta_t)
    ax.set_xlim(t0, t1)  # zoom x-axis to window
    ax.set_ylim(x0 - 25, x1 + 25)  # zoom y-axis to spatial window5
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Position (m)')
    ax.set_title(f'Trajectories: x ∈ [{x0}, {x1}] m')
  #  ax.legend(loc='center left')
    ax.grid(True)
    plt.tight_layout()
    plt.show()

    # plot the MFD
    plot_mfd()

    """
    make_traffic_video_4(
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