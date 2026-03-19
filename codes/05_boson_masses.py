"""
Boson Mass Predictions: Z, W, Higgs from cone mechanics
Energy budget: 500 GeV total = 2 × 250 GeV cones
"""
import numpy as np

m0 = 246.22  # GeV (post-graviton VEV)
m0_cone = 250.0  # GeV (pre-graviton cone energy)

# Cone mechanics
kappa = (3*np.sqrt(2)/4)**(2/3)
I3_ratio_45 = 8/5
I3_ratio_30 = 8/7
T1 = 0.1500  # Mc² units
T_min = 9/(40*kappa)
Delta_E = T_min - T1

print("Cone Mechanics:")
print(f"  κ = (3√2/4)^(2/3) = {kappa:.6f}")
print(f"  T(45°) = {T1:.4f} m₀c²")
print(f"  T_min(30°) = {T_min:.4f} m₀c²")
print(f"  ΔE = {Delta_E:.4f} m₀c²")

# Z boson (uses pre-graviton mass 250)
mZ_pred = np.sqrt(2*Delta_E) * m0_cone
mZ_obs = 91.19
print(f"\nm_Z = √(2×{Delta_E:.4f}) × {m0_cone} = {mZ_pred:.2f} GeV")
print(f"  Observed: {mZ_obs} GeV, Match: {mZ_pred/mZ_obs*100:.2f}%")

# W boson
sin2_W = 3/13
mW_pred = mZ_pred * np.sqrt(1 - sin2_W)
mW_obs = 80.38
print(f"\nm_W = m_Z × √(1-3/13) = {mW_pred:.2f} GeV")
print(f"  Observed: {mW_obs} GeV, Match: {mW_pred/mW_obs*100:.2f}%")

# Higgs
E3 = m0 * 0.25/2  # m₀ sin²30°/2
mH_pred = m0 - mZ_obs - E3
print(f"\nm_H = m₀ - m_Z - m₀sin²30°/2 = {m0} - {mZ_obs} - {E3:.1f} = {mH_pred:.1f} GeV")
print(f"  Observed: 125.10 GeV, Match: {mH_pred/125.10*100:.2f}%")

# Energy budget
print(f"\nEnergy budget per cone:")
print(f"  Z:     {mZ_obs:.1f} GeV ({mZ_obs/m0*100:.1f}%)")
print(f"  H:     125.1 GeV ({125.1/m0*100:.1f}%)")
print(f"  E₃:    {m0-mZ_obs-125.1:.1f} GeV ({(m0-mZ_obs-125.1)/m0*100:.1f}%)")
print(f"  Total: {m0:.2f} GeV")
print(f"\n  Two cones: 2×{m0} + 8 (graviton) = {2*m0+8:.1f} ≈ 500 GeV")
