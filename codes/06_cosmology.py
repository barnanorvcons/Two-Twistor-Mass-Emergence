"""
Cosmological Observables: Hubble, MOND, Dark Matter, Age
From the constraint c₁/t₂ = c₂/t₁ = A
"""
import numpy as np

c = 2.998e8  # m/s

# Hubble constant range
for label, H0_km in [("Planck", 67.36), ("User", 74.5), ("SH0ES", 73.0)]:
    H0 = H0_km * 1e3 / 3.086e22  # s^-1
    A = H0 * c  # m/s^2
    a0 = A / (2*np.pi)
    t_age = 1/H0 / (365.25*24*3600*1e9)
    print(f"H₀ = {H0_km} km/s/Mpc ({label}):")
    print(f"  A = H₀c = {A:.3e} m/s²")
    print(f"  a₀ = A/(2π) = {a0:.3e} m/s² (Milgrom: 1.2e-10)")
    print(f"  Age = c/A = {t_age:.1f} Gyr (obs: 13.8)")
    print()

# Dark matter fraction
DM_pred = (2**6 - 2**3) / 2**6
print(f"Dark matter fraction: (2⁶-2³)/2⁶ = {DM_pred*100:.1f}%")
print(f"  Observed: 85%")
print(f"  Match: {DM_pred/0.85*100:.1f}%")
