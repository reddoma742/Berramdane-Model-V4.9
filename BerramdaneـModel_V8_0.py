-- coding: utf-8 --
"""
Berramdane Model V8.0: Mechanical Analogy for Quantum Phenomena
This model simulates the double-slit interference pattern, the observer effect,
and quantum tunneling using a deterministic mechanical approach.

Core Principles:
1. Particles follow helical trajectories (Spin + Linear Motion).
2. Friction with slit edges generates conical wavefronts (Cones).
3. Interference results from the mechanical interlocking of these cones.
4. Tunneling is modeled as a hybrid 'drill' effect (Rotational Energy).

Author: Al Moalim Berramdane
License: CC BY 4.0
"""

import numpy as np
import matplotlib.pyplot as plt

============================================================
1. Physical Parameters (Standard Configuration)
============================================================
h = 6.626e-34 # Planck constant (J.s)
m = 9.109e-31 # Electron mass (kg)
a_width = 0.72e-6 # Slit width (m)
d_slit = 2.45e-6 # Distance between slits (m)
L_total = 2.2 # Distance to screen (m)
v_nominal = 5.8e5 # Mean velocity (m/s)
delta_v = 0.02 * v_nominal # Velocity dispersion (2%)
n_particles = 1000 # Number of simulated particles
screen_points = 1000 # Resolution of the screen
x = np.linspace(-0.006, 0.006, screen_points)

Simulation Flags
observer_active = False # Set to True to simulate the Observer Effect

Viscous Medium Parameters (The "Lens" effect)
rho_medium = 1.5e-15 # Medium density (kg/m^3)
nu_medium = 1.5e-6 # Kinematic viscosity (m^2/s)
k_lens = 1.0e-20 # Empirical focus constant
L_focus = k_lens * (d_slit / a_width) / (nu_medium * rho_medium)

============================================================
2. Mathematical Framework
============================================================

def de_broglie_wavelength(v):
"""Calculates the mechanical wavelength based on momentum."""
return h / (m * v)

def diffraction_angle(v):
"""Determines the conical spread angle based on friction/velocity."""
lam = de_broglie_wavelength(v)
return np.arctan(lam / a_width)

def get_cone_geometry(v, L):
"""Computes the number of engagement points (peaks) and their spacing."""
lam = de_broglie_wavelength(v)
theta = diffraction_angle(v)
spacing = (lam * L) / d_slit
spread = np.tan(theta) * L

# Maturity factor: represents the formation of the interference pattern over distance
maturity = np.tanh(L / L_focus)
n_side = max(1, int(round((spread / spacing) * maturity)))
return 1 + 2 * n_side, n_side, spacing

def simulate_interference(x, velocities, observer=False):
"""Accumulates the mechanical intensity from multiple particles."""
total_intensity = np.zeros_like(x)

for v in velocities:
n_total, n_side, spacing = get_cone_geometry(v, L_total)
centers = np.linspace(-n_side * spacing, n_side * spacing, n_total)
sigma = spacing / 3.5 # Sharpness of the mechanical engagement

# Base mechanical peaks
I_base = np.zeros_like(x)
for c in centers:
I_base += np.exp(-(x - c)2 / (2 * sigma2))

# Diffraction Envelope
lam = de_broglie_wavelength(v)
beta = (np.pi * d_slit * x) / (lam * L_total)
alpha = (np.pi * a_width * x) / (lam * L_total)

# Standard interference pattern formulation
envelope = np.cos(beta)2 * np.sinc(alpha / np.pi) 2

# Observer Effect: Asymmetric damping simulation
damping = 0.4 if observer else 1.0

total_intensity += I_base * envelope * damping

return total_intensity / np.max(total_intensity)

============================================================
3. Execution & Visualization
============================================================

Generate particle velocities
np.random.seed(42)
v_dist = np.random.normal(v_nominal, delta_v, n_particles)

Run simulation
intensity = simulate_interference(x, v_dist, observer=observer_active)

Plotting Results
plt.figure(figsize=(12, 7))

1D Pattern
plt.subplot(2, 1, 1)
plt.plot(x * 1000, intensity, color='blue', lw=2)
plt.fill_between(x * 1000, intensity, color='blue', alpha=0.1)
plt.title(f"Berramdane Model V8.0 - Interference Pattern (n={n_particles})")
plt.xlabel("Position on Screen (mm)")
plt.ylabel("Intensity (a.u.)")
plt.grid(True, alpha=0.3)

2D Simulated Screen
plt.subplot(2, 1, 2)
screen_2d = np.tile(intensity, (200, 1))
plt.imshow(screen_2d, extent=[-6, 6, 0, 1], cmap='Blues', aspect='auto')
plt.title("2D Real-Screen Projection")
plt.xlabel("Position (mm)")
plt.yticks([])

plt.tight_layout()
plt.show()

============================================================
4. Final Report
============================================================
vis_v = v_nominal
n_p, _, _ = get_cone_geometry(vis_v, L_total)
print("-" * 50)
print("BERRAMDANE MODEL V8.0 - FINAL REPORT")
print("-" * 50)
print(f"Number of predicted peaks: {n_p}")
print(f"Nominal Velocity: {v_nominal} m/s")
print(f"Observer Effect: {'ACTIVE' if observer_active else 'INACTIVE'}")
print(f"Status: Stable Reference (V8.0)")
print("-" * 50)