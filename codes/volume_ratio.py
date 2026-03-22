"""
Volume ratio: Poinsot ellipsoid vs cone
as function of theta

Szoke Barna — March 2026
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

m = 1.0
L = 1.0

thetas_deg = np.linspace(88, 25, 2000)
thetas = np.radians(thetas_deg)
tan_t = np.tan(thetas)

h = tan_t**(-2.0/3.0)
r = tan_t**(1.0/3.0)

# Cone volume (constant by construction)
V_cone = (np.pi/3) * r**2 * h

# Moments of inertia
I3 = (3.0/10.0) * m * r**2
I1 = (3.0/20.0) * m * (r**2 + 4*h**2)

# Rotational energy
T = L**2 / (2 * I3)

# Poinsot ellipsoid semi-axes
a1 = np.sqrt(2*T / I1)
a2 = a1  # symmetric
a3 = np.sqrt(2*T / I3)

# Ellipsoid volume
V_ell = (4.0/3.0) * np.pi * a1 * a2 * a3

# Ratio
ratio = V_ell / V_cone

# Surface areas
# Cone lateral surface
S_cone = np.pi * r * np.sqrt(r**2 + h**2) + np.pi * r**2  # lateral + base

# Ellipsoid surface (spheroid approximation)
S_ell = np.zeros_like(thetas_deg)
for i in range(len(thetas_deg)):
    a_eq = a1[i]
    c_pol = a3[i]
    if abs(a_eq - c_pol) < 1e-10:
        S_ell[i] = 4 * np.pi * a_eq**2
    elif a_eq > c_pol:
        e = np.sqrt(1 - c_pol**2 / a_eq**2)
        S_ell[i] = 2*np.pi*a_eq**2 * (1 + (1-e**2)/e * np.arctanh(e))
    else:
        e = np.sqrt(1 - a_eq**2 / c_pol**2)
        S_ell[i] = 2*np.pi*a_eq**2 * (1 + c_pol/(a_eq*e) * np.arcsin(e))

S_ratio = S_ell / S_cone

# S/V ratios
SV_cone = S_cone / V_cone
SV_ell = S_ell / V_ell
SV_ratio = SV_ell / SV_cone

print("=" * 70)
print("VOLUME & SURFACE RATIOS: POINSOT ELLIPSOID vs CONE")
print("=" * 70)

print(f"\n{'theta':>8} {'V_cone':>10} {'V_ell':>10} {'V_ell/V_c':>10} "
      f"{'S_cone':>10} {'S_ell':>10} {'S_ell/S_c':>10} {'SV_e/SV_c':>10}")
print("-" * 85)

for angle in [88, 80, 70, 63.43, 60, 55, 50, 45, 40, 35, 30]:
    idx = np.argmin(np.abs(thetas_deg - angle))
    print(f"{thetas_deg[idx]:8.2f} {V_cone[idx]:10.4f} {V_ell[idx]:10.4f} "
          f"{ratio[idx]:10.4f} {S_cone[idx]:10.4f} {S_ell[idx]:10.4f} "
          f"{S_ratio[idx]:10.4f} {SV_ratio[idx]:10.4f}")

# Find where V_ell = V_cone
cross_v = np.argmin(np.abs(ratio - 1.0))
print(f"\n  V_ell = V_cone at theta = {thetas_deg[cross_v]:.2f}")

# Find where S_ell = S_cone
cross_s = np.argmin(np.abs(S_ratio - 1.0))
print(f"  S_ell = S_cone at theta = {thetas_deg[cross_s]:.2f}")

# Find where SV_ell = SV_cone
cross_sv = np.argmin(np.abs(SV_ratio - 1.0))
print(f"  (S/V)_ell = (S/V)_cone at theta = {thetas_deg[cross_sv]:.2f}")

# Key ratios at critical angles
print(f"\n{'=' * 70}")
print("KEY RATIOS AT CRITICAL ANGLES:")
for angle in [63.43, 45.0, 30.0]:
    idx = np.argmin(np.abs(thetas_deg - angle))
    print(f"\n  theta = {angle}:")
    print(f"    V_ell/V_cone = {ratio[idx]:.6f}")
    print(f"    S_ell/S_cone = {S_ratio[idx]:.6f}")
    print(f"    (S/V)_ell / (S/V)_cone = {SV_ratio[idx]:.6f}")
    print(f"    V_ell = {V_ell[idx]:.6f}")
    print(f"    V_cone = {V_cone[idx]:.6f}")

# === PLOTS ===
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Poinsot Ellipsoid vs Cone: Volume and Surface Ratios',
             fontsize=14, fontweight='bold')

def add_lines(ax):
    ax.axvline(x=63.43, color='green', linestyle='--', alpha=0.6, linewidth=1)
    ax.axvline(x=45, color='orange', linestyle='--', alpha=0.6, linewidth=1)
    ax.axvline(x=30, color='red', linestyle='--', alpha=0.6, linewidth=1)

# 1. Volumes
ax = axes[0, 0]
ax.plot(thetas_deg, V_cone, 'b-', linewidth=2, label='V_cone (const)')
ax.plot(thetas_deg, V_ell, 'r-', linewidth=2, label='V_ellipsoid')
add_lines(ax)
ax.set_xlabel('theta (degrees)')
ax.set_ylabel('Volume')
ax.set_title('Volumes')
ax.legend()
ax.grid(True, alpha=0.3)

# 2. Volume ratio
ax = axes[0, 1]
ax.plot(thetas_deg, ratio, 'purple', linewidth=2)
ax.axhline(y=1.0, color='black', linestyle=':', alpha=0.5, label='V_ell = V_cone')
add_lines(ax)
ax.set_xlabel('theta (degrees)')
ax.set_ylabel('V_ellipsoid / V_cone')
ax.set_title('Volume ratio')
ax.legend()
ax.grid(True, alpha=0.3)

# 3. Surface ratio
ax = axes[1, 0]
ax.plot(thetas_deg, S_ratio, 'darkred', linewidth=2)
ax.axhline(y=1.0, color='black', linestyle=':', alpha=0.5, label='S_ell = S_cone')
add_lines(ax)
ax.set_xlabel('theta (degrees)')
ax.set_ylabel('S_ellipsoid / S_cone')
ax.set_title('Surface ratio')
ax.legend()
ax.grid(True, alpha=0.3)

# 4. S/V ratio comparison
ax = axes[1, 1]
ax.plot(thetas_deg, SV_cone, 'b-', linewidth=2, label='(S/V)_cone')
ax.plot(thetas_deg, SV_ell, 'r-', linewidth=2, label='(S/V)_ellipsoid')
add_lines(ax)
ax.set_xlabel('theta (degrees)')
ax.set_ylabel('S/V')
ax.set_title('Surface/Volume ratios')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('C:/Users/szoke/two-twistor-mass-emergence/visuals/volume_ratio.png',
            dpi=150, bbox_inches='tight')
print(f"\nPlot saved to visuals/volume_ratio.png")
