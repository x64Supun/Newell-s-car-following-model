# traffic_video.py  (library)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.patches import Wedge

from sim_data import road_length, tau, l_vehicle, delta_t, v_f, simulation_time, cycle_time, green_ratio, signal_pos

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
        
        is_green = (k * delta_t % cycle_time) <= (green_ratio * cycle_time)
        if is_green == True:
            signal_circle.set_facecolor("green")
        else:
            signal_circle.set_facecolor("red")
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

from matplotlib.patches import Wedge, Circle
from matplotlib.animation import FuncAnimation, FFMpegWriter

def make_traffic_video_5(
    trajectories: np.ndarray,
    road_length: float,
    l_vehicle: float,
    dt: float,
    output_filename: str = "traffic_ring.mp4",
    fps: int = 10,
    figsize: tuple = (6, 6),
    vehicle_thickness: float = 0.05,
):
    T, N = trajectories.shape
    alpha = np.pi * l_vehicle / road_length          # half-angle occupied by each car

    fig, ax = plt.subplots(figsize=figsize)
    ax.add_patch(plt.Circle((0, 0), 1.0, edgecolor="black", fill=False, lw=2))   # road

    # traffic light (small disk just above the ring)
    signal_circle = Circle((0, 1.2), 0.07, facecolor="green", edgecolor="k")
    ax.add_patch(signal_circle)

    wedges = [
        Wedge((0, 0), 1.0, 0, 0, width=vehicle_thickness, facecolor="C0", ec="k")
        for _ in range(N)
    ]
    for w in wedges:
        ax.add_patch(w)

    texts = [ax.text(0, 0, "", ha="center", va="center", fontsize=8) for _ in range(N)]

    ax.set_aspect("equal")
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.axis("off")
    title = ax.set_title("")

    def init():
        title.set_text("")
        for w in wedges:
            w.set_theta1(0)
            w.set_theta2(0)
        for txt in texts:
            txt.set_text("")
        return wedges + texts + [title, signal_circle]

    def update(frame):
        current_t = frame * dt
        title.set_text(f"Time = {current_t:.1f} s")

        # ----- signal colour -----
        is_green = (current_t % cycle_time) <= (green_ratio * cycle_time)
        signal_circle.set_facecolor("green" if is_green else "red")

        # ----- vehicles -----
        pos = trajectories[frame]
        angles = 2 * np.pi * pos / road_length
        for i, ang in enumerate(angles):
            start, end = np.degrees(ang - alpha), np.degrees(ang + alpha)
            wedges[i].set_theta1(start)
            wedges[i].set_theta2(end)

            # label at the centre of the wedge
            x, y = np.cos(ang), np.sin(ang)
            texts[i].set_position((x, y))
            texts[i].set_text(str(i))

        return wedges + texts + [title, signal_circle]

    anim = FuncAnimation(fig, update, frames=T, init_func=init, blit=True, interval=1000 / fps)
    writer = FFMpegWriter(fps=fps, codec="libx264", extra_args=["-pix_fmt", "yuv420p"])
    anim.save(output_filename, writer=writer, dpi=200)
    plt.close(fig)
    print(f"✔ Saved ring-road video to {output_filename}")
    return output_filename