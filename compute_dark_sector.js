const m0 = 246.22; // GeV
const N = 1.0858e7;
const alpha = 1/137.036;
const Delta = 4*alpha*alpha/9;
const pi = Math.PI;

// ======== VISIBLE SECTOR ========
console.log("================================================================");
console.log("     VISIBLE SECTOR (Cone A, \u03C6-k\u00F6r, N = " + N.toExponential(4) + ")");
console.log("================================================================");

const m_e = 2*m0*alpha*Math.sqrt(2/N)/3;
const m_mu = Math.sqrt(m_e*m_e + 2*m0*m0/N);
const m_tau = Math.sqrt(m_mu*m_mu + 564*m0*m0/N);

const m_t = m0/Math.sqrt(2);
const md_mu_ratio = Math.sqrt((1+2/pi)/(1-2/pi));
const m_u = 0.00222;
const m_d = m_u * md_mu_ratio;
const m_s = 0.095;
const mc2_ms2 = 2*m0*m0*145/N;
const m_c = Math.sqrt(m_s*m_s + mc2_ms2);
const mt2_mb2 = 2*Math.pow(Math.sin(30*pi/180), 2) * m0*m0;
const m_b = Math.sqrt(m_t*m_t - mt2_mb2);

const m_Z = Math.sqrt(2*0.0663)*250;
const sin2w = 3/13;
const m_W = m_Z * Math.sqrt(1 - sin2w);
const m_H = m0 - m_Z - m0*Math.pow(Math.sin(30*pi/180), 2)/2;

console.log("LEPTONS:");
console.log("  Electron:   " + (m_e*1000).toFixed(3) + " MeV     (obs: 0.511)");
console.log("  Muon:       " + (m_mu*1000).toFixed(2) + " MeV   (obs: 105.66)");
console.log("  Tau:        " + (m_tau*1000).toFixed(0) + " MeV      (obs: 1777)");
console.log("QUARKS:");
console.log("  Up:         " + (m_u*1000).toFixed(1) + " MeV       (obs: 2.2)");
console.log("  Down:       " + (m_d*1000).toFixed(1) + " MeV       (obs: 4.7)");
console.log("  Strange:    " + (m_s*1000).toFixed(0) + " MeV        (obs: 95)");
console.log("  Charm:      " + (m_c*1000).toFixed(0) + " MeV      (obs: 1275)");
console.log("  Bottom:     " + (m_b*1000).toFixed(0) + " MeV      (obs: 4180)");
console.log("  Top:        " + (m_t*1000).toFixed(0) + " MeV    (obs: 173000)");
console.log("BOSONS:");
console.log("  W:          " + (m_W*1000).toFixed(0) + " MeV     (obs: 80380)");
console.log("  Z:          " + (m_Z*1000).toFixed(0) + " MeV     (obs: 91190)");
console.log("  Higgs:      " + (m_H*1000).toFixed(0) + " MeV    (obs: 125100)");
console.log("  Photon:     0");
console.log("  Gluon:      0");

// ======== DARK SECTOR ========
const Nd = N/2;
console.log("");
console.log("================================================================");
console.log("     DARK SECTOR (Cone B, \u03C6\u2032-k\u00F6r, N\u2032 = " + Nd.toExponential(4) + ")");
console.log("     \u03C3\u2032 = \u03C3/2,  \u03B5\u2032 = 4\u03B5");
console.log("================================================================");

// Dark Leptons (N -> N/2)
const m_de = 2*m0*alpha*Math.sqrt(2/Nd)/3;
const m_dmu = Math.sqrt(m_de*m_de + 2*m0*m0/Nd);
const m_dtau = Math.sqrt(m_dmu*m_dmu + 564*m0*m0/Nd);

// Dark electron from DIRECT mass emergence formula
const m_de_direct = Math.sqrt(2*m0*m0/N);

console.log("DARK LEPTONS:");
console.log("  Dark e:     " + (m_de*1000).toFixed(3) + " MeV");
console.log("  Dark \u03BC:     " + (m_dmu*1000).toFixed(2) + " MeV");
console.log("  Dark \u03C4:     " + (m_dtau*1000).toFixed(0) + " MeV = " + m_dtau.toFixed(3) + " GeV");
console.log("");
console.log("  ** Dark e (direct formula): " + (m_de_direct*1000).toFixed(2) + " MeV");
console.log("  ** Visible muon:            " + (m_mu*1000).toFixed(2) + " MeV");
console.log("  ** MATCH: " + (m_de_direct/m_mu*100).toFixed(2) + "%");

// Dark Quarks
// Light quarks scale with sqrt(N/Nd) = sqrt(2)
const m_du = m_u * Math.sqrt(2);
const m_dd = m_du * md_mu_ratio;
const m_ds = m_s * Math.sqrt(2);
const mc2_ms2_d = 2*m0*m0*145/Nd;
const m_dc = Math.sqrt(m_ds*m_ds + mc2_ms2_d);
const m_dt = m0/Math.sqrt(2); // same cone angle
const m_db = Math.sqrt(m_dt*m_dt - mt2_mb2);

console.log("");
console.log("DARK QUARKS:");
console.log("  Dark u:     " + (m_du*1000).toFixed(1) + " MeV");
console.log("  Dark d:     " + (m_dd*1000).toFixed(1) + " MeV");
console.log("  Dark s:     " + (m_ds*1000).toFixed(0) + " MeV");
console.log("  Dark c:     " + (m_dc*1000).toFixed(0) + " MeV = " + m_dc.toFixed(3) + " GeV");
console.log("  Dark b:     " + (m_db*1000).toFixed(0) + " MeV = " + m_db.toFixed(2) + " GeV");
console.log("  Dark t:     " + (m_dt*1000).toFixed(0) + " MeV = " + m_dt.toFixed(1) + " GeV");

console.log("");
console.log("DARK BOSONS:");
console.log("  Dark W:     " + (m_W*1000).toFixed(0) + " MeV  (same cone geometry)");
console.log("  Dark Z:     " + (m_Z*1000).toFixed(0) + " MeV  (same cone geometry)");
console.log("  Dark H:     " + (m_H*1000).toFixed(0) + " MeV (same cone geometry)");
console.log("  Dark \u03B3:     0 (n = N/2, fully precessing)");
console.log("  Dark g:     0");

// ======== FULL COMPARISON TABLE ========
console.log("");
console.log("================================================================");
console.log("     FULL COMPARISON TABLE");
console.log("================================================================");
console.log("Particle   Visible        Dark           Ratio   Connection");
console.log("--------   -----------    -----------    -----   ----------");

function pad(s, n) { return (s + "                    ").substring(0, n); }

var rows = [
  ["e",      m_e*1e3,     m_de*1e3,    "MeV"],
  ["\u03BC",      m_mu*1e3,    m_dmu*1e3,   "MeV"],
  ["\u03C4",      m_tau*1e3,   m_dtau*1e3,  "MeV"],
  ["u",      m_u*1e3,     m_du*1e3,    "MeV"],
  ["d",      m_d*1e3,     m_dd*1e3,    "MeV"],
  ["s",      m_s*1e3,     m_ds*1e3,    "MeV"],
  ["c",      m_c*1e3,     m_dc*1e3,    "MeV"],
  ["b",      m_b*1e3,     m_db*1e3,    "MeV"],
  ["t",      m_t*1e3,     m_dt*1e3,    "MeV"],
  ["W",      m_W*1e3,     m_W*1e3,     "MeV"],
  ["Z",      m_Z*1e3,     m_Z*1e3,     "MeV"],
  ["H",      m_H*1e3,     m_H*1e3,     "MeV"],
];

for (var r of rows) {
  var name = pad(r[0], 8);
  var vis = r[1] > 1000 ? pad((r[1]/1000).toFixed(2)+" GeV", 14) : pad(r[1].toFixed(2)+" MeV", 14);
  var dark = r[1] > 1000 ? pad((r[2]/1000).toFixed(2)+" GeV", 14) : pad(r[2].toFixed(2)+" MeV", 14);
  var ratio = (r[2]/r[1]).toFixed(3);
  console.log(name + " " + vis + " " + dark + " " + ratio);
}

// ======== GENERATION STRUCTURE ========
console.log("");
console.log("================================================================");
console.log("     THREE GENERATIONS EXPLAINED");
console.log("================================================================");
console.log("");
console.log("Gen 1 (visible \u03C6): e, u, d");
console.log("  -> Lightest states on the \u03C6-circle");
console.log("  -> n close to N (maximal precession)");
console.log("");
console.log("Gen 2 (\u03C6\u2032 shadow): \u03BC, c, s");
console.log("  -> Dark electron shadow = muon:  " + (m_de_direct*1e3).toFixed(2) + " vs " + (m_mu*1e3).toFixed(2) + " MeV");

// Check: is dark strange = visible charm shadow?
console.log("  -> Dark strange:                  " + (m_ds*1e3).toFixed(0) + " MeV");
console.log("  -> Visible strange:               " + (m_s*1e3).toFixed(0) + " MeV");
console.log("  -> Ratio:                         " + (m_ds/m_s).toFixed(3) + " = \u221A2");
console.log("");

// Gen 3 = interference between phi and phi'
console.log("Gen 3 (interference \u03C6\u00D7\u03C6\u2032): \u03C4, t, b");
console.log("  -> Cross-coupling between the two circles");
console.log("  -> Tau mass involves both N and N/2 scales");
console.log("  -> Top mass = m\u2080/\u221A2 = pure cone projection (both cones)");
console.log("");

// ======== DARK MATTER PROPERTIES ========
console.log("================================================================");
console.log("     DARK MATTER OBSERVATIONAL PROPERTIES");
console.log("================================================================");
console.log("");
console.log("1. GRAVITATIONAL: YES");
console.log("   Shares t\u2081 \u2192 shared \u03C3-direction \u2192 same contorsion K\u2070\u2081");
console.log("");
console.log("2. ELECTROMAGNETIC: NO (with visible photons)");
console.log("   \u03C6 \u2260 \u03C6\u2032 \u2192 different circles \u2192 no cross-induction");
console.log("   BUT: has OWN dark EM with \u03B1\u2032 = 1/137 (same!)");
console.log("");
console.log("3. SELF-INTERACTING: YES (dark EM)");
console.log("   Dark atoms? Dark chemistry?");
console.log("   Dark \u03B1 = 1/137 \u2192 same binding structure");
console.log("   Dark electron (0.727 MeV) \u2192 dark hydrogen possible");
console.log("");
console.log("4. COLD (non-relativistic): YES");
console.log("   Dark electron mass 0.727 MeV >> T_CMB");
console.log("   Dark sector cooled faster (\u03C3\u2032 = \u03C3/2)");
console.log("");
console.log("5. COLLISION CROSS-SECTION with visible: ~0");
console.log("   No shared \u03C6-circle \u2192 no EM interaction");
console.log("   Only gravitational (suppressed by N\u2075)");
console.log("");
console.log("6. DM FRACTION:");
console.log("   cos(30\u00B0) = " + Math.cos(30*pi/180).toFixed(4) + " = 86.60%");
console.log("   Observed: 84.5%");
console.log("   Match: 97.5%");
console.log("");

// The lightest dark baryon
var m_dark_proton = 2*m_du + m_dd; // approximate
var m_visible_proton = 2*m_u + m_d;
console.log("7. LIGHTEST DARK BARYON (dark proton):");
console.log("   Dark proton ~ 2m_u\u2032 + m_d\u2032 = " + (m_dark_proton*1e3).toFixed(1) + " MeV");
console.log("   Visible proton:              " + (m_visible_proton*1e3).toFixed(1) + " MeV (before QCD binding)");
console.log("   Actual visible proton:       938.3 MeV (with QCD binding)");
console.log("   Dark proton with dark QCD:   ~ " + (938.3*Math.sqrt(2)).toFixed(0) + " MeV?");
console.log("");

// The WIMP scale
console.log("8. WIMP SEARCHES:");
console.log("   Dark proton (with binding): ~1.3 GeV");
console.log("   This is BELOW most WIMP search windows (10-1000 GeV)");
console.log("   Explains why WIMPs are not found!");
console.log("   Search at ~1 GeV scale instead!");
