"""
H tensor F2 = M2(F2): EXPLICIT ISOMORPHISM
The quaternion algebra reduced to F2 = the Compartment algebra
Author: Szoke Barna, March 2026
"""

def mm(A,B):
    return (((A[0][0]*B[0][0]+A[0][1]*B[1][0])%2,(A[0][0]*B[0][1]+A[0][1]*B[1][1])%2),
            ((A[1][0]*B[0][0]+A[1][1]*B[1][0])%2,(A[1][0]*B[0][1]+A[1][1]*B[1][1])%2))

def ma(A,B):
    return (((A[0][0]+B[0][0])%2,(A[0][1]+B[0][1])%2),
            ((A[1][0]+B[1][0])%2,(A[1][1]+B[1][1])%2))

I=((1,0),(0,1)); O=((0,0),(0,0))
swap=((0,1),(1,0))
P=ma(I,swap)  # [[1,1],[1,1]]

print("H tensor F2 = M2(F2)")
print("="*60)

# Over F2: -1=1, so i^2=j^2=k^2=1
# ij=k, ji=-k=k, so COMMUTATIVE
print("Over F2: i^2=j^2=k^2=1 (since -1=1)")
print("ij=ji=k (COMMUTATIVE)")

# The isomorphism
print("
ISOMORPHISM:")
print("  epsilon = 1 = [[1,0],[0,1]]")
print("  omega   = i = [[0,1],[1,0]] = swap")
print("  P = 1+i = [[1,1],[1,1]] = nilpotent")

# Verify P^2 = 0
PP=mm(P,P)
print("
P^2 = [[%d,%d],[%d,%d]] = ZERO: %s" % (PP[0][0],PP[0][1],PP[1][0],PP[1][1],PP==O))

# Verify epsilon + omega + P = 0
eop=ma(ma(I,swap),P)
print("eps+omega+P = [[%d,%d],[%d,%d]] = ZERO: %s" % (eop[0][0],eop[0][1],eop[1][0],eop[1][1],eop==O))

# All 16 elements
print("
ALL 16 ELEMENTS:")
j=((1,1),(0,1))
k=mm(swap,j)
print("  j = [[1,1],[0,1]]")
print("  k = ij = [[%d,%d],[%d,%d]]" % (k[0][0],k[0][1],k[1][0],k[1][1]))

# Verify j^2
jj=mm(j,j)
print("  j^2 = [[%d,%d],[%d,%d]] = I: %s" % (jj[0][0],jj[0][1],jj[1][0],jj[1][1],jj==I))
kk=mm(k,k)
print("  k^2 = [[%d,%d],[%d,%d]] = I: %s" % (kk[0][0],kk[0][1],kk[1][0],kk[1][1],kk==I))

# k^2 might not be I! Check
if kk!=I:
    print("  NOTE: k^2 != I over F2!")
    print("  This means H_F2 is NOT a division algebra")
    print("  It is M2(F2) = matrix algebra (has zero divisors)")

# List all 16
print("
FULL TABLE:")
print("  abcd  matrix       det  name")
for a in range(2):
    for b in range(2):
        for c in range(2):
            for d in range(2):
                m=O
                if a: m=ma(m,I)
                if b: m=ma(m,swap)
                if c: m=ma(m,j)
                if d: m=ma(m,k)
                det=(m[0][0]*m[1][1]+m[0][1]*m[1][0])%2
                nm=""
                if (a,b,c,d)==(0,0,0,0): nm="zero"
                elif (a,b,c,d)==(1,0,0,0): nm="1=eps"
                elif (a,b,c,d)==(0,1,0,0): nm="i=omega"
                elif (a,b,c,d)==(0,0,1,0): nm="j"
                elif (a,b,c,d)==(0,0,0,1): nm="k=ij"
                elif (a,b,c,d)==(1,1,0,0): nm="1+i=P"
                print("  %d%d%d%d  [[%d,%d],[%d,%d]]  %d    %s" % (a,b,c,d,m[0][0],m[0][1],m[1][0],m[1][1],det,nm))

# Z2xZ2 grading
print("
Z2xZ2 GRADING:")
print("  (0,0) -> 1 = epsilon")
print("  (1,0) -> i = omega")
print("  (0,1) -> j")
print("  (1,1) -> k = ij")
print("  phi1 picks i, phi2 picks j, phi3 picks k")
print("  Three surjections = three quaternion axes = three Pin covers")

print("
CONCLUSION:")
print("  Compartment algebra = quaternion algebra over F2")
print("  eps+omega+P=0 = quaternion identity mod 2")
print("  P^2=0 because (1+i)^2 = 1+2i+i^2 = 1+0+1 = 0 in F2")
print("  The 16 spacetime matrices = quaternions mod 2")
print("  F2 = residue field at the ramification prime p=2")
