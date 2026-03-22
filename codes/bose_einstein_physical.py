"""
Bose-Einstein condensation with physical framework parameters

m0 = 246.22 GeV (Higgs VEV)
N = 1.0858e7 (quantum number scale)
A = H0*c = 6.54e-10 m/s^2
alpha = 1/137
E_cone = 250 GeV per cone

Szoke Barna — March 2026
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# === FRAMEWORK CONSTANTS ===
m0 = 246.22        # GeV, Higgs VEV
E_cone = 250.0     # GeV, full cone energy before twist
N = 1.0858e7        # quantum number scale
alpha = 1.0/137.0   # fine structure
Delta = 4*alpha**2/9  # electron gap = 2.37e-5
A = 6.54e-10        # m/s^2, acceleration

# Derived
epsilon = 1.0/N**2   # epoch parameter

print("=" * 70)
print("BOSE-EINSTEIN WITH PHYSICAL PARAMETERS")
print("=" * 70)
print(f"\n  m0 = {m0} GeV")
print(f"  E_cone = {E_cone} GeV")
print(f"  N = {N:.4e}")
print(f"  alpha = {alpha:.6f}")
print(f"  Delta = {Delta:.6e}")
print(f"  epsilon = {epsilon:.6e}")

# === CONE GEOMETRY WITH PHYSICAL ENERGY ===
# V = const, proportional to E_cone
# At each theta, the energy distributes into modes
# Mode energies: E_n = m0 * sqrt(1 - n^2 * epsilon) for n = 1..N
# This IS the mass emergence formula

# Number of available modes at each theta:
# At theta = 90: all N modes available (flat, everything precesses)
# At theta = 63.43: I1=I3, modes redistribute
# At theta = 45: contact, modes split between cones
# At theta = 30: equilateral, photon mode available

# Mode count scales with cone geometry
def N_modes(theta_deg):
    """Available modes as function of cone angle"""
    theta = np.radians(theta_deg)
    tan_t = np.tan(theta)
    h = tan_t**(-2.0/3.0)
    r = tan_t**(1.0/3.0)
    # Modes ~ lateral surface area / wavelength^2
    # Lateral surface = pi * r * sqrt(r^2 + h^2)
    lateral = np.pi * r * np.sqrt(r**2 + h**2)
    # Scale to physical N
    # At theta=90 (flat): all N modes
    # Normalize so that integral over all angles gives N
    return lateral

def T_eff(theta_deg):
    """Effective temperature from rotational energy"""
    theta = np.radians(theta_deg)
    tan_t = np.tan(theta)
    h = tan_t**(-2.0/3.0)
    r = tan_t**(1.0/3.0)
    I3 = (3.0/10.0) * r**2
    return E_cone / (2 * I3)  # in GeV

def E_ground(theta_deg):
    """Ground state energy"""
    theta = np.radians(theta_deg)
    tan_t = np.tan(theta)
    h = tan_t**(-2.0/3.0)
    # E_0 ~ 1/h^2, scaled to physical units
    return m0 * epsilon * np.pi**2 / h**2

# === MASS EMERGENCE AT EACH THETA ===
print(f"\n{'=' * 70}")
print("MASS EMERGENCE vs CONE ANGLE")
print(f"{'=' * 70}")
print(f"\n{'theta':>8} {'T_eff':>12} {'E_ground':>12} {'T/E0':>10} "
      f"{'n_crit':>10} {'m_app':>12} {'particle':>12}")
print("-" * 85)

# Known particles with their n values (relative to N)
particles = [
    ("photon",     N,           0.0),
    ("electron",   N - 0.5,     0.511e-3),
    ("muon",       N - 1.5,     105.66e-3),
    ("tau",        N - 283.5,   1.777),
    ("W",          None,        80.38),
    ("Z",          None,        91.19),
    ("Higgs",      None,        125.1),
    ("top",        None,        173.0),
]

thetas = np.linspace(85, 28, 500)
T_arr = np.array([T_eff(t) for t in thetas])
E0_arr = np.array([E_ground(t) for t in thetas])
ratio_arr = T_arr / E0_arr
N_arr = np.array([N_modes(t) for t in thetas])

for angle in [85, 75, 63.43, 55, 45, 35, 30]:
    idx = np.argmin(np.abs(thetas - angle))
    T = T_arr[idx]
    E0 = E0_arr[idx]
    rat = ratio_arr[idx]

    # Critical n: where m_app starts emerging significantly
    # m_app = m0 * sqrt(1 - n^2*eps)
    # At this temperature, modes with E < T are thermally populated
    # n_crit: where m0*sqrt(1-(n/N)^2) ~ T
    # (n/N)^2 ~ 1 - (T/m0)^2
    T_over_m0 = T / m0
    if T_over_m0 < 1:
        n_crit = N * np.sqrt(1 - T_over_m0**2)
    else:
        n_crit = 0

    m_app = m0 * np.sqrt(1 - (n_crit/N)**2) if n_crit > 0 else m0

    # Which particle is this closest to?
    closest = ""
    for name, n_p, m_p in particles:
        if abs(m_app - m_p) < m_p * 0.3 and m_p > 0:
            closest = name
            break

    print(f"{angle:8.2f} {T:12.4f} {E0:12.6f} {rat:10.4f} "
          f"{n_crit:10.0f} {m_app:12.4f} {closest:>12}")

# === BE OCCUPATION FOR PHYSICAL MODES ===
print(f"\n{'=' * 70}")
print("BOSE-EINSTEIN OCCUPATION AT CRITICAL ANGLES")
print(f"{'=' * 70}")

for angle in [63.43, 45.0, 30.0]:
    T = T_eff(angle)
    print(f"\n  theta = {angle} | T_eff = {T:.4f} GeV")
    print(f"  {'mode':>6} {'n':>12} {'m_app (GeV)':>14} {'E_mode':>12} {'BE_occ':>10}")
    print(f"  {'-'*60}")

    for name, n_p, m_p in particles:
        if n_p is None:
            continue
        m_app = m0 * np.sqrt(abs(1 - (n_p/N)**2))
        E_mode = m_app  # mode energy ~ apparent mass

        # BE occupation
        if E_mode > 0 and T > 0:
            x = E_mode / T
            if x > 100:
                be = 0
            elif x < 0.01:
                be = T / E_mode
            else:
                be = 1.0 / (np.exp(x) - 1)
        else:
            be = float('inf')

        print(f"  {name:>6} {n_p:12.1f} {m_app:14.6f} {E_mode:12.6f} {be:10.4f}")

# === THE KEY: CONDENSATION TEMPERATURE ===
print(f"\n{'=' * 70}")
print("CONDENSATION ANALYSIS")
print(f"{'=' * 70}")

# BEC temperature for our system
# T_c ~ E_0 (when thermal wavelength ~ mode spacing)
# Find theta where T_eff = E_ground

cross_idx = np.argmin(np.abs(ratio_arr - 1.0))
theta_BEC = thetas[cross_idx]
print(f"\n  T_eff = E_ground at theta = {theta_BEC:.2f}")
print(f"  T_eff at crossing = {T_arr[cross_idx]:.6f} GeV")
print(f"  E_ground at crossing = {E0_arr[cross_idx]:.6f} GeV")

# What mass emerges at BEC transition?
T_cross = T_arr[cross_idx]
if T_cross < m0:
    n_at_BEC = N * np.sqrt(1 - (T_cross/m0)**2)
    m_at_BEC = m0 * np.sqrt(1 - (n_at_BEC/N)**2)
    print(f"  n at BEC = {n_at_BEC:.0f}")
    print(f"  m_app at BEC = {m_at_BEC:.4f} GeV = {m_at_BEC*1000:.2f} MeV")

    # Compare to known particles
    print(f"\n  Comparison to known particles:")
    for name, n_p, m_p in particles:
        if m_p > 0:
            print(f"    {name:>10}: m = {m_p*1000 if m_p < 1 else m_p:.2f} "
                  f"{'MeV' if m_p < 1 else 'GeV'} | "
                  f"ratio = {m_at_BEC/m_p:.4f}")

# === ENTROPY JUMP AT EACH TRANSITION ===
print(f"\n{'=' * 70}")
print("ENTROPY STRUCTURE")
print(f"{'=' * 70}")

# S = N * ln(1 + 1/(exp(E/T)-1)) + E/(T*(exp(E/T)-1))
# Simplified: S ~ N * ln(T/E0) for T >> E0
S_arr = N_arr * np.log(np.maximum(ratio_arr, 0.001))

idx_63 = np.argmin(np.abs(thetas - 63.43))
idx_45 = np.argmin(np.abs(thetas - 45.0))
idx_30 = np.argmin(np.abs(thetas - 30.0))

print(f"\n  S(63.43) = {S_arr[idx_63]:.4f}")
print(f"  S(45)    = {S_arr[idx_45]:.4f}")
print(f"  S(30)    = {S_arr[idx_30]:.4f}")
print(f"\n  Delta S (63.43 -> 45) = {S_arr[idx_45] - S_arr[idx_63]:.4f}")
print(f"  Delta S (45 -> 30)    = {S_arr[idx_30] - S_arr[idx_45]:.4f}")
print(f"  Delta S (63.43 -> 30) = {S_arr[idx_30] - S_arr[idx_63]:.4f}")
print(f"\n  Ratio of jumps: {(S_arr[idx_45]-S_arr[idx_63])/(S_arr[idx_30]-S_arr[idx_45]):.4f}")

# === PLOTS ===
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Bose-Einstein Condensation — Physical Parameters\n'
             f'm0 = {m0} GeV, N = {N:.2e}, E_cone = {E_cone} GeV',
             fontsize=13, fontweight='bold')

def add_lines(ax):
    ax.axvline(x=63.43, color='green', linestyle='--', alpha=0.6, linewidth=1, label='63.43')
    ax.axvline(x=45, color='orange', linestyle='--', alpha=0.6, linewidth=1, label='45')
    ax.axvline(x=30, color='red', linestyle='--', alpha=0.6, linewidth=1, label='30')

# 1. T_eff and E_ground
ax = axes[0, 0]
ax.plot(thetas, T_arr, 'b-', linewidth=2, label='T_eff (GeV)')
ax.plot(thetas, E0_arr, 'r-', linewidth=2, label='E_ground (GeV)')
add_lines(ax)
ax.set_xlabel('theta (degrees)')
ax.set_ylabel('Energy (GeV)')
ax.set_title('Effective temperature vs ground state energy')
ax.legend(fontsize=8)
ax.set_yscale('log')
ax.grid(True, alpha=0.3)

# 2. T/E0 ratio
ax = axes[0, 1]
ax.plot(thetas, ratio_arr, 'purple', linewidth=2)
ax.axhline(y=1.0, color='black', linestyle=':', alpha=0.5, label='T = E0 (BEC)')
add_lines(ax)
if theta_BEC:
    ax.axvline(x=theta_BEC, color='purple', linewidth=2, alpha=0.8,
               label=f'BEC at {theta_BEC:.1f}')
ax.set_xlabel('theta (degrees)')
ax.set_ylabel('T_eff / E_ground')
ax.set_title('Condensation parameter')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# 3. Entropy
ax = axes[1, 0]
ax.plot(thetas, S_arr, 'navy', linewidth=2)
add_lines(ax)
ax.set_xlabel('theta (degrees)')
ax.set_ylabel('S (normalized)')
ax.set_title('BE Entropy')
ax.grid(True, alpha=0.3)

# 4. Mass emergence at BEC
ax = axes[1, 1]
# m_app at each theta from the critical n
m_emerge = []
for t in thetas:
    T = T_eff(t)
    if T < m0:
        m_emerge.append(T)  # m_app ~ T at condensation boundary
    else:
        m_emerge.append(m0)
m_emerge = np.array(m_emerge)

ax.plot(thetas, m_emerge * 1000, 'darkred', linewidth=2, label='m_app at BEC boundary')
# Mark known particles
for name, n_p, m_p in particles:
    if m_p > 0 and m_p < 200:
        m_mev = m_p * 1000 if m_p < 1 else m_p * 1000
        if m_mev < max(m_emerge*1000):
            ax.axhline(y=m_mev, color='gray', linestyle=':', alpha=0.4)
            ax.text(82, m_mev, f' {name} ({m_p*1000:.1f} MeV)' if m_p < 1
                    else f' {name} ({m_p:.1f} GeV)',
                    fontsize=7, va='bottom')

add_lines(ax)
ax.set_xlabel('theta (degrees)')
ax.set_ylabel('Mass (MeV)')
ax.set_title('Emergent mass at condensation boundary')
ax.set_yscale('log')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('C:/Users/szoke/two-twistor-mass-emergence/visuals/bose_einstein_physical.png',
            dpi=150, bbox_inches='tight')
print(f"\nPlot saved to visuals/bose_einstein_physical.png")
