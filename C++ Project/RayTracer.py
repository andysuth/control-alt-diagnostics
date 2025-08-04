import matplotlib.pyplot as plt
import numpy as np

def intersect_lines(p1, d1, p2, d2):
    """
    Compute intersection point of two parametric lines:
    r1(t1) = p1 + t1*d1
    r2(t2) = p2 + t2*d2
    Solves for r1 == r2
    """
    # Set up system: p1 + t1*d1 = p2 + t2*d2
    A = np.array([d1, -d2]).T  # 2x2
    b = p2 - p1

    if np.linalg.matrix_rank(A) < 2:
        return None  # Lines are parallel

    t = np.linalg.solve(A, b)
    intersection = p1 + t[0] * d1
    return intersection

# === Parameters ===
focal_y = -5.0        # Intended focus position
slab_top = 0.0
slab_bottom = -2.0
extend_length = 0.0
ray_color = "#8A2BE2"  # Violet
ghost_color = "gray"   # For no-glass reference rays
filename = "ray_bundle.txt"

# === Load ray data ===
rays = []
angles = []
current_ray = []

with open(filename, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            if current_ray:
                rays.append(current_ray)
                current_ray = []
        else:
            angle, x, y = map(float, line.split())
            current_ray.append(np.array([x, y]))
    if current_ray:
        rays.append(current_ray)

# === Plot setup ===
plt.figure(figsize=(8, 6))

# Glass slab background
plt.axhspan(slab_bottom, slab_top, facecolor='lightgray', alpha=0.5, label="Glass Slab")

# === Plot each ray and overlay reference (air-only) ray ===
for ray in rays:
    ray = np.array(ray)
    p0 = ray[0]
    p1 = ray[1]
    dir_vec = (p1 - p0)
    dir_vec /= np.linalg.norm(dir_vec)

    # Plot actual ray through glass
    x_vals, y_vals = ray[:, 0], ray[:, 1]
    plt.plot(x_vals, y_vals, color=ray_color, linewidth=1.5)

    # Extend actual ray
    if len(ray) >= 2:
        p_last = ray[-1]
        d_last = (ray[-1] - ray[-2])
        d_last /= np.linalg.norm(d_last)
        p_ext = p_last + d_last * extend_length
        plt.plot([p_last[0], p_ext[0]], [p_last[1], p_ext[1]],
                 linestyle='--', color=ray_color, alpha=0.8)

    # Plot no-glass (air-only) path
    # Extend from start point p0 to same y-depth as actual ray or focal_y
    if dir_vec[1] == 0:
        continue  # avoid divide-by-zero for flat rays

    y_target = focal_y
    t = (y_target - p0[1]) / dir_vec[1]
    p_virtual = p0 + dir_vec * t

    plt.plot([p0[0], p_virtual[0]], [p0[1], p_virtual[1]],
             linestyle='--', color=ghost_color, linewidth=1.2, alpha=0.6)

# === Overlays ===
plt.axhline(slab_top, linestyle='--', color='gray', linewidth=0.8)
plt.axhline(slab_bottom, linestyle='--', color='gray', linewidth=0.8)
plt.plot(0, focal_y, 'rx', markersize=8, label='Intended Focus (No Slab)')

# === Formatting ===
plt.title("Laser Ray Bundle Through Glass Slab vs No-Slab Reference")
plt.xlabel("x position")
plt.ylabel("y position")
plt.axis("equal")
plt.grid(True)
plt.legend(loc="upper right")
plt.tight_layout()

# === Find beam waist from ray intersections ===
intersection_points = []

for i in range(len(rays)):
    for j in range(i+1, len(rays)):
        ray1 = rays[i]
        ray2 = rays[j]

        if len(ray1) < 2 or len(ray2) < 2:
            continue

        p1 = ray1[-2]
        p2 = ray1[-1]
        d1 = p2 - p1
        d1 /= np.linalg.norm(d1)

        q1 = ray2[-2]
        q2 = ray2[-1]
        d2 = q2 - q1
        d2 /= np.linalg.norm(d2)

        pt = intersect_lines(p1, d1, q1, d2)
        if pt is not None and -10 < pt[1] < 10:  # filter for sensible y-range
            intersection_points.append(pt)

# === Average intersection ===
if intersection_points:
    intersection_points = np.array(intersection_points)
    mean_focus = np.mean(intersection_points, axis=0)
    print(f"Estimated focus from intersections: ({mean_focus[0]:.3f}, {mean_focus[1]:.3f})")

    # Add to plot
    plt.plot(mean_focus[0], mean_focus[1], 'ko', label="Numerical Focus (Rays)")
    plt.axhline(mean_focus[1], linestyle=':', color='k', alpha=0.4)
else:
    print("No intersections found.")


# === Compute and annotate defocus ===
intended_focus_y = np.array([0.0, focal_y])
actual_focus_y = mean_focus
defocus = actual_focus_y - intended_focus_y

annotation_text = (
    f"Waist shift (Δx, Δy): ({defocus[0]:+.2f}, {defocus[1]:+.2f}) units"
)
plt.text(0.4+ mean_focus[0] + 0.2, mean_focus[1],
    annotation_text,
    fontsize=10, color='black', ha='left', va='bottom',
    bbox=dict(facecolor='white', edgecolor='gray', alpha=0.8))

plt.show()


