# Berramdane Model V8.0 – A Mechanical Analogy for Double‑Slit Interference, Observer Effect, and Tunneling

**Author:** Al Moalim Berramdane (workshop owner, mechanical manufacturing & IT technician)  
**License:** CC BY 4.0  
**GitHub:** [https://github.com/reddoma742/Berramdane-Model-V8.0](https://github.com/reddoma742/Berramdane-Model-V8.0)  
**DOI:** (to be added)

---

## 📖 Overview

The Berramdane Model V8.0 offers a mechanical interpretation of the double‑slit experiment, the observer effect, the de Broglie relation, and tunneling. Instead of wave‑function superposition, it assumes:

- Particles (e.g., electrons) follow **helical trajectories** (spinning + forward motion).
- Friction with the slit edges generates a **transverse velocity**, turning the path into **conical wavefronts** (cones).
- Interference is not wave superposition but **mechanical interlocking of cones** from both slits.
- The observer effect is modeled as **asymmetric damping** (a simplified approximation).
- Tunneling is hybrid: `T = Gamow × drill`, where `drill = tanh(ω_spin / ω_Compton)` – a unique prediction that deviates from standard quantum mechanics by a factor of about 0.004 for slow electrons through a 0.5 nm SiO₂ barrier.

The code produces:
- A **7‑peak interference pattern** (clear and symmetric).
- A **2D real‑screen view** (vertical fringes).
- A **tunneling probability plot** vs wall density.
- An **exponential decay plot** (Gamow factor).

---

## 📁 Repository Contents

- `berramdane_v8.0.py` – Main simulation code (Python 3.8+).
- `README.md` – This file.
- `LICENSE` – CC BY 4.0.
- `examples/` – Sample figures and output (to be added).

Experimental branches (V9.x, V10.x) exploring memory accumulation and counter‑rotating cones are available separately but are not part of the stable reference.

---

## ⚙️ Requirements

- Python 3.8 or newer
- `numpy`
- `matplotlib`

Install with:
```bash
pip install numpy matplotlib
