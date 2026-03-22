"""
Braking Energetics - Spin-down to Pure Precession
One cone, two hemispheres, BE asymmetry causes spin to brake.
Braking energy -> torsion -> gravity.
Final state: ONLY precession remains.

Author: Szoke Barna, March 2026
"""
import numpy as np

V0 = 1.0

def cone_from_theta(theta_deg):
    theta = np.radians(theta_deg)
    tan_t = np.tan(theta)
    h = (3 * V0 / (np.pi * tan_t**2))**(1.0/3.0)
    r = h * tan_t
    return h, r

def inertia_cone(theta_deg, mass=1.0):
    h, r = cone_from_theta(theta_deg)
    I3 = (3.0/10.0) * mass * r**2
    I1 = (3.0/20.0) * mass * (r**2 + 4*h**2)
    return I1, I3

def two_hemispheres(theta_deg, delta_rho, omega_spin=1.0, mass_total=1.0):
    m_A = mass_total * (1 + delta_rho) / 2
    m_B = mass_total * (1 - delta_rho) / 2
    I1_A, I3_A = inertia_cone(theta_deg, m_A)
    I1_B, I3_B = inertia_cone(theta_deg, m_B)
    T_spin_A = 0.5 * I3_A * omega_spin**2
    T_spin_B = 0.5 * I3_B * omega_spin**2
    T_torsion = abs(T_spin_A - T_spin_B)
    T_spin_total = T_spin_A + T_spin_B
    return {
        'theta': theta_deg, 'delta_rho': delta_rho,
        'T_spin_A': T_spin_A, 'T_spin_B': T_spin_B,
        'T_spin_total': T_spin_total,
        'T_torsion': T_torsion,
        'torsion_fraction': T_torsion / T_spin_total if T_spin_total > 0 else 0,
    }

print("=" * 80)
print("BRAKING ENERGETICS")
print("=" * 80)

# IDEAL CASE
print("\n--- IDEAL (no asymmetry) ---")
for theta in [89, 63.43, 60, 45, 30]:
    I1, I3 = inertia_cone(theta)
    print(f"  theta={theta:7.2f}  I1/I3={I1/I3:7.4f}  T_spin={0.5*I3:.6f}")

# BE ASYMMETRY
print("\n" + "=" * 80)
print("BE ASYMMETRY TABLE")
print("=" * 80)
print(f"\n{'th':>7} | {'dRho':>6} | {'T_A':>10} | {'T_B':>10} | {'T_torsion':>10} | {'Tors%':>7}")
print(f"{'-'*7}-+-{'-'*6}-+-{'-'*10}-+-{'-'*10}-+-{'-'*10}-+-{'-'*7}")

for theta in [89, 63.43, 60, 45, 30]:
    for dr in [0.001, 0.01, 0.05, 0.10]:
        h = two_hemispheres(theta, dr)
        print(f"{theta:7.2f} | {dr:6.3f} | {h['T_spin_A']:10.6f} | {h['T_spin_B']:10.6f} | {h['T_torsion']:10.6f} | {h['torsion_fraction']*100:6.2f}%")
    print()

# GRAVITON
print("=" * 80)
print("GRAVITON ENERGY FROM BRAKING")
print("=" * 80)
E_cone = 250.0
m0 = 246.22
E_grav = E_cone - m0
dr_target = E_grav / E_cone
print(f"\n  E_cone={E_cone} GeV, m0={m0} GeV, E_grav={E_grav:.2f} GeV/cone")
print(f"  delta_rho = {dr_target:.6f}")
h30 = two_hemispheres(30, dr_target)
print(f"  At 30 deg: torsion_fraction = {h30['torsion_fraction']:.6f}")
print(f"  T_torsion in GeV = {E_cone * h30['torsion_fraction']:.4f}")

# I1/I3 EXACT FRACTIONS
print("\n" + "=" * 80)
print("I1/I3 EXACT FRACTIONS")
print("=" * 80)
for theta, name, exact in [(63.43,"1/1",1), (60,"7/6",7/6), (45,"5/2",5/2), (30,"13/2",13/2)]:
    I1, I3 = inertia_cone(theta)
    r = I1/I3
    print(f"  {theta:6.2f} deg: I1/I3={r:.8f}  exact={name}={exact:.8f}  diff={abs(r-exact):.2e}")

print("\n  ANALYTIC PROOF:")
print("    60 deg: r=h*sqrt(3) -> I1=(21/20)h^2, I3=(9/10)h^2 -> 7/6 EXACT")
print("    45 deg: r=h         -> I1=(3/4)h^2,   I3=(3/10)h^2 -> 5/2 EXACT")
print("    30 deg: r=h/sqrt(3) -> I1=(13/20)h^2,  I3=(1/10)h^2 -> 13/2 EXACT")

# S/V
print("\n" + "=" * 80)
print("POINSOT S/V AT KEY ANGLES")
print("=" * 80)
for theta in [63.43, 60, 45, 30]:
    I1, I3 = inertia_cone(theta)
    a1 = np.sqrt(I3/I1)
    a3 = 1.0
    V = (4*np.pi/3) * a1**2 * a3
    if abs(a1-a3) < 1e-10:
        S = 4*np.pi*a1**2
    elif a1 < a3:
        e = np.sqrt(1-(a1/a3)**2)
        S = 2*np.pi*a1**2*(1+(a3/(a1*e))*np.arcsin(e))
    else:
        e = np.sqrt(1-(a3/a1)**2)
        S = 2*np.pi*a1**2*(1+(a3**2/(a1**2*e))*np.arctanh(e))
    print(f"  {theta:6.2f}: a1={a1:.6f} V={V:.6f} S={S:.6f} S/V={S/V:.6f}")

print("\nDONE")
