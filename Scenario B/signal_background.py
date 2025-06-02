import numpy as np
import matplotlib.pyplot as plt

from sim_data import road_length, tau, l_vehicle, delta_t, v_f, simulation_time, cycle_time, green_ratio, signal_pos


def draw_signal_background(ax, t, cycle=cycle_time, green_frac=green_ratio):

    n_cycles = int(np.ceil(t[-1] / cycle))
    for k in range(n_cycles):
        t0 = k*cycle
        tg = t0 + green_frac*cycle
        ax.axvspan(t0, tg,  facecolor='green', alpha=0.2)
        ax.axvspan(tg,  t0+cycle, facecolor='red',   alpha=0.2)


def plot_time_colored_bar(ax, t, y_pos, cycle_time, green_ratio, lw=2):
    # 1) Compute a boolean array is_green[i] = True if t[i] is in a green‐phase.
    is_green = ((t % cycle_time) < (green_ratio * cycle_time))

    # 2) Find all indices where the phase flips (green→red or red→green).
    #    We'll break the t‐axis into contiguous chunks of “all‐green” or “all‐red.”
    phase_changes = np.where(np.diff(is_green.astype(int)) != 0)[0]

    # 3) Walk through these change‐points and draw each chunk.
    start_idx = 0
    for ch in phase_changes:
        end_idx = ch
        color = 'green' if is_green[start_idx] else 'red'

        # draw a horizontal line from t[start_idx] up to t[end_idx]
        ax.hlines(y=y_pos,
                  xmin=t[start_idx],
                  xmax=t[end_idx],
                  colors=color,
                  linewidth=lw)

        start_idx = end_idx + 1

    # 4) Finally draw the last segment (from the last change‐point to t[-1])
    color = 'green' if is_green[start_idx] else 'red'
    ax.hlines(y=y_pos,
              xmin=t[start_idx],
              xmax=t[-1],
              colors=color,
              linewidth=lw)