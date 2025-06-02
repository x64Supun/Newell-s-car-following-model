# traffic_video.py  (library)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.patches import Wedge

from sim_data import  road_length, tau, l_vehicle, delta_t, v_f, simulation_time, cycle_time, green_time, yellow_time, red_time, signal_pos, s_1, s_2, time_window, loc_window

def make_traffic_video_4(
    trajectories: np.ndarray,
    road_length: float,
    l_vehicle: float,
    dt: float,
    output_filename: str = "traffic_ring.mp4",
    fps: int = 10,
    figsize: tuple = (6, 6),
    vehicle_thickness: float = 0.05
):
    T, N = trajectories.shape

    # half‐angle for each vehicle:
    alpha = np.pi * l_vehicle / road_length  # radians

    fig, ax = plt.subplots(figsize=figsize)
    ring = plt.Circle((0, 0), 1.0, edgecolor='black', fill=False, linewidth=2)
    ax.add_patch(ring)

    # 1) create N wedges
    wedges = [
        Wedge((0,0), 1.0,
              theta1=0, theta2=0,
              width=vehicle_thickness,
              facecolor='C0', edgecolor='k')
        for _ in range(N)
    ]
    for w in wedges:
        ax.add_patch(w)

    # 2) text labels
    texts = [
        ax.text(0, 0, "", ha="center", va="center", fontsize=8, color="k")
        for _ in range(N)
    ]

    ax.set_aspect('equal')
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.axis('off')
    title = ax.set_title("")

    def init():
        title.set_text("")
        for w in wedges:
            w.set_theta1(0)
            w.set_theta2(0)
        for txt in texts:
            txt.set_text("")
        return wedges + texts + [title]

    def update(frame):
        title.set_text(f"Time = {frame*dt:.1f} s")
        pos    = trajectories[frame]
        angles = 2 * np.pi * pos / road_length
        """
        to include a signal light in the video
        
        is_green = (t * delta_t % cycle_time) <= (green_ratio * cycle_time)
        if is_green == True:
            signal_circle.set_facecolor("green")
        else:
            signal_circle.set_facecolor("red") """
        for i, ang in enumerate(angles):
            # set wedge arc
            start = np.degrees(ang - alpha)
            end   = np.degrees(ang + alpha)
            wedges[i].set_theta1(start)
            wedges[i].set_theta2(end)
            # position text at the wedge center
            mid_ang = ang
            x, y = np.cos(mid_ang), np.sin(mid_ang)
            texts[i].set_position((x, y))
            texts[i].set_text(str(i))
        return wedges + texts + [title]

    anim = FuncAnimation(
        fig, update, frames=T, init_func=init,
        blit=True, interval=1000/fps
    )

    writer = FFMpegWriter(
        fps=fps,
        codec="libx264",
        extra_args=["-pix_fmt", "yuv420p"]
    )
    anim.save(output_filename, writer=writer, dpi=200)
    plt.close(fig)
    print(f"✔ Saved ring-road video to {output_filename}")
    return output_filename