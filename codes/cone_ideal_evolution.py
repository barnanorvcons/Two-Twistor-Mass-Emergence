"""
Ideal cone evolution: single cone, internal contra-rotation
Homogeneous density, V = const, L = const
Computes theta(t) evolution from 90° downward
and the Poinsot ellipsoid stability

Szoke Barna — March 2026
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# === CONE GEOMETRY ===
# Half-angle theta, height h, radius r = h * tan(theta)
# Volume V = (pi/3) * r^2 * h = (pi/3) * h^3 * tan^2(theta)

# Moments of inertia for homogeneous cone (mass m, radius r, height h):
# I3 (symmetry axis) = (3/10) * m * r^2
# I1 = I2 (perpendicular) = (3/20) * m * (r^2 + 4*h^2)

# No-precession condition: I1 = I3
# (3/20)(r^2 + 4h^2) = (3/10)r^2
# r^2 + 4h^2 = 2r^2
# r = 2h => tan(theta) = 2 => theta = arctan(2) = 63.43°

theta_eq = np.degrees(np.arctan(2))
print(f"=== IDEAL CONE EVOLUTION ===\n")
print(f"No-precession equilibrium angle: {theta_eq:.4f}°")
print(f"  tan(theta) = 2")
print(f"  This is arctan(2) = {theta_eq:.4f}°\n")

# === EVOLUTION: theta from 90° to equilibrium ===
# V = const => h^3 * tan^2(theta) = const = C
# At theta=90 this diverges, so start near 90

# Let's parametrize by theta and compute h(theta) from V = const
# Fix V = pi/3 (normalized), m = 1

V0 = np.pi / 3  # normalized volume
m = 1.0

# theta range (avoiding exactly 90 where tan diverges)
thetas_deg = np.linspace(89, 30, 1000)
thetas = np.radians(thetas_deg)

# h from V = (pi/3) h^3 tan^2(theta) = V0
# h^3 = V0 / ((pi/3) * tan^2(theta)) = 1 / tan^2(theta)
# h = tan(theta)^(-2/3)

h = np.tan(thetas)**(-2.0/3.0)
r = h * np.tan(thetas)  # = h * tan(theta) = tan(theta)^(1/3)

# Moments of inertia
I3 = (3.0/10.0) * m * r**2
I1 = (3.0/20.0) * m * (r**2 + 4*h**2)

# Ratio I1/I3 — when this = 1, no precession
ratio = I1 / I3

# Precession angular velocity (when I1 != I3):
# omega_p = omega_spin * (I3 - I1) / I1  (for symmetric top)
# Normalized precession rate:
precession_rate = (I3 - I1) / I1

# Energy in rotation (L = const = 1)
# T = L^2 / (2*I3) for spin about symmetry axis
L = 1.0
T_spin = L**2 / (2 * I3)

# Poinsot ellipsoid semi-axes: a_i = sqrt(2T / I_i)
# For the energy ellipsoid
a3 = np.sqrt(2 * T_spin / I3)  # along spin axis
a1 = np.sqrt(2 * T_spin / I1)  # perpendicular

print(f"=== KEY VALUES ===\n")
for angle in [90, 80, 70, 63.43, 60, 45, 30]:
    idx = np.argmin(np.abs(thetas_deg - angle))
    th = thetas_deg[idx]
    print(f"  theta = {th:6.2f}°: h = {h[idx]:.4f}, r = {r[idx]:.4f}, "
          f"I1/I3 = {ratio[idx]:.4f}, precession = {precession_rate[idx]:+.4f}")

print(f"\n=== CRITICAL POINT ===")
# Find where I1 = I3
cross_idx = np.argmin(np.abs(ratio - 1.0))
print(f"  I1 = I3 at theta = {thetas_deg[cross_idx]:.2f}°")
print(f"  This is arctan(2) = {theta_eq:.2f}°")

print(f"\n=== INTERPRETATION ===")
print(f"  theta > 63.43°: I1 > I3 (oblate), precession in one direction")
print(f"  theta < 63.43°: I1 < I3 (prolate), precession reverses")
print(f"  theta = 63.43°: I1 = I3 (spherical top), NO precession")
print(f"  theta = 45°: contact angle (cone half-angle = 45°)")
print(f"")
print(f"  The window 63.43° to 45° is where the event MUST occur:")
print(f"  the system crosses from oblate to prolate,")
print(f"  precession reverses, and stabilization requires symmetry breaking.")

# === PLOTS ===
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Ideal Cone Evolution — Homogeneous ρ, V=const, L=const',
             fontsize=14, fontweight='bold')

# Plot 1: I1/I3 ratio vs theta
ax = axes[0, 0]
ax.plot(thetas_deg, ratio, 'b-', linewidth=2)
ax.axhline(y=1.0, color='r', linestyle='--', alpha=0.7, label='I₁ = I₃ (no precession)')
ax.axvline(x=theta_eq, color='g', linestyle='--', alpha=0.7, label=f'θ = {theta_eq:.1f}°')
ax.axvline(x=45, color='orange', linestyle='--', alpha=0.7, label='θ = 45° (contact)')
ax.set_xlabel('Half-angle θ (degrees)')
ax.set_ylabel('I₁ / I₃')
ax.set_title('Inertia ratio: oblate ↔ prolate transition')
ax.legend(fontsize=9)
ax.set_xlim(30, 89)
ax.grid(True, alpha=0.3)

# Plot 2: Precession rate vs theta
ax = axes[0, 1]
ax.plot(thetas_deg, precession_rate, 'purple', linewidth=2)
ax.axhline(y=0, color='r', linestyle='--', alpha=0.7)
ax.axvline(x=theta_eq, color='g', linestyle='--', alpha=0.7, label=f'θ = {theta_eq:.1f}°')
ax.axvline(x=45, color='orange', linestyle='--', alpha=0.7, label='θ = 45° (contact)')
ax.fill_between(thetas_deg, precession_rate, 0,
                where=(thetas_deg <= theta_eq) & (thetas_deg >= 45),
                alpha=0.2, color='red', label='EVENT WINDOW')
ax.set_xlabel('Half-angle θ (degrees)')
ax.set_ylabel('(I₃ − I₁) / I₁')
ax.set_title('Precession rate (sign = direction)')
ax.legend(fontsize=9)
ax.set_xlim(30, 89)
ax.grid(True, alpha=0.3)

# Plot 3: Geometry h, r vs theta
ax = axes[1, 0]
ax.plot(thetas_deg, h, 'b-', linewidth=2, label='h (height)')
ax.plot(thetas_deg, r, 'r-', linewidth=2, label='r (radius)')
ax.axvline(x=theta_eq, color='g', linestyle='--', alpha=0.7, label=f'θ = {theta_eq:.1f}°')
ax.axvline(x=45, color='orange', linestyle='--', alpha=0.7, label='θ = 45° (contact)')
ax.set_xlabel('Half-angle θ (degrees)')
ax.set_ylabel('Normalized length')
ax.set_title('Cone dimensions at constant volume')
ax.legend(fontsize=9)
ax.set_xlim(30, 89)
ax.grid(True, alpha=0.3)

# Plot 4: Poinsot ellipsoid eccentricity
ax = axes[1, 1]
eccentricity = (a1 - a3) / (a1 + a3)
ax.plot(thetas_deg, eccentricity, 'darkred', linewidth=2)
ax.axhline(y=0, color='r', linestyle='--', alpha=0.7, label='Sphere (no precession)')
ax.axvline(x=theta_eq, color='g', linestyle='--', alpha=0.7, label=f'θ = {theta_eq:.1f}°')
ax.axvline(x=45, color='orange', linestyle='--', alpha=0.7, label='θ = 45° (contact)')
ax.set_xlabel('Half-angle θ (degrees)')
ax.set_ylabel('Ellipsoid eccentricity')
ax.set_title('Poinsot ellipsoid deformation')
ax.legend(fontsize=9)
ax.set_xlim(30, 89)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('C:/Users/szoke/two-twistor-mass-emergence/visuals/cone_ideal_evolution.png',
            dpi=150, bbox_inches='tight')
print(f"\nPlot saved to visuals/cone_ideal_evolution.png")
