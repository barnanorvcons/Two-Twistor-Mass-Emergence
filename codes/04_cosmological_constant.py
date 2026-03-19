"""
Cosmological Constant: ρ_Λ = (4/3)m₀⁴/N⁸
Resolving the 10¹²³ discrepancy
"""
import numpy as np

m0 = 246.22  # GeV
N = 1.0858e7
M_Pl = 1.22e19  # GeV

rho_pred = (4/3) * m0**4 / N**8
rho_obs = 2.52e-47  # GeV^4

print(f"ρ_Λ = (4/3) × m₀⁴/N⁸")
print(f"   = (4/3) × {m0**4:.3e} / {N**8:.3e}")
print(f"   = {rho_pred:.3e} GeV⁴")
print(f"   Observed: {rho_obs:.2e} GeV⁴")
print(f"   Match: {rho_pred/rho_obs*100:.1f}%")

# The 10^123 decomposition
factor1 = (M_Pl/m0)**4
factor2 = N**8
print(f"\nThe 10¹²³ discrepancy:")
print(f"   (M_Pl/m₀)⁴ = {factor1:.2e}  (wrong cutoff)")
print(f"   N⁸          = {factor2:.2e}  (hidden energy)")
print(f"   Product     = {factor1*factor2:.2e}  ≈ 10¹²³")

# N cross-check
N_from_lambda = (4*m0**4/(3*rho_obs))**(1/8)
print(f"\nN from Λ:       {N_from_lambda:.4e}")
print(f"N from leptons: {N:.4e}")
print(f"Match: {N_from_lambda/N*100:.1f}%")
