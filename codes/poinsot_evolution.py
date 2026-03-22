"""
Poinsot Ellipsoid Evolution - Single Cone, Two Hemispheres
One cone, one axis, upper/lower hemispheres counter-rotating.
V = const, L = const throughout.
Three geometric thresholds: 63.43, 45, 30 degrees.

Author: Szoke Barna
Date: March 2026
"""

import numpy as np

V0 = 1.0

def cone_from_theta(theta_deg):
    theta = np.radians(theta_deg)
    tan_t = np.tan(theta)
    h = (3 * V0 / (np.pi * tan_t**2))**(1.0/3.0)
    r = h * tan_t
    slant = np.sqrt(h**2 + r**2)
    surface = np.pi * r * slant + np.pi * r**2
    return h, r, slant, surface

def inertia_cone(theta_deg, mass=1.0):
    h, r, sl, su = cone_from_theta(theta_deg)
    I3 = (3.0/10.0) * mass * r**2
    I1 = (3.0/20.0) * mass * (r**2 + 4*h**2)
    return I1, I1, I3

def poinsot_ellipsoid(theta_deg, omega3=1.0, mass=1.0):
    I1, I2, I3 = inertia_cone(theta_deg, mass)
    T = 0.5 * I3 * omega3**2
    L = I3 * omega3
    a1 = np.sqrt(2*T / I1) if I1 > 0 else 0
    a2 = a1
    a3 = np.sqrt(2*T / I3) if I3 > 0 else 0
    V_ell = (4*np.pi/3) * a1 * a2 * a3
    if a1 > 0 and a3 > 0:
        if abs(a1 - a3) < 1e-12:
            S_ell = 4 * np.pi * a1**2
        elif a1 > a3:
            e = np.sqrt(1 - (a3/a1)**2)
            S_ell = 2*np.pi*a1**2 * (1 + (a3**2/(a1**2 * e)) * np.arctanh(e))
        else:
            e = np.sqrt(1 - (a1/a3)**2)
            S_ell = 2*np.pi*a1**2 * (1 + (a3/(a1 * e)) * np.arcsin(e))
    else:
        S_ell = 0
    return {
        'theta': theta_deg, 'I1': I1, 'I3': I3,
        'I1_over_I3': I1/I3 if I3 > 0 else float('inf'),
        'T': T, 'L': L, 'a1': a1, 'a3': a3,
        'a1_over_a3': a1/a3 if a3 > 0 else float('inf'),
        'V_ell': V_ell, 'S_ell': S_ell, 'V_cone': V0,
        'V_ratio': V_ell / V0,
        'S_over_V': S_ell / V_ell if V_ell > 0 else float('inf'),
    }

theta_spherical = np.degrees(np.arctan(2))
theta_contact = 45.0
theta_equilateral = 30.0

print("=" * 80)
print("POINSOT ELLIPSOID EVOLUTION")
print("Single cone, two counter-rotating hemispheres, V=const, L=const")
print("=" * 80)

print(f"\nCRITICAL ANGLES:")
print(f"  arctan(2)    = {theta_spherical:.4f} deg  I1=I3, spherical top")
print(f"  arctan(1)    = {theta_contact:.4f} deg  contact")
print(f"  arctan(1/v3) = {theta_equilateral:.4f} deg  equilateral cross-section")

print(f"\n{'='*80}")
print(f"{'th':>7} | {'h':>7} | {'r':>7} | {'r/h':>7} | {'I1':>9} | {'I3':>9} | {'I1/I3':>7} | {'Shape':>8}")
print(f"{'-'*7}-+-{'-'*7}-+-{'-'*7}-+-{'-'*7}-+-{'-'*9}-+-{'-'*9}-+-{'-'*7}-+-{'-'*8}")

angles = [89, 85, 80, 75, 70, 63.43, 60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 10]
for theta in angles:
    h, r, sl, su = cone_from_theta(theta)
    I1, I2, I3 = inertia_cone(theta)
    ratio = I1/I3
    shape = "OBLATE" if ratio > 1.001 else ("PROLATE" if ratio < 0.999 else "SPHERE")
    mark = " <<" if abs(theta-theta_spherical)<0.1 or abs(theta-45)<0.1 or abs(theta-30)<0.1 else ""
    print(f"{theta:7.2f} | {h:7.4f} | {r:7.4f} | {r/h:7.4f} | {I1:9.6f} | {I3:9.6f} | {ratio:7.4f} | {shape}{mark}")

print(f"\n{'='*80}")
print(f"POINSOT ELLIPSOID AT CRITICAL ANGLES")
print(f"{'='*80}")

for theta, name in [(89, "START (~90 deg)"),
                     (theta_spherical, "SPHERICAL TOP (63.43 deg)"),
                     (theta_contact, "CONTACT (45 deg)"),
                     (theta_equilateral, "EQUILATERAL (30 deg)")]:
    p = poinsot_ellipsoid(theta)
    h, r, sl, su = cone_from_theta(theta)
    print(f"\n--- {name} ---")
    print(f"  Cone:  h={h:.6f}  r={r:.6f}  r/h={r/h:.6f}")
    print(f"  I1={p['I1']:.8f}  I3={p['I3']:.8f}  I1/I3={p['I1_over_I3']:.6f}")
    print(f"  T={p['T']:.8f}  L={p['L']:.8f}")
    print(f"  Ellipsoid: a1=a2={p['a1']:.6f}  a3={p['a3']:.6f}  a1/a3={p['a1_over_a3']:.6f}")
    print(f"  V_ell={p['V_ell']:.8f}  V_cone={p['V_cone']:.6f}")
    print(f"  V_ell/V_cone={p['V_ratio']:.8f}")
    print(f"  S_ell={p['S_ell']:.8f}  S/V={p['S_over_V']:.6f}")

print(f"\n{'='*80}")
print(f"RATIOS BETWEEN THRESHOLDS")
print(f"{'='*80}")

p0 = poinsot_ellipsoid(89)
ps = poinsot_ellipsoid(theta_spherical)
pc = poinsot_ellipsoid(theta_contact)
pe = poinsot_ellipsoid(theta_equilateral)

print(f"\n  V_ell ratios:")
print(f"    sphere/start     = {ps['V_ell']/p0['V_ell']:.6f}")
print(f"    contact/sphere   = {pc['V_ell']/ps['V_ell']:.6f}")
print(f"    equilat/contact  = {pe['V_ell']/pc['V_ell']:.6f}")
print(f"    equilat/start    = {pe['V_ell']/p0['V_ell']:.6f}")

print(f"\n  Energy T ratios:")
print(f"    sphere/start     = {ps['T']/p0['T']:.6f}")
print(f"    contact/sphere   = {pc['T']/ps['T']:.6f}")
print(f"    equilat/contact  = {pe['T']/pc['T']:.6f}")

print(f"\n  I3 ratios:")
print(f"    sphere/start     = {ps['I3']/p0['I3']:.6f}")
print(f"    contact/sphere   = {pc['I3']/ps['I3']:.6f}")
print(f"    equilat/contact  = {pe['I3']/pc['I3']:.6f}")

print(f"\n{'='*80}")
print(f"KEY GEOMETRIC CONSTANTS")
print(f"{'='*80}")
print(f"  sin(63.43) = {np.sin(np.radians(theta_spherical)):.6f}  = 2/v5 = {2/np.sqrt(5):.6f}")
print(f"  cos(63.43) = {np.cos(np.radians(theta_spherical)):.6f}  = 1/v5 = {1/np.sqrt(5):.6f}")
print(f"  sin(45)    = {np.sin(np.radians(45)):.6f}  = 1/v2")
print(f"  cos(45)    = {np.cos(np.radians(45)):.6f}  = 1/v2")
print(f"  sin(30)    = {np.sin(np.radians(30)):.6f}  = 1/2")
print(f"  cos(30)    = {np.cos(np.radians(30)):.6f}  = v3/2")
print(f"")
print(f"  Angle gaps:")
print(f"    90 - 63.43      = {90-theta_spherical:.4f} deg")
print(f"    63.43 - 45      = {theta_spherical-45:.4f} deg")
print(f"    45 - 30         = 15.0000 deg")
print(f"    (63.43-45)/(45-30) = {(theta_spherical-45)/15:.6f}")
