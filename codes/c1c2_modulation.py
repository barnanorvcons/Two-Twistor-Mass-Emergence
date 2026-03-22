"""
c1/c2 Modulation and CMB Polarization
Two perpendicular polarized waves from two time vectors.
Before axis break: cancellation. After: mutual modulation.
Author: Szoke Barna, March 2026
"""
import numpy as np
from numpy.fft import fft

N=360; phi=np.linspace(0,2*np.pi,N)
prec=2./13; dr=0.01512; cos30=np.cos(np.radians(30)); sin30=np.sin(np.radians(30))

print("="*80)
print("c1/c2 MODULATION AND CMB POLARIZATION")
print("="*80)

# PHASE 1: CANCELLATION
A1=1+dr; A2=1-dr
print("\n1. BEFORE AXIS BREAK: CANCELLATION")
print(f"  A1={A1:.6f} A2={A2:.6f} residual=2*dr={2*dr:.6f}")
print(f"  At phi=pi/2: signal={2*dr:.6f} (MINIMUM not maximum)")

# PHASE 2: MODULATION
E_carrier=np.sin(phi)
E_mod=1-(1-cos30)*np.sin(prec*phi)**2
E_mode=E_carrier*E_mod
B_carrier=np.cos(phi)
B_mod=sin30*np.sin(prec*phi)
B_mode=B_carrier*B_mod
E_max=np.max(np.abs(E_mode)); B_max=np.max(np.abs(B_mode))

print("\n2. AFTER AXIS BREAK: MODULATION")
print(f"  E-mode max={E_max:.6f}")
print(f"  B-mode max={B_max:.6f}=sin(30)")
print(f"  B/E={B_max/E_max:.6f}")
print(f"  Precession=2/13={prec:.6f}")

# c1/c2
print("\n3. c1/c2 RATIO")
for p,n in [(0,"0"),(np.pi/2,"pi/2"),(np.pi,"pi"),(2*np.pi,"2pi")]:
    print(f"  phi={n:>5s}: c1/c2={np.exp(-p):.6f} c2/c1={np.exp(p):.6f}")

# POWER SPECTRUM
E_fft=np.abs(fft(E_mode))[:N//2]
B_fft=np.abs(fft(B_mode))[:N//2]
E_fft=E_fft/np.max(E_fft); B_fft_n=B_fft/np.max(E_fft) if np.max(E_fft)>0 else B_fft

print("\n4. POWER SPECTRUM")
print(f"  {'ell':>4} | {'C_EE':>10} | {'C_BB':>10} | {'BB/EE':>10}")
for l in [2,3,5,7,10,13,20,30,50]:
    if l<len(E_fft):
        ee=E_fft[l]**2; bb=B_fft_n[l]**2
        r=bb/ee if ee>1e-15 else 0
        print(f"  {l:4d} | {ee:10.6f} | {bb:10.6f} | {r:10.6f}")

# TENSOR-TO-SCALAR
tEE=np.sum(E_fft[2:]**2); tBB=np.sum(B_fft_n[2:]**2)
r_t=tBB/tEE if tEE>0 else 0
print(f"\n5. TENSOR-TO-SCALAR r={r_t:.6f}")
print(f"  Observed: r<0.036 (BICEP/Keck 2021)")
print(f"  Framework: (2/13)^2={(2./13)**2:.6f}")

# ELLIPTICITY
ecc=np.sqrt(1-(B_max/E_max)**2) if E_max>B_max else 0
print(f"\n6. POLARIZATION ELLIPSE")
print(f"  Eccentricity={ecc:.6f}")
print(f"  Ellipticity=B/E={B_max/E_max:.6f}")
print(f"  tan(30)={np.tan(np.radians(30)):.6f}")
print(f"  1/sqrt(3)={1/np.sqrt(3):.6f}")

# STOKES
print("\n7. STOKES PARAMETERS")
print(f"  {'phi':>6} | {'E':>8} | {'B':>8} | {'Q':>10} | {'U':>10}")
for i,n in [(0,"0"),(N//8,"pi/4"),(N//4,"pi/2"),(N//2,"pi")]:
    E=E_mode[i]; B=B_mode[i]; Q=E**2-B**2; U=2*E*B
    print(f"  {n:>6} | {E:8.5f} | {B:8.5f} | {Q:10.6f} | {U:10.6f}")

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"  Cancellation residual: 2*delta_rho={2*dr:.6f}")
print(f"  E-mode: modulated by cos(30)={cos30:.6f}")
print(f"  B-mode: torsion, amplitude=sin(30)={sin30:.6f}")
print(f"  r ~ (2/13)^2 = {(2./13)**2:.6f}")
print(f"  Ellipticity = tan(30) = 1/sqrt(3) = {1/np.sqrt(3):.6f}")
print(f"  c1*c2 = c^2 (constant)")
print(f"  #40: CMB quadrupole suppression = cancellation")
print(f"  #41: B-mode amplitude = sin(30) torsion")
print("="*80)
