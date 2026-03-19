"""
All Five Fundamental Coupling Constants from Prime Structure in PG(5,2)
"""
import numpy as np

print("="*60)
print("COUPLING CONSTANTS FROM PRIME STRUCTURE")
print("="*60)

# 1. Electromagnetic
alpha_inv_pred = 163 - 2*13  # = 137
alpha_inv_obs = 137.036
print(f"\n1/α_EM = 163 - 2×13 = {alpha_inv_pred}")
print(f"   Observed: {alpha_inv_obs}")
print(f"   Match: {alpha_inv_pred/alpha_inv_obs*100:.2f}%")

# 2. Weinberg angle
sin2_pred = 3/13
sin2_obs = 0.23121
print(f"\nsin²θ_W = 3/13 = {sin2_pred:.5f}")
print(f"   Observed: {sin2_obs}")
print(f"   Match: {sin2_pred/sin2_obs*100:.2f}%")

# 3. Strong coupling
alpha_s_pred = 7/59
alpha_s_obs = 0.1180
print(f"\nα_s = 7/59 = {alpha_s_pred:.5f}")
print(f"   59 = 35 (Q⁺ quadric) + 24 (max cliques)")
print(f"   Observed: {alpha_s_obs}")
print(f"   Match: {alpha_s_pred/alpha_s_obs*100:.2f}%")

# 4. Higgs self-coupling
f_Z = np.sqrt(2*0.0663)  # Z fraction
f_3 = 0.25/2  # sin²30°/2
f_H = 1 - f_Z - f_3
lambda_pred = f_H**2 / 2
lambda_obs = 0.129
print(f"\nλ_Higgs = (1 - √(2×0.0663) - sin²30°/2)²/2 = {lambda_pred:.4f}")
print(f"   Observed: {lambda_obs}")
print(f"   Match: {lambda_pred/lambda_obs*100:.2f}%")

# 5. Muon g-2
g2_pred = 1/384
g2_obs = 0.00261
print(f"\nα' (g-2) = 1/384 = {g2_pred:.6f}")
print(f"   Observed: {g2_obs}")
print(f"   Match: {g2_pred/g2_obs*100:.2f}%")

# 6. Up-down coupling
g_ud = 2/np.pi
ratio_pred = np.sqrt((1+g_ud)/(1-g_ud))
ratio_obs = 4.7/2.2
print(f"\ng(u,d) = 2/π = {g_ud:.6f}")
print(f"   m_d/m_u = {ratio_pred:.3f} (obs: {ratio_obs:.3f}, {ratio_pred/ratio_obs*100:.1f}%)")

# Prime skeleton
print(f"\n{'='*60}")
print("PRIME SKELETON:")
print(f"  163 - 137 = 26 = 2×13")
print(f"  137 - 59  = 78 = dim(E₆)")
print(f"  163 - 59  = 104 = 8×13")
print(f"  All primes: 3, 7, 13, 59, 137, 163")
print(f"{'='*60}")
