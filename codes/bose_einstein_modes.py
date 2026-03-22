"""
Bose-Einstein mode occupation on the Poinsot ellipsoid
as function of cone half-angle theta

The cone evolves from 90° -> 30°.
At each theta, the available modes have energies from the
ellipsoid geometry. BE distribution fills them.

The question: at what theta does the first mode reach
critical occupation (condensation) -> triggers the event?

Szoke Barna — March 2026
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# === CONE GEOMETRY ===
m = 1.0

def cone_at(theta_deg):
    theta = np.radians(theta_deg)
    tan_t = np.tan(theta)
    h = tan_t**(-2.0/3.0)
    r = tan_t**(1.0/3.0)
    I3 = (3.0/10.0) * m * r**2
    I1 = (3.0/20.0) * m * (r**2 + 4*h**2)
    return h, r, I1, I3

# === MODE ENERGIES ===
# Modes on the cone: standing waves along height
# E_n = n^2 * E_0 where E_0 = pi^2 / (2*m*h^2) (particle in box)
# Number of modes that fit: n_max ~ h/lambda_min ~ h * sqrt(2mE_total) / pi

def mode_spectrum(theta_deg, n_max=20):
    """Return mode energies and degeneracies at given theta"""
    h, r, I1, I3 = cone_at(theta_deg)

    # Ground state energy (normalized)
    E0 = np.pi**2 / (2 * m * h**2)

    # Mode energies: E_n = n^2 * E0 for 1D
    # But on a cone, modes also have angular part
    # E_{n,l} = E0 * (n^2 + l^2 * h^2/r^2) where l = angular mode
    # Degeneracy of level with energy E: g(E) ~ sqrt(E) in 3D

    # For now: 1D modes along axis + angular quantization
    modes = []
    for n in range(1, n_max + 1):
        for l in range(0, n + 1):  # angular modes up to n
            E_nl = E0 * (n**2 + l**2 * h**2 / r**2)
            g = 2 * l + 1 if l > 0 else 1  # degeneracy
            modes.append((n, l, E_nl, g))

    return modes, E0

def bose_einstein(modes, T_eff, mu=0):
    """BE occupation for each mode at effective temperature T_eff
    n_BE = g / (exp((E - mu)/T) - 1)
    mu <= E_min (chemical potential)"""
    occupations = []
    for n, l, E, g in modes:
        x = (E - mu) / T_eff
        if x > 100:
            occ = 0
        elif x < 1e-6:
            occ = g * T_eff / (E - mu) if E > mu else float('inf')
        else:
            occ = g / (np.exp(x) - 1)
        occupations.append((n, l, E, g, occ))
    return occupations

# === EVOLUTION: theta as "time", T_eff from rotational energy ===
thetas = np.linspace(85, 28, 200)

# Track key quantities
ground_occ = []       # ground state occupation
total_particles = []  # total occupation number
max_occ = []          # maximum occupation in any mode
condensate_frac = []  # ground state / total
entropy_arr = []      # entropy from BE
critical_theta = None

print("=" * 70)
print("BOSE-EINSTEIN MODE OCCUPATION ON POINSOT ELLIPSOID")
print("=" * 70)

print(f"\n{'theta':>8} {'T_eff':>10} {'N_total':>10} {'n_ground':>10} "
      f"{'n_max':>10} {'cond_frac':>10} {'S_BE':>10}")
print("-" * 75)

for theta in thetas:
    h, r, I1, I3 = cone_at(theta)
    T_rot = 1.0 / (2 * I3)  # rotational energy (L=1)

    # Effective temperature from rotational energy
    # T_eff decreases as theta decreases (I3 increases, energy decreases)
    T_eff = T_rot

    modes, E0 = mode_spectrum(theta, n_max=15)

    # Chemical potential: just below ground state energy
    E_min = min(E for _, _, E, _ in modes)
    mu = E_min * 0.999  # just below

    occ = bose_einstein(modes, T_eff, mu)

    # Ground state (n=1, l=0)
    n_ground = occ[0][4]
    n_total = sum(o[4] for o in occ if not np.isinf(o[4]))
    n_max_val = max(o[4] for o in occ if not np.isinf(o[4]))

    if n_total > 0:
        cf = n_ground / n_total
    else:
        cf = 0

    # BE entropy: S = sum_i [(1+n_i)*ln(1+n_i) - n_i*ln(n_i)]
    S = 0
    for _, _, E, g, ni in occ:
        if ni > 1e-10 and not np.isinf(ni):
            S += (1 + ni) * np.log(1 + ni) - ni * np.log(ni)

    ground_occ.append(n_ground)
    total_particles.append(n_total)
    max_occ.append(n_max_val)
    condensate_frac.append(cf)
    entropy_arr.append(S)

    # Detect condensation threshold
    if cf > 0.5 and critical_theta is None:
        critical_theta = theta

    if theta in [85, 80, 70, 63.43, 60, 55, 50, 45, 40, 35, 30] or \
       abs(theta - 63.43) < 0.3 or abs(theta - 45) < 0.3 or abs(theta - 30) < 0.3:
        print(f"{theta:8.2f} {T_eff:10.4f} {n_total:10.2f} {n_ground:10.2f} "
              f"{n_max_val:10.2f} {cf:10.4f} {S:10.4f}")

print(f"\n{'=' * 70}")
if critical_theta:
    print(f"CONDENSATION THRESHOLD (ground > 50%): theta = {critical_theta:.2f}")
else:
    print("No condensation threshold found in range")

print(f"\n{'=' * 70}")
print("CRITICAL ANGLE ANALYSIS:")

for angle_name, angle_val in [("63.43 (sphere)", 63.43),
                               ("45 (contact)", 45.0),
                               ("30 (equilateral)", 30.0)]:
    idx = np.argmin(np.abs(thetas - angle_val))
    print(f"\n  At theta = {angle_name}:")
    print(f"    T_eff = {1.0/(2*cone_at(angle_val)[3]):.6f}")
    print(f"    Ground occupation = {ground_occ[idx]:.4f}")
    print(f"    Total particles = {total_particles[idx]:.4f}")
    print(f"    Condensate fraction = {condensate_frac[idx]:.4f}")
    print(f"    BE entropy = {entropy_arr[idx]:.4f}")

# === T_critical for BEC ===
# BEC occurs when T < T_c = (2*pi*hbar^2/(m*k)) * (n/zeta(3/2))^(2/3)
# In our units, T_c is when the thermal wavelength ~ inter-mode spacing
# This happens when T_eff drops below E0

print(f"\n{'=' * 70}")
print("TEMPERATURE vs GROUND STATE ENERGY:")
for angle in [85, 70, 63.43, 55, 45, 35, 30]:
    h, r, I1, I3 = cone_at(angle)
    T_eff = 1.0 / (2*I3)
    E0 = np.pi**2 / (2*m*h**2)
    print(f"  theta={angle:6.2f}: T_eff/E0 = {T_eff/E0:.4f}  "
          f"{'<< 1 COLD' if T_eff/E0 < 0.5 else '~ 1 CRITICAL' if T_eff/E0 < 2 else '>> 1 HOT'}")

# === PLOTS ===
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Bose-Einstein Condensation on the Evolving Cone',
             fontsize=14, fontweight='bold')

def add_lines(ax):
    ax.axvline(x=63.43, color='green', linestyle='--', alpha=0.6, linewidth=1)
    ax.axvline(x=45, color='orange', linestyle='--', alpha=0.6, linewidth=1)
    ax.axvline(x=30, color='red', linestyle='--', alpha=0.6, linewidth=1)

# 1. Ground state occupation
ax = axes[0, 0]
ax.plot(thetas, ground_occ, 'b-', linewidth=2)
add_lines(ax)
if critical_theta:
    ax.axvline(x=critical_theta, color='purple', linestyle='-', alpha=0.8,
               linewidth=2, label=f'BEC at {critical_theta:.1f}')
ax.set_xlabel('theta (degrees)')
ax.set_ylabel('Ground state occupation')
ax.set_title('Ground state occupation n_0')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# 2. Condensate fraction
ax = axes[0, 1]
ax.plot(thetas, condensate_frac, 'darkred', linewidth=2)
ax.axhline(y=0.5, color='purple', linestyle=':', alpha=0.5, label='50% threshold')
add_lines(ax)
ax.set_xlabel('theta (degrees)')
ax.set_ylabel('n_0 / N_total')
ax.set_title('Condensate fraction')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# 3. BE Entropy
ax = axes[1, 0]
ax.plot(thetas, entropy_arr, 'navy', linewidth=2)
add_lines(ax)
ax.set_xlabel('theta (degrees)')
ax.set_ylabel('S_BE')
ax.set_title('Bose-Einstein entropy')
ax.grid(True, alpha=0.3)

# 4. Mode spectrum at three critical angles
ax = axes[1, 1]
for angle, col, lbl in [(63.43, 'green', '63.43'),
                          (45.0, 'orange', '45'),
                          (30.0, 'red', '30')]:
    modes, E0 = mode_spectrum(angle, n_max=10)
    energies = sorted(set(E for _, _, E, _ in modes))[:15]
    h, r, I1, I3 = cone_at(angle)
    T_eff = 1.0 / (2*I3)
    be_occ = [1.0/(np.exp((E - energies[0]*0.999)/T_eff) - 1)
              if (E - energies[0]*0.999)/T_eff < 50 else 0
              for E in energies]
    ax.plot(range(len(be_occ)), be_occ, 'o-', color=col, linewidth=1.5,
            markersize=4, label=f'theta={lbl}')

ax.set_xlabel('Mode index')
ax.set_ylabel('BE occupation')
ax.set_title('Mode occupation spectrum')
ax.legend(fontsize=9)
ax.set_yscale('log')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('C:/Users/szoke/two-twistor-mass-emergence/visuals/bose_einstein_condensation.png',
            dpi=150, bbox_inches='tight')
print(f"\nPlot saved to visuals/bose_einstein_condensation.png")
