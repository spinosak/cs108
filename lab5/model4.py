from vispy import app, scene
from vispy.visuals import transforms
import numpy as np

canvas = scene.SceneCanvas(
    title='Nebula Ribbon (Volumetric)',
    bgcolor='#000005',
    size=(1000, 700),
    show=True
)

view = canvas.central_widget.add_view()
view.camera = scene.TurntableCamera(fov=45, distance=6, elevation=25)

# -----------------------------
# Base parametric curve
# -----------------------------
n = 4000
t = np.linspace(0, 2 * np.pi, n)

# A, B, C
a = 2 
b = 3
c = 7

base = np.column_stack([
    np.sin(a * t + np.pi/4),
    np.sin(b * t),
    np.sin(c * t)
]).astype(np.float32)

# -----------------------------
# Ribbon object (line strip)
# -----------------------------
line = scene.visuals.Line(
    base,
    color=(0.4, 0.6, 1.0, 0.0),  # we will override via colors
    width=2,
    method='gl',
    parent=view.scene
)

# -----------------------------
# Color field (nebula gradient)
# -----------------------------
c = (np.sin(t) + 1) / 2
colors = np.zeros((n, 4), dtype=np.float32)
colors[:, 0] = c**2.5
colors[:, 1] = 0.3 + 0.4 * (1 - c)
colors[:, 2] = 0.8 + 0.2 * c
colors[:, 3] = 0.9

line.set_data(pos=base, color=colors)

# -----------------------------
# Secondary fog layer (points)
# -----------------------------
fog_n = 6000
fog = np.random.randn(fog_n, 3).astype(np.float32) * 1.5

fog_colors = np.zeros((fog_n, 4), dtype=np.float32)
fog_colors[:, 2] = 1.0
fog_colors[:, 3] = 0.03  # very faint fog

fog_markers = scene.visuals.Markers(
    pos=fog,
    size=2,
    face_color=fog_colors,
    edge_width=0,
    parent=view.scene
)

fog_markers.set_gl_state(
    'translucent',
    blend=True,
    depth_test=False
)

# -----------------------------
# Motion state
# -----------------------------
phase = 0.0

def deform(t, phase):
    warp = 0.25 * np.sin(6 * t + phase)

    pts = np.empty_like(base)
    pts[:, 0] = base[:, 0] + warp * np.cos(3 * t + phase)
    pts[:, 1] = base[:, 1] + warp * np.sin(2 * t - phase)
    pts[:, 2] = base[:, 2] + warp * np.sin(4 * t + phase * 0.5)

    return pts

# -----------------------------
# Animation loop
# -----------------------------
def on_timer(event):
    global phase

    phase += 0.02

    pts = deform(t, phase)

    # -------------------------
    # Ribbon glow dynamics
    # -------------------------
    pulse = 0.6 + 0.4 * np.sin(phase * 2.0)

    glow = colors.copy()
    glow[:, 3] = 0.3 + 0.7 * pulse  # alpha pulse

    line.set_data(pos=pts, color=glow, width=2 + 2 * pulse)

    # -------------------------
    # Fog drift (slow motion field)
    # -------------------------
    fog[:, 0] += 0.001 * np.sin(phase)
    fog[:, 1] += 0.001 * np.cos(phase * 0.7)
    fog[:, 2] += 0.001 * np.sin(phase * 0.3)

    fog_markers.set_data(pos=fog, face_color=fog_colors)

    # -------------------------
    # Camera motion (depth cue)
    # -------------------------
    view.camera.azimuth += 0.15
    view.camera.elevation = 25 + 8 * np.sin(phase * 0.3)

    canvas.update()

timer = app.Timer(1/60, connect=on_timer, start=True)

if __name__ == '__main__':
    # IMPORTANT: enable additive glow blending
    line.set_gl_state('translucent', blend=True, depth_test=False)

    app.run()