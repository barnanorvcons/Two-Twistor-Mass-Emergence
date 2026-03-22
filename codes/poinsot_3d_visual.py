"""
Poinsot ellipsoid 3D visualization
Shows deformation at three critical angles: 63.43°, 45°, 30°
Plus the polhode curves (energy ellipsoid ∩ momentum sphere)

Szoke Barna — March 2026
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

m = 1.0

def cone_params(theta_deg):
    """Get cone geometry and inertia at given half-angle"""
    theta = np.radians(theta_deg)
    tan_t = np.tan(theta)
    h = tan_t**(-2.0/3.0)
    r = tan_t**(1.0/3.0)
    I3 = (3.0/10.0) * m * r**2
    I1 = (3.0/20.0) * m * (r**2 + 4*h**2)
    I2 = I1
    return h, r, I1, I2, I3

def make_ellipsoid(I1, I2, I3, L=1.0):
    """Generate ellipsoid surface points
    Energy ellipsoid: I1*w1^2 + I2*w2^2 + I3*w3^2 = 2T
    where T = L^2/(2*I3)"""
    T = L**2 / (2 * I3)
    a1 = np.sqrt(2*T / I1)
    a2 = np.sqrt(2*T / I2)
    a3 = np.sqrt(2*T / I3)

    u = np.linspace(0, 2*np.pi, 80)
    v = np.linspace(0, np.pi, 60)
    U, V = np.meshgrid(u, v)

    x = a1 * np.sin(V) * np.cos(U)
    y = a2 * np.sin(V) * np.sin(U)
    z = a3 * np.cos(V)

    return x, y, z, a1, a2, a3, T

def make_momentum_sphere(I1, I2, I3, L=1.0):
    """Angular momentum sphere: I1^2*w1^2 + I2^2*w2^2 + I3^2*w3^2 = L^2"""
    u = np.linspace(0, 2*np.pi, 80)
    v = np.linspace(0, np.pi, 60)
    U, V = np.meshgrid(u, v)

    x = (L/I1) * np.sin(V) * np.cos(U)
    y = (L/I2) * np.sin(V) * np.sin(U)
    z = (L/I3) * np.cos(V)

    return x, y, z

def compute_polhode(I1, I2, I3, L=1.0, npts=500):
    """Compute polhode: intersection of energy ellipsoid and momentum ellipsoid
    Parametrize by angle around spin axis"""
    T = L**2 / (2*I3)

    # For symmetric top (I1=I2), polhode is a circle
    # w3 is fixed by energy: w3 = L/I3
    # w1^2 + w2^2 is fixed by the energy-momentum constraint

    w3 = L / I3
    # From energy: I1*w1^2 + I1*w2^2 + I3*w3^2 = 2T
    # I1*(w1^2+w2^2) = 2T - I3*w3^2 = L^2/I3 - L^2/I3 = 0 at exact spin
    # But for polhode we want the NEARBY trajectories
    # Perturb: let energy be slightly different

    # Better: show polhode for different energy levels
    polhodes = []
    for dE_frac in [0.01, 0.05, 0.1, 0.2, 0.3]:
        T_pert = T * (1 + dE_frac)
        # I1*(w1^2+w2^2) = 2*T_pert - I3*w3_new^2
        # I1^2*(w1^2+w2^2) + I3^2*w3_new^2 = L^2
        # From second: w3_new^2 = (L^2 - I1^2*(w1^2+w2^2)) / I3^2
        # Sub into first: I1*(w1^2+w2^2) + I3*(L^2 - I1^2*(w1^2+w2^2))/I3^2 = 2*T_pert
        # I1*R^2 + L^2/I3 - I1^2*R^2/I3 = 2*T_pert  where R^2 = w1^2+w2^2
        # R^2 * (I1 - I1^2/I3) = 2*T_pert - L^2/I3
        # R^2 * I1*(1 - I1/I3) = 2*T_pert - L^2/I3
        # R^2 * I1*(I3-I1)/I3 = 2*T_pert - L^2/I3

        denom = I1[0] if hasattr(I1, '__len__') else I1
        I3_val = I3[0] if hasattr(I3, '__len__') else I3
        I1_val = I1[0] if hasattr(I1, '__len__') else I1

        rhs = 2*T_pert - L**2/I3_val
        lhs_coeff = I1_val * (I3_val - I1_val) / I3_val

        if abs(lhs_coeff) < 1e-12 or rhs/lhs_coeff < 0:
            continue

        R2 = rhs / lhs_coeff
        if R2 < 0:
            continue
        R = np.sqrt(R2)

        w3_val = np.sqrt((L**2 - I1_val**2 * R2) / I3_val**2)
        if np.isnan(w3_val):
            continue

        phi = np.linspace(0, 2*np.pi, npts)
        w1 = R * np.cos(phi)
        w2 = R * np.sin(phi)
        w3_arr = np.full_like(phi, w3_val)

        polhodes.append((w1, w2, w3_arr))

    return polhodes

# === Three critical angles ===
angles = [63.43, 45.0, 30.0]
titles = ['63.43 (I1=I3, sphere)\nNo precession',
          '45 (contact)\nProlate, strong precession',
          '30 (equilateral triangle)\nExtremely prolate']
colors_ell = ['#2196F3', '#FF9800', '#F44336']
colors_sph = ['#81D4FA', '#FFE0B2', '#EF9A9A']

# === MAIN FIGURE: 3 ellipsoids side by side ===
fig = plt.figure(figsize=(20, 14))

for i, (angle, title, col_e, col_s) in enumerate(zip(angles, titles, colors_ell, colors_sph)):
    h, r, I1, I2, I3 = cone_params(angle)

    # Energy ellipsoid
    xe, ye, ze, a1, a2, a3, T = make_ellipsoid(I1, I2, I3)

    # Momentum sphere
    xm, ym, zm = make_momentum_sphere(I1, I2, I3)

    # Top row: energy ellipsoid
    ax = fig.add_subplot(2, 3, i+1, projection='3d')
    ax.plot_surface(xe, ye, ze, alpha=0.4, color=col_e, edgecolor='none')
    ax.plot_wireframe(xe, ye, ze, alpha=0.1, color='black', rstride=8, cstride=8)

    # Draw axes
    maxval = max(a1, a3) * 1.3
    ax.plot([-maxval, maxval], [0, 0], [0, 0], 'k-', alpha=0.2, linewidth=0.5)
    ax.plot([0, 0], [-maxval, maxval], [0, 0], 'k-', alpha=0.2, linewidth=0.5)
    ax.plot([0, 0], [0, 0], [-maxval, maxval], 'k-', alpha=0.2, linewidth=0.5)

    # Spin axis indicator
    ax.plot([0, 0], [0, 0], [0, a3*1.2], 'r-', linewidth=2, alpha=0.8)

    ax.set_title(f'theta = {title}', fontsize=10, fontweight='bold')
    ax.set_xlabel('w1')
    ax.set_ylabel('w2')
    ax.set_zlabel('w3 (spin)')

    # Equal aspect
    ax.set_xlim(-maxval, maxval)
    ax.set_ylim(-maxval, maxval)
    ax.set_zlim(-maxval, maxval)

    # Add text with semi-axes
    ratio = I1/I3
    ax.text2D(0.02, 0.95, f'a_eq = {a1:.3f}\na_pol = {a3:.3f}\nI1/I3 = {ratio:.3f}',
              transform=ax.transAxes, fontsize=8, verticalalignment='top',
              bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # Bottom row: cross-section (w1-w3 plane) showing ellipsoid + momentum sphere
    ax2 = fig.add_subplot(2, 3, i+4)

    # Ellipsoid cross-section (ellipse in w1-w3 plane)
    phi = np.linspace(0, 2*np.pi, 200)
    ew1 = a1 * np.cos(phi)
    ew3 = a3 * np.sin(phi)
    ax2.plot(ew1, ew3, '-', color=col_e, linewidth=2.5, label='Energy ellipsoid')
    ax2.fill(ew1, ew3, color=col_e, alpha=0.15)

    # Momentum sphere cross-section (ellipse with semi-axes L/I1, L/I3)
    mw1 = (1.0/I1) * np.cos(phi)
    mw3 = (1.0/I3) * np.sin(phi)
    ax2.plot(mw1, mw3, '--', color='black', linewidth=1.5, label='L sphere')

    # Mark spin point (0, L/I3)
    ax2.plot(0, 1.0/I3, 'ro', markersize=8, zorder=5)
    ax2.annotate('spin', (0, 1.0/I3), textcoords="offset points",
                xytext=(10, 5), fontsize=8, color='red')

    # Mark intersections (polhode points in this plane)
    # Solve: w1^2/a1^2 + w3^2/a3^2 = 1 AND I1^2*w1^2 + I3^2*w3^2 = 1
    # w1^2*(1/a1^2 - I1^2*a3^2/(a3^2)) ... parametric

    ax2.set_xlabel('w1 (perpendicular)')
    ax2.set_ylabel('w3 (spin axis)')
    ax2.set_title(f'Cross-section at theta = {angle}', fontsize=10)
    ax2.set_aspect('equal')
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)

    maxv2 = max(max(np.abs(ew1)), max(np.abs(ew3)), max(np.abs(mw1)), max(np.abs(mw3))) * 1.2
    ax2.set_xlim(-maxv2, maxv2)
    ax2.set_ylim(-maxv2, maxv2)

plt.suptitle('Poinsot Ellipsoid Deformation: 63.43 -> 45 -> 30 degrees\n'
             'Sphere -> Prolate -> Extremely prolate',
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('C:/Users/szoke/two-twistor-mass-emergence/visuals/poinsot_3d.png',
            dpi=150, bbox_inches='tight')
print("Saved to visuals/poinsot_3d.png")

# === SECOND FIGURE: Cone cross-sections at critical angles ===
fig2, axes2 = plt.subplots(1, 3, figsize=(18, 6))

for i, (angle, col) in enumerate(zip(angles, colors_ell)):
    ax = axes2[i]
    h, r, I1, I2, I3 = cone_params(angle)

    # Draw cone cross-section (isosceles triangle)
    triangle_x = [-r, 0, r, -r]
    triangle_y = [0, h, 0, 0]
    ax.plot(triangle_x, triangle_y, '-', color=col, linewidth=2.5)
    ax.fill(triangle_x, triangle_y, color=col, alpha=0.15)

    # Draw the internal equilateral triangle reference
    # Equilateral with base 2r: height = r*sqrt(3)
    eq_h = r * np.sqrt(3)
    ax.plot([-r, 0, r, -r], [0, eq_h, 0, 0], '--', color='gray',
            linewidth=1, alpha=0.5, label='equilateral ref')

    # Mark dimensions
    ax.annotate(f'r = {r:.3f}', xy=(r/2, -0.05), fontsize=9, ha='center')
    ax.annotate(f'h = {h:.3f}', xy=(0.05, h/2), fontsize=9, rotation=90)

    # Angle arc
    arc_r = 0.15
    arc_theta = np.linspace(np.pi/2, np.pi/2 + np.arctan(r/h), 30)
    arc_x = arc_r * np.cos(arc_theta)
    arc_y = h + arc_r * np.sin(arc_theta) - arc_r

    slant = np.sqrt(h**2 + r**2)

    ax.set_title(f'theta = {angle} | h/r = {h/r:.3f} | slant = {slant:.3f}',
                fontsize=10, fontweight='bold')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.2)
    ax.legend(fontsize=8)

plt.suptitle('Cone cross-sections at critical angles (V = const)',
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('C:/Users/szoke/two-twistor-mass-emergence/visuals/cone_cross_sections.png',
            dpi=150, bbox_inches='tight')
print("Saved to visuals/cone_cross_sections.png")
