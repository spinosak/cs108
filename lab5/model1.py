import numpy as np
from vispy import app, scene

canvas = scene.SceneCanvas(title='3D Scene', bgcolor='#050510', size=(900, 600), show=True)
view = canvas.central_widget.add_view()
view.camera = scene.TurntableCamera(fov=50, distance=6, elevation=20)

# --- Starfield ---
n_stars = 2000
stars_xyz = (np.random.rand(n_stars, 3) - 0.5) * 30
star_sizes = np.random.uniform(1, 3, n_stars)
scene.visuals.Markers(pos=stars_xyz, size=star_sizes,
                      face_color=(1, 1, 1, 0.6), edge_width=0,
                      parent=view.scene)

# --- Torus of colored points ---
n = 8000
# --- Torus of colored points (structured grid instead of random) ---
n_u = 120
n_v = 80

u_vals = np.linspace(0, 2 * np.pi, n_u)
v_vals = np.linspace(0, 2 * np.pi, n_v)

u, v = np.meshgrid(u_vals, v_vals)
u = u.ravel()
v = v.ravel()

R, r = 1.5, 0.5

x = (R + r * np.cos(v)) * np.cos(u)
y = (R + r * np.cos(v)) * np.sin(u)
z = r * np.sin(v)

torus_pts = np.column_stack([x, y, z])

# Color by angle around the ring
hue = (u / (2 * np.pi))

n = u.size  # IMPORTANT: matches meshgrid output

colors = np.zeros((n, 4))
colors[:, 0] = np.abs(np.sin(hue * np.pi))        # R
colors[:, 1] = np.abs(np.sin(hue * np.pi + 2.1))  # G
colors[:, 2] = np.abs(np.sin(hue * np.pi + 4.2))  # B
colors[:, 3] = 0.85

torus = scene.visuals.Markers(pos=torus_pts, size=2.5,
                               face_color=colors, edge_width=0,
                               parent=view.scene)

# --- Rotation ---
def on_timer(event):
    torus.transform = scene.transforms.MatrixTransform()
    angle = event.elapsed * 30  # degrees/sec
    torus.transform.rotate(angle, (0, 0, 1))
    canvas.update()

timer = app.Timer(interval=1/60, connect=on_timer, start=True)

if __name__ == '__main__':
    app.run()
    