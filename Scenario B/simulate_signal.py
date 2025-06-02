import numpy as np
import matplotlib.pyplot as plt

from sim_data import road_length, tau, l_vehicle, delta_t, v_f, simulation_time, cycle_time, green_ratio, signal_pos


def simulate_signal_4(N, simulation_time):
    steps = int(simulation_time / delta_t)
    # start evenly spaced around the ring
    pos_abs = (np.linspace(0, road_length, N, endpoint=False)
               + road_length / 2) % road_length

    traj = np.zeros((steps, N))
    speeds = np.zeros((steps, N))

    prev_green  = True # tells the color of the signal light one step ago
    j_queue     = None # index of the car that is supposed to stop

    for k in range(steps):
        t_abs = k * delta_t
        # green for the first green_ratio of each cycle
        is_green = (t_abs % cycle_time) <= (green_ratio * cycle_time)

        if prev_green and not is_green:
            gap_signal = (signal_pos - pos_abs) % road_length
            idx_app = np.where(gap_signal > 0)[0]
            if len(idx_app) > 0:
                j_queue = idx_app[np.argmin(gap_signal[idx_app])]
            else:
                j_queue = None

            # as soon as green returns, clear j_queue and cars follow their leader
        if is_green:
            j_queue = None

            # record positions
        traj[k] = pos_abs

        # compute leader‐gaps
        leaders = (np.arange(N) + 1) % N
        raw_gap = pos_abs[leaders] - pos_abs - l_vehicle
        gap_leader = raw_gap % road_length
        v_leader = gap_leader / tau

        # desired speeds
        v_des = np.zeros(N)
        if is_green:
            # when green everyone follows their leader
            v_des[:] = np.minimum(v_leader, v_f)
        else:
            # when red, apply Newell to j_queue only, fix it all red
            if j_queue is not None:
                # bumper‐to‐bar gap
                barrier_gap = (signal_pos - pos_abs[j_queue]) % road_length
                barrier_gap = max(barrier_gap, 0.0) # removed the subtracted l_vehicle
                v_des[j_queue] = min(barrier_gap / tau, v_f)
            # everyone else uses their leader‐gap
            others = [i for i in range(N) if i != j_queue]
            for i in others:
                v_des[i] = min(v_leader[i], v_f)

        # update for next step
        speeds[k] = v_des
        pos_abs = (pos_abs + v_des * delta_t) % road_length
        prev_green = is_green

    sms = speeds.mean(axis=1)
    return traj, sms
