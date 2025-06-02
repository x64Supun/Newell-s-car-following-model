import numpy as np
import matplotlib.pyplot as plt

from sim_data import *

def signal_phase(t):
    t_in_cycle = t % cycle_time
    if t_in_cycle <= green_time:
        return 'green'
    elif t_in_cycle <= green_time + yellow_time:
        return 'yellow'
    else:
        return 'red'

def simulate_signal(N, simulation_time):
    steps   = int(simulation_time / delta_t)

    # initial positions evenly spaced + (road_length / 2)
    pos_abs = (np.linspace(0, road_length, N, endpoint=False) + road_length/2) % road_length

    traj   = np.zeros((steps, N))
    speeds = np.zeros((steps, N))

    prev_phase = 'green'
    j_queue    = None

    for k in range(steps):
        t_abs  = k * delta_t
        phase  = signal_phase(t_abs)               # green -> yellow -> red
        d_bar  = (signal_pos - pos_abs) % road_length  # bumper-to-bar distances

        # signal phase transition
        if phase != prev_phase:

            if phase == 'green':
                # when light turns green → release the queue
                j_queue = None

            elif phase == 'yellow' and j_queue is None:
                # first yellow step of the cycle, pick the queue-front car once
                idx_app = np.where(d_bar > 0)[0]  # cars still upstream
                if len(idx_app) > 0:
                    # nearest-to-farther ordering
                    sort_idx = idx_app[np.argsort(d_bar[idx_app])]
                    for idx in sort_idx:
                        if d_bar[idx] > s_2:  # first car beyond s_2
                            j_queue = idx  # j_queue is fixed until the next green phase
                            break
                # if every car is within s_2, nobody stops; j_queue stays None

            # when the light turns red, nothing is done, j_queue stays fixed until the next green
            #     j_queue keeps whatever value it acquired in yellow
        # leader gaps and desired speds
        leaders     = (np.arange(N) + 1) % N
        raw_gap     = pos_abs[leaders] - pos_abs - l_vehicle
        gap_leader  = raw_gap % road_length
        v_leader    = gap_leader / tau

        v_des = np.zeros(N)

        if phase == 'green':
            v_des[:] = np.minimum(v_leader, v_f)

        elif phase == 'yellow':
            # near / far masks relative to s_2
            near_mask = d_bar <= s_2
            v_des[near_mask] = np.minimum(v_leader[near_mask], v_f)

            if j_queue is not None:
                gap_bar = max(d_bar[j_queue], 0.0) # removed the l_vehicle subtraction
                v_des[j_queue] = min(gap_bar / tau, v_f, v_leader[j_queue]) # corrected to fix overtaking

            # all other cars (far & not j_queue) follow their leader
            others = [i for i in range(N) if (i != j_queue) and (not near_mask[i])]
            for i in others:
                v_des[i] = min(v_leader[i], v_f)

        else:   # phase == 'red'
            if j_queue is not None:
                gap_bar = max(d_bar[j_queue], 0.0) # removed the l_vehicle substraction
                v_des[j_queue] = min(gap_bar / tau, v_f, v_leader[j_queue]) # corrected t fix overtaking

            # everyone else still follows leader
            for i in range(N):
                if i == j_queue:
                    continue
                v_des[i] = min(v_leader[i], v_f)

        # advance one time step
        traj[k]   = pos_abs
        speeds[k] = v_des
        pos_abs   = (pos_abs + v_des * delta_t) % road_length
        prev_phase = phase

    sms = speeds.mean(axis=1)
    return traj, sms

# picks a random vehicle between s_1 and s_2 and sets it as j_queue
def simulate_signal_2(N, simulation_time, rng = None):
    if rng is None:                          # ensure we always have an RNG
        rng = np.random.default_rng()

    steps   = int(simulation_time / delta_t)
    pos_abs = (np.linspace(0, road_length, N, endpoint=False) + road_length/2) % road_length

    traj   = np.zeros((steps, N))
    speeds = np.zeros((steps, N))

    prev_phase = 'green'
    j_queue    = None

    for k in range(steps):
        t_abs   = k * delta_t
        phase   = signal_phase(t_abs)                      # 'green' | 'yellow' | 'red'
        d_bar   = (signal_pos - pos_abs) % road_length     # front-bumper → bar

        # phase transition
        if phase != prev_phase:
            if phase == 'green':
                j_queue = None                             # release queue
            elif phase == 'yellow' and j_queue is None:
                idx_app = np.where((d_bar > s_1) & (d_bar <= s_2))[0]
                if idx_app.size:
                    j_queue = rng.choice(idx_app)          # random pick

        # leader gaps & candidate speeds
        leaders     = (np.arange(N) + 1) % N
        raw_gap     = pos_abs[leaders] - pos_abs - l_vehicle
        gap_leader  = raw_gap % road_length
        v_leader    = gap_leader / tau

        v_des = np.zeros(N)

        if phase == 'green':
            v_des[:] = np.minimum(v_leader, v_f)

        elif phase == 'yellow':
            near_mask = d_bar <= s_1                       # ≤ s₁ are “near”
            v_des[near_mask] = np.minimum(v_leader[near_mask], v_f)

            if j_queue is not None:
                gap_bar = d_bar[j_queue]                   # front-bumper gap
                v_des[j_queue] = min(gap_bar / tau, v_leader[j_queue], v_f)

            others = [i for i in range(N) if (i != j_queue) and (not near_mask[i])]
            for i in others:
                v_des[i] = min(v_leader[i], v_f)

        else:  # phase == 'red'
            if j_queue is not None:
                gap_bar = d_bar[j_queue]
                v_des[j_queue] = min(gap_bar / tau, v_leader[j_queue], v_f)

            for i in range(N):
                if i == j_queue:
                    continue
                v_des[i] = min(v_leader[i], v_f)

        # advance one Δt
        traj[k]   = pos_abs
        speeds[k] = v_des
        pos_abs   = (pos_abs + v_des * delta_t) % road_length
        prev_phase = phase

    sms = speeds.mean(axis=1)
    return traj, sms