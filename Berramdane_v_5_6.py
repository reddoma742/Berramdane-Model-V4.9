# -*- coding: utf-8 -*-
"""
Berramdane Model V5.6 – Final Corrected Version (Fraunhofer spacing fix)
Author: Al Moalim Berramdane (CC BY 4.0)
"""

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 1. Fundamental constants and geometry
# ============================================================
h = 6.626e-34
hbar = h / (2 * np.pi)
m = 9.109e-31
c = 3e8
m_c2 = m * c**2
omega_Compton = m_c2 / hbar

a_width = 0.2e-6          # slit width (m)
d_slit = 1.2e-6           # slit separation (m)
L_total = 1.2              # distance to screen (m)

v_nominal = 1.2e6
delta_v = 0.04e6
n_velocities = 100

rho_medium = 1.5e-15
nu_medium = 1.5e-6
k_lens = 3.75e-21
L_focus = k_lens * (d_slit / a_width) / (nu_medium * rho_medium)

observer_active = True
observer_side = 'right'
observer_strength = 0.95

use_magnetic_splitting = True
B_field = 0.01

wall_density = 0.8
barrier_thickness = 2e-9
V0_max = 3.1 * 1.6e-19
V0_min = 0.0
electron_energy = 1.0 * 1.6e-19

# ============================================================
# 2. Core functions
# ============================================================
def de_broglie_wavelength(v_par):
    return h / (m * v_par)

def diffraction_angle(v_par):
    lam = de_broglie_wavelength(v_par)
    return np.arctan(a_width / lam)

def number_of_cones(v_par, L):
    lam = de_broglie_wavelength(v_par)
    theta = diffraction_angle(v_par)
    tan_theta = np.tan(theta)
    n_side_float = tan_theta * d_slit / lam
    maturity = np.tanh(L / L_focus)
    n_side_float *= maturity
    n_side = max(1, int(round(n_side_float)))
    n_side = min(n_side, 15)
    return 1 + 2 * n_side, n_side

def cone_centers(v_par, L):
    lam = de_broglie_wavelength(v_par)
    spacing = lam * L / d_slit   # correct Fraunhofer spacing
    _, n_side = number_of_cones(v_par, L)
    centers = np.linspace(-n_side * spacing, n_side * spacing, 2*n_side + 1)
    return centers, spacing

def effective_wavelength(v_par, dist):
    lam = de_broglie_wavelength(v_par)
    n_eff = 1 + 5e-3 * rho_medium * v_par**2
    lam /= n_eff
    maturity = np.tanh(dist / L_focus)
    lens_quality = np.clip(1.0 - (a_width / 1e-6), 0.1, 1.0) * maturity
    return lam, lens_quality

def cone_intensity(x, center, sigma):
    return np.exp(-(x - center)**2 / (2 * sigma**2))

def double_slit_intensity(x, v_par, L):
    centers, spacing = cone_centers(v_par, L)
    lam, qual = effective_wavelength(v_par, L)
    sigma = spacing / 2.5

    I_base = np.zeros_like(x)
    for c in centers:
        I_base += cone_intensity(x, c, sigma)

    beta = (np.pi * d_slit * x) / (lam * L)
    alpha = (np.pi * a_width * x) / (lam * L)
    envelope = np.cos(beta)**2 * np.sinc(alpha / np.pi)**2
    I = I_base * envelope * qual

    if use_magnetic_splitting and B_field != 0:
        shift = 0.0005 * B_field * (lam / 1e-9)
        I_right = np.interp(x + shift, x, I, left=0, right=0)
        I_left  = np.interp(x - shift, x, I, left=0, right=0)
        I_mag = 0.5 * (I_right + I_left)
        I = 0.7 * I + 0.3 * I_mag

    if observer_active:
        mask = np.ones_like(x)
        if observer_side == 'right':
            mask[x > 0] = 1 - observer_strength
        else:
            mask[x < 0] = 1 - observer_strength
        I *= mask

    return I, len(centers)

def tunneling_probability(v_par, V0, thickness):
    E_kin = 0.5 * m * v_par**2
    if E_kin >= V0:
        return 1.0
    kappa = np.sqrt(2 * m * (V0 - E_kin)) / hbar
    gamow = np.exp(-2 * kappa * thickness)
    omega_spin = 2 * np.pi * a_width * m**2 * v_par**3 / h**2
    drill = np.tanh(omega_spin / omega_Compton)
    return gamow * drill

# ============================================================
# 3. Simulation
# ============================================================
x = np.linspace(-0.003, 0.003, 1500)
velocities = np.random.normal(v_nominal, delta_v, n_velocities)
velocities = np.clip(velocities, v_nominal - 3*delta_v, v_nominal + 3*delta_v)

total_intensity = np.zeros_like(x)
cone_counts = []
for v in velocities:
    I_v, n_cones = double_slit_intensity(x, v, L_total)
    total_intensity += I_v
    cone_counts.append(n_cones)
total_intensity /= n_velocities
total_intensity /= np.max(total_intensity)
avg_n_cones = np.mean(cone_counts)

I_max = np.max(total_intensity)
center_idx = np.argmin(np.abs(x))
I_min = np.min(total_intensity[center_idx-50:center_idx+50])
visibility = (I_max - I_min) / (I_max + I_min) if (I_max+I_min)>0 else 0

v_par = np.sqrt(2 * electron_energy / m)
V0_eff = V0_min + wall_density * (V0_max - V0_min)
prob_model = tunneling_probability(v_par, V0_eff, barrier_thickness)
kappa_qm = np.sqrt(2 * m * (V0_eff - electron_energy)) / hbar
prob_qm = np.exp(-2 * kappa_qm * barrier_thickness)
omega_spin = 2 * np.pi * a_width * m**2 * v_par**3 / h**2
drill = np.tanh(omega_spin / omega_Compton)

# ============================================================
# 4. Plots
# ============================================================
plt.figure(figsize=(14, 10))

plt.subplot(2, 2, 1)
plt.plot(x*1000, total_intensity, 'b-', lw=2)
plt.fill_between(x*1000, total_intensity, alpha=0.3)
plt.title(f'Double-slit (V5.6)\nvisibility {visibility:.1%}, avg cones = {avg_n_cones:.1f}')
plt.xlabel('Position (mm)')
plt.ylabel('Intensity (a.u.)')
plt.grid(True, alpha=0.3)

plt.subplot(2, 2, 2)
screen = np.tile(total_intensity, (200, 1))
plt.imshow(screen, cmap='Blues', aspect='auto', extent=[-3, 3, 0, 1])
plt.colorbar(label='Intensity')
plt.title('Real screen view')
plt.xlabel('Position (mm)')
plt.yticks([])

densities = np.linspace(0, 1, 200)
probs = []
for d in densities:
    V = V0_min + d * (V0_max - V0_min)
    probs.append(tunneling_probability(v_par, V, barrier_thickness))
plt.subplot(2, 2, 3)
plt.plot(densities, probs, 'r-', lw=2)
plt.xlabel('Wall density')
plt.ylabel('Tunneling probability')
plt.title('Mechanical tunneling (drill effect)')
plt.grid(True, alpha=0.3)

thicknesses = np.linspace(0.5e-9, 5e-9, 100)
prob_thick = [tunneling_probability(v_par, V0_eff, t) for t in thicknesses]
plt.subplot(2, 2, 4)
plt.semilogy(thicknesses*1e9, prob_thick, 'g-', lw=2)
plt.xlabel('Thickness (nm)')
plt.ylabel('Probability')
plt.title('Gamow exponential decay')
plt.grid(True, alpha=0.3)

plt.suptitle('Berramdane Model V5.6 – Final Corrected (Fraunhofer spacing)', fontsize=14)
plt.tight_layout()
plt.show()

# ============================================================
# 5. Console report
# ============================================================
print("="*70)
print("Berramdane Model V5.6 – Final Corrected Version")
print("="*70)
print(f"Slit width: {a_width*1e6:.2f} µm, separation: {d_slit*1e6:.2f} µm")
print(f"Screen distance: {L_total:.1f} m, Focus distance: {L_focus:.4f} m")
print(f"Average number of cones (peaks): {avg_n_cones:.1f}")
print(f"Fringe visibility: {visibility:.1%}")
print(f"Tunneling drill factor: {drill:.3e}")
print(f"Ratio model/QM: {prob_model/prob_qm:.3f}")
print("\nKey correction: spacing = lam * L / d_slit (standard Fraunhofer).")
print("="*70)