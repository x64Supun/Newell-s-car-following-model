import numpy as np
import matplotlib.pyplot as plt

from sim_data import *
from simulate_signal import *

def draw_signal_background(ax, t, cycle = cycle_time, green_time = green_time, yellow_time = yellow_time, red_time = red_time):
    """
    Shade vertical bands on ax: green, yellow, then red each cycle.
    t must be a 1D array of time stamps (in seconds).
    """
    n_cycles = int(np.ceil(t[-1] / cycle))
    for k in range(n_cycles):
        t0 = k * cycle
        t_green_end  = t0 + green_time
        t_yellow_end = t_green_end + yellow_time
        t_red_end    = t0 + cycle

        # green
        ax.axvspan(t0, t_green_end,  facecolor='green',  alpha=0.2)
        # yellow
        ax.axvspan(t_green_end, t_yellow_end, facecolor='yellow', alpha=0.2)
        # red
        ax.axvspan(t_yellow_end, t_red_end,   facecolor='red',    alpha=0.2)

def plot_signal_bar(ax, t: np.ndarray, y_level: float, dt: float):
    """
    Draw a horizontal “bar” at y = y_level whose color at each small time‐interval is
    determined by the 3‐phase function signal_phase(t). We simply plot a sequence of
    tiny horizontal segments [t[k], t[k+1]] at y = y_level, color‐coded by phase.
    """
    # We assume t is sorted, equally spaced, and dt = t[1] - t[0].
    # We will draw T−1 little line‐segments, each colored by the phase at its left endpoint.
    T = len(t)
    for k in range(T - 1):
        phase_color = signal_phase(t[k])
        # draw a short line from t[k] to t[k+1], at y = y_level
        ax.plot([t[k], t[k+1]], [y_level, y_level], color=phase_color, linewidth=4, solid_capstyle='butt')