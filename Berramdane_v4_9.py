# -*- coding: utf-8 -*-
"""
Berramdane Model V4.9 – Final Video Version
نموذج "بالرمضان" – تفسير ميكانيكي لتجربة الشقين، تأثير المراقب، والتشابك
Author: Al Moalim Berramdane (CC BY 4.0)
"""

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 1. المعاملات الأساسية (Parameters)
# ============================================================
h = 6.626e-34          # Planck constant
m = 9.1e-31            # Electron mass
rho_m = 1.5e-15        # Medium density
v_nominal = 1.2e6      # Central forward velocity (m/s)
d_slit = 1.2e-6        # Slit separation (m)
a_width = 0.2e-6       # Slit width (m)
L_total = 1.2          # Distance from slits to screen (m)
nu_medium = 1.5e-6     # Kinematic viscosity (m²/s)

# Lens constant (makes L_focus ~ 1 m for lab scale)
k_lens = 3.75e-21
L_focus = k_lens * (d_slit / a_width) / (nu_medium * rho_m)

# Beam velocity dispersion
n_velocities = 100
delta_v = 0.04e6

# ============================================================
# 2. Scene selection (اختيار المشهد)
# ============================================================
# Change this to "full", "observer_only", or "observer_magnetic"
scene = "observer_magnetic"

# Observer settings (used if scene != "full")
observer_active = True
observer_side = 'right'       # 'right' or 'left'
observer_strength = 0.95

# Magnetic splitting (used if scene == "observer_magnetic")
use_magnetic_splitting = True
B_field = 0.01                # Tesla

# ============================================================
# 3. Core functions
# ============================================================
def get_lens_physics(v_par, dist):
    # Transverse velocity due to friction (simplified)
    v_perp = (0.3 * 1e-12 / m) * (1e-12 / v_par)
    v_total = np.sqrt(v_par**2 + v_perp**2)
    maturity = np.tanh(dist / L_focus)
    lens_quality = np.clip(1.0 - (a_width / 1e-6), 0.1, 1.0) * maturity
    lam = h / (m * v_total) / (1 + 5e-3 * rho_m * v_total**2)
    return lam, lens_quality

def magnetic_splitting(x, lam, L):
    if not use_magnetic_splitting or B_field == 0:
        return 0
    shift = 0.0005 * B_field * (lam / 1e-9)
    return shift

def simulate_pattern():
    x = np.linspace(-0.003, 0.003, 1500)
    velocities = np.random.normal(v_nominal, delta_v, n_velocities)
    velocities = np.clip(velocities, v_nominal - 3*delta_v, v_nominal + 3*delta_v)
    total_intensity = np.zeros_like(x)

    for v in velocities:
        lam, qual = get_lens_physics(v, L_total)
        beta = (np.pi * d_slit * x) / (lam * L_total)
        alpha = (np.pi * a_width * x) / (lam * L_total)
        I_base = (np.cos(beta)**2 * np.sinc(alpha / np.pi)**2) * qual

        # Magnetic splitting (if enabled)
        shift = magnetic_splitting(x, lam, L_total)
        if shift != 0:
            I_shifted_right = np.interp(x + shift, x, I_base, left=0, right=0)
            I_shifted_left = np.interp(x - shift, x, I_base, left=0, right=0)
            I_mag = 0.5 * (I_shifted_right + I_shifted_left)
            I_base = 0.7 * I_base + 0.3 * I_mag

        # Observer effect (asymmetric, if scene != "full")
        if scene != "full" and observer_active:
            mask = np.ones_like(x)
            if observer_side == 'right':
                mask[x > 0] = 1 - observer_strength
            else:
                mask[x < 0] = 1 - observer_strength
            I_base *= mask

        total_intensity += I_base

    total_intensity /= len(velocities)
    total_intensity /= np.max(total_intensity)
    return x, total_intensity

# ============================================================
# 4. Run simulation and plot
# ============================================================
x_axis, intensity = simulate_pattern()

plt.figure(figsize=(12, 5))

# 1D pattern
plt.subplot(1, 2, 1)
plt.plot(x_axis * 1000, intensity, 'b-', lw=2)
plt.fill_between(x_axis * 1000, intensity, alpha=0.3)
title = f'Berramdane Model V4.9 – {scene}\nL_focus = {L_focus:.2f} m'
plt.title(title)
plt.xlabel('Position (mm)')
plt.ylabel('Intensity (a.u.)')
plt.grid(True, alpha=0.3)

# 2D real‑screen view
plt.subplot(1, 2, 2)
screen_2d = np.tile(intensity, (200, 1))
plt.imshow(screen_2d, cmap='Blues', aspect='auto', extent=[-3, 3, 0, 1])
plt.colorbar(label='Intensity')
plt.title('Real screen view')
plt.xlabel('Position (mm)')
plt.yticks([])

plt.tight_layout()
plt.show()

# ============================================================
# 5. Console report
# ============================================================
print("="*60)
print("Berramdane Model V4.9 – Final Video Version")
print(f"Scene: {scene}")
if scene != "full":
    print(f"Observer side: {observer_side}, strength: {observer_strength}")
if use_magnetic_splitting and B_field > 0:
    print(f"Magnetic field: {B_field} T (splitting enabled)")
print(f"L_focus = {L_focus:.4f} m")
print("Model is local (Bell S=2). Non-locality remains open.")
print("="*60)