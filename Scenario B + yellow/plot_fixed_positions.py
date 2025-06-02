import numpy as np
import matplotlib.pyplot as plt

from sim_data import  road_length, tau, l_vehicle, delta_t, v_f, simulation_time, cycle_time, green_time, yellow_time, red_time, signal_pos, s_1, s_2, time_window, loc_window

from signal_background import *

def plot_fixed_circle_positions(initial_pos, final_pos):
    """
    Draw two fixed‐scale unit circles side by side,
    with vehicle positions (annotated) on each.
    """
  #  traj_full, sms_full = simulate_signal(N, simulation_time)
   # t_full = np.arange(traj_full.shape[0]) * delta_t

    # compute initial & final positions for the placement plots

   # final_pos= traj_full[-1]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,6))

    for ax, pos_array, title, color in (
        (ax1, initial_pos, "Initial placement", "C0"),
        (ax2, final_pos,   "Final placement",   "C3")
    ):
        # compute angles around unit circle
        theta = 2*np.pi * pos_array / road_length
        x, y  = np.cos(theta), np.sin(theta)

        # draw the ring (unit circle)
        ring = plt.Circle((0,0), 1.0, edgecolor='k', fill=False, linewidth=2)
        ax.add_artist(ring)

        # plot vehicles
        ax.scatter(x, y, c=color, s=80, zorder=3)
        for idx, (xi, yi) in enumerate(zip(x, y)):
            ax.text(xi, yi, str(idx),
                    color='white', fontsize=8,
                    ha='center', va='center', zorder=4)

        # fix axes so circle always looks like a circle
        ax.set_aspect('equal', 'box')
        ax.set_xlim(-1.1, 1.1)
        ax.set_ylim(-1.1, 1.1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(title)

    plt.tight_layout()
    plt.show()