"""
VO+(4,2) = K4⊗K4 Quark Mass Computation
Complete eigenvalue analysis and mass predictions
"""
import numpy as np

# K4 tensor product
K4 = np.ones((4,4)) - np.eye(4)
VO = np.kron(K4, K4)
evals = np.round(np.linalg.eigvalsh(VO), 6)
unique, counts = np.unique(evals, return_counts=True)

print("VO+(4,2) Eigenvalues:")
for e, c in zip(unique[::-1], counts[::-1]):
    print(f"  λ = {e:+.0f}  ×{c}")
print(f"  1 singlet + 6 quarks + 9 (8 gluons + 1) = 16\n")

# Framework constants
m0 = 246.22  # GeV
N = 1.0858e7
alpha = 1/137.036
g_ud = 2/np.pi

# Observed masses
mu, md, ms, mc, mb, mt = 2.2e-3, 4.7e-3, 0.095, 1.275, 4.18, 173.0

# Generation couplings
g1 = (md**2 - mu**2)/(md**2 + mu**2)
g2 = (mc**2 - ms**2)/(mc**2 + ms**2)
g3 = (mt**2 - mb**2)/(mt**2 + mb**2)

print("Generation couplings:")
print(f"  g1 = {g1:.6f}  (2/π = {g_ud:.6f}, match: {g1/g_ud*100:.1f}%)")
print(f"  g2 = {g2:.6f}  g3 = {g3:.6f}")
print(f"  F2 = {(1-g1)/(1-g2):.1f}  F3 = {(1-g1)/(1-g3):.1f}")

# Predictions
print(f"\nPredictions:")
print(f"  m_t = m0/√2 = {m0/np.sqrt(2):.1f} GeV (obs: 173.0, {m0/np.sqrt(2)/173*100:.1f}%)")
print(f"  m_d/m_u = √((1+2/π)/(1-2/π)) = {np.sqrt((1+g_ud)/(1-g_ud)):.3f} (obs: {md/mu:.3f}, {np.sqrt((1+g_ud)/(1-g_ud))/(md/mu)*100:.1f}%)")
Dn_cs = 145
dm2_pred = 2*m0**2*Dn_cs/N
dm2_obs = mc**2 - ms**2
print(f"  Δm²(c-s) = {dm2_pred*1e6:.0f} MeV² (obs: {dm2_obs*1e6:.0f}, {dm2_pred/dm2_obs*100:.1f}%)")
print(f"  sin θ_C = √(m_d/m_s) = {np.sqrt(md/ms):.4f} (obs: 0.2243, {np.sqrt(md/ms)/0.2243*100:.1f}%)")
