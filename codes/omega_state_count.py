"""
Omega(theta) — number of microstates for a cone
as function of half-angle theta

N(theta) = number of modes (Bessel modes that fit in cone)
E(theta) = total energy in mode units (from I3, L=const)

Omega = C(N+E-1, E) = (N+E-1)! / (E! * (N-1)!)
P(sync) = 1/Omega

Pure geometry — no physics parameters injected.

Szoke Barna — March 2026
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.special import gammaln

# === CONE GEOMETRY (same as before, normalized) ===
m = 1.0
thetas_deg = np.linspace(88, 25, 2000)
thetas = np.radians(thetas_deg)
tan_t = np.tan(thetas)

h = tan_t**(-2.0/3.0)
r = tan_t**(1.0/3.0)

# Moments of inertia
I3 = (3.0/10.0) * m * r**2
I1 = (3.0/20.0) * m * (r**2 + 4*h**2)

# === N(theta): number of modes ===
# Modes on a cone: Bessel zeros that fit within the geometry
# For a cone of height h and radius r, the number of modes
# scales as the area of the phi-circle cross-section
# N ~ pi * r * h (lateral surface area, normalized)
# This is the "phase space volume" available to modes

N_modes = np.pi * r * h  # normalized mode count

# Also: N from volume-based counting
# N_vol ~ V^(2/3) for 3D
# But let's use the surface-based one (modes live on the boundary)

# === E(theta): energy in mode units ===
# L = 1 (const), T = L^2/(2*I3)
L = 1.0
T = L**2 / (2 * I3)

# Energy in units of the lowest mode spacing
# Lowest mode ~ 1/h^2 (particle in box)
E_lowest = 1.0 / h**2
E_units = T / E_lowest  # how many mode-quanta fit

# === Omega(theta) ===
# Omega = C(N+E-1, E)
# ln(Omega) = ln((N+E-1)!) - ln(E!) - ln((N-1)!)
# Use gammaln for numerical stability

# Round to integers for combinatorial calculation
N_int = np.maximum(np.round(N_modes).astype(int), 2)
E_int = np.maximum(np.round(E_units).astype(int), 1)

ln_Omega = (gammaln(N_int + E_int)
            - gammaln(E_int + 1)
            - gammaln(N_int))

# Entropy S = ln(Omega)
S = ln_Omega

# P(sync) = 1/Omega = exp(-S)
# ln(P) = -S

# === CRITICAL ANGLES ===
theta_noprecession = np.degrees(np.arctan(2))  # 63.43
theta_contact = 45.0
theta_equilateral = 30.0

print("=" * 70)
print("OMEGA(theta) -- MICROSTATE COUNT")
print("=" * 70)

print(f"\n{'theta':>8} {'N_modes':>10} {'E_units':>10} {'ln(Omega)':>12} {'S/kB':>10} {'ln(P_sync)':>12}")
print("-" * 70)

for angle in [88, 80, 70, 63.43, 60, 55, 50, 45, 40, 35, 30]:
    idx = np.argmin(np.abs(thetas_deg - angle))
    print(f"{thetas_deg[idx]:8.2f} {N_modes[idx]:10.2f} {E_units[idx]:10.2f} "
          f"{ln_Omega[idx]:12.2f} {S[idx]:10.2f} {-ln_Omega[idx]:12.2f}")

print(f"\n{'=' * 70}")
print("CRITICAL POINTS:")

idx_63 = np.argmin(np.abs(thetas_deg - 63.43))
idx_45 = np.argmin(np.abs(thetas_deg - 45.0))
idx_30 = np.argmin(np.abs(thetas_deg - 30.0))

print(f"\n  63.43 -> 45 transition:")
print(f"    Delta S = {S[idx_45] - S[idx_63]:.4f}")
print(f"    Omega(45)/Omega(63.43) = exp({ln_Omega[idx_45] - ln_Omega[idx_63]:.2f})")

print(f"\n  45 -> 30 transition:")
print(f"    Delta S = {S[idx_30] - S[idx_45]:.4f}")
print(f"    Omega(30)/Omega(45) = exp({ln_Omega[idx_30] - ln_Omega[idx_45]:.2f})")

print(f"\n  63.43 -> 30 total:")
print(f"    Delta S = {S[idx_30] - S[idx_63]:.4f}")
print(f"    Omega(30)/Omega(63.43) = exp({ln_Omega[idx_30] - ln_Omega[idx_63]:.2f})")

# === FIND EXTREMA ===
dS = np.gradient(S, thetas_deg)
d2S = np.gradient(dS, thetas_deg)

# Find where dS/dtheta = 0 (entropy extrema)
sign_changes = np.where(np.diff(np.sign(dS)))[0]
print(f"\n  Entropy extrema at theta = ", end="")
for sc in sign_changes:
    print(f"{thetas_deg[sc]:.2f}, ", end="")
print()

# Find S/V minimum of Omega
dSV = np.gradient(S / np.maximum(N_modes, 0.01), thetas_deg)
sv_sign_changes = np.where(np.diff(np.sign(dSV)))[0]
print(f"  S/N extrema at theta = ", end="")
for sc in sv_sign_changes:
    print(f"{thetas_deg[sc]:.2f}, ", end="")
print()

# === PLOTS ===
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Omega(theta) - Microstate Count Evolution',
             fontsize=14, fontweight='bold')

def add_lines(ax):
    ax.axvline(x=63.43, color='green', linestyle='--', alpha=0.6, label='63.43 (I1=I3)')
    ax.axvline(x=45, color='orange', linestyle='--', alpha=0.6, label='45 (contact)')
    ax.axvline(x=30, color='red', linestyle='--', alpha=0.6, label='30 (equilateral)')

# 1. N and E vs theta
ax = axes[0, 0]
ax.plot(thetas_deg, N_modes, 'b-', linewidth=2, label='N (modes)')
ax.plot(thetas_deg, E_units, 'r-', linewidth=2, label='E (energy units)')
add_lines(ax)
ax.set_xlabel('theta (degrees)')
ax.set_ylabel('Count')
ax.set_title('Mode count and energy quanta')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# 2. ln(Omega) = Entropy
ax = axes[0, 1]
ax.plot(thetas_deg, ln_Omega, 'purple', linewidth=2)
add_lines(ax)
ax.set_xlabel('theta (degrees)')
ax.set_ylabel('ln(Omega) = S')
ax.set_title('Entropy (= ln of microstate count)')
ax.grid(True, alpha=0.3)

# 3. -ln(P_sync) = how impossible is synchronization
ax = axes[1, 0]
ax.plot(thetas_deg, ln_Omega, 'darkred', linewidth=2)
add_lines(ax)
ax.set_xlabel('theta (degrees)')
ax.set_ylabel('-ln(P_sync) = ln(Omega)')
ax.set_title('Impossibility of synchronization (higher = less likely)')
ax.grid(True, alpha=0.3)

# 4. dS/dtheta — entropy production rate
ax = axes[1, 1]
ax.plot(thetas_deg, dS, 'navy', linewidth=2)
ax.axhline(y=0, color='black', linewidth=0.5)
add_lines(ax)
ax.set_xlabel('theta (degrees)')
ax.set_ylabel('dS/dtheta')
ax.set_title('Entropy rate of change')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('C:/Users/szoke/two-twistor-mass-emergence/visuals/omega_evolution.png',
            dpi=150, bbox_inches='tight')
print(f"\nPlot saved to visuals/omega_evolution.png")
