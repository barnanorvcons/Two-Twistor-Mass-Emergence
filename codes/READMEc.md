# Computational Codes

All computations supporting "Mass Emergence from Two-Twistor Geometry."

## Part I — Python (metric, masses, couplings)

| Code | Description |
|------|-------------|
| `01_VO_quark_computation.py` | VO+(4,2) = K4⊗K4 eigenvalues, quark mass predictions |
| `02_coupling_constants.py` | All 5 fundamental couplings from prime structure |
| `03_lepton_masses.py` | Electron, muon, tau masses from (α, N, m₀) |
| `04_cosmological_constant.py` | ρ_Λ = (4/3)m₀⁴/N⁸, the 10¹²³ resolution |
| `05_boson_masses.py` | Z, W, Higgs from cone mechanics energy budget |
| `06_cosmology.py` | Hubble, MOND, dark matter fraction, age |

## Part II — JavaScript (dark sector, derived equations)

| Code | Description |
|------|-------------|
| `compute_dark_sector.js` | Dark fermion masses, √2 scaling, dark electron = muon |
| `compute_dark_sector_v2.js` | Extended dark sector: dark photon, three generations |
| `compute_dark_bh.js` | Dark black holes, Chandrasekhar limit, TOV limit |
| `compute_maxwell.js` | Maxwell equations from torsion derivation |
| `compute_schrodinger.js` | Schrödinger from 5D wave equation |
| `compute_experiments.js` | Experimental predictions and testable signatures |

## Requirements

- Python 3.x + NumPy (Part I)
- Node.js (Part II)

## Running

```bash
python 01_VO_quark_computation.py
python 02_coupling_constants.py
python 03_lepton_masses.py
python 04_cosmological_constant.py
python 05_boson_masses.py
python 06_cosmology.py

node compute_dark_sector.js
node compute_dark_bh.js
node compute_maxwell.js
node compute_schrodinger.js
node compute_experiments.js
```

All codes are self-contained and reproduce the results in the papers exactly.
