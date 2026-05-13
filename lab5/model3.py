from vispy import app, scene
import numpy as np

canvas = scene.SceneCanvas(
    title='Animated Scalar Field',
    bgcolor='#020008',
    size=(900, 600),
    show=True
)

view = canvas.central_widget.add_view()
view.camera = scene.TurntableCamera(fov=55, distance=7, elevation=25)

# --- Grid ---
res = 30
lin = np.linspace(-2, 2, res)
gx, gy, gz = np.meshgrid(lin, lin, lin)
pts = np.column_stack([gx.ravel(), gy.ravel(), gz.ravel()]).astype(np.float32)

# --- Field ---
def field_value(t):
    r2 = gx**2 + gy**2 + gz**2

    # BIGGER pulsation so it's visible
    sigma = 0.4 + 0.5 * np.sin(t * 1.5)

    blob = np.exp(-r2 / (2 * sigma**2))

    # add wave interference (this makes motion obvious)
    wave = 0.5 * np.sin(3*gx + t) * np.sin(3*gy - t)

    return (blob + wave).ravel().astype(np.float32)

def make_colors(vals):
    v = (vals - vals.min()) / (vals.max() - vals.min() + 1e-6)

    colors = np.zeros((len(v), 4), dtype=np.float32)
    colors[:, 0] = v
    colors[:, 1] = 0.2 * v
    colors[:, 2] = 1 - v
    colors[:, 3] = 0.15 + 0.85 * v  # ensure visibility

    return colors

vals = field_value(0)

markers = scene.visuals.Markers(
    pos=pts,
    size=4,
    face_color=make_colors(vals),
    edge_width=0,
    parent=view.scene
)

# --- Animation ---
t = 0.0

def on_timer(event):
    global t

    t += 0.03

    vals = field_value(t)

    markers.set_data(
        pos=pts,
        face_color=make_colors(vals),
        size=4
    )

    # camera motion = instant "this is alive"
    view.camera.azimuth += 0.2

    canvas.update()

timer = app.Timer(1/60, connect=on_timer, start=True)

if __name__ == '__main__':
    app.run()