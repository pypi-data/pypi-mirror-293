<p align="center">
  
</p>

<h1 align="center">Freesopy</h1>

<p align="center">
  <i>A Python package for the implementation of various equations of Free Space Optical Communication</i>
</p>

<hr>


`Freesopy` is designed to simplify the implementation of various mathematical equations used in Free Space Optical Communication. It provides easy-to-use functions that can be integrated into your projects.

## Usaage

You can import `Freesopy` as:

```bash
import freesopy as fso
```
## Calculation of Losses
wl = wavelength<br>
d= distance between transmitter and receiver<br>
alpha= atmospheric attenuation coefficient<br>
dt= diameter of transmitter antenna<br>
dr = diameter of receiver antenna<br>
pt = power total<br>
pn = power of ambient noise<br>
sigma_p = standard deviation of pointing error<br>
sigma_s= standard deviation due to scintillation<br>
gamma = initial intensity of optical beam<br>cn = refractive structure parameter<br>
theta= angle of divergence<br>
theta_mis = mismatch angle divergence<br>
<br><br>
<h3>Attenuation Loss</h3>
```bash
attenuation_loss = fso.atmospheric_attenuation_loss(gamma, alpha, d)
```
<h3>Geometric Loss</h3>
```bash
geo_loss = fso.geometric_loss(dr, dt, d, wl, pt)
```
<h3>Misalignment Loss</h3>
```bash
misalignment_loss = fso.pointing_misalignment_loss(d, sigma_p, pt)
```
<h3>Atmospheric Turbulence</h3>
```bash
turbulence_loss = fso.atmospheric_turbulence(pt, cn, d, wl)
```
<h3>Polarising Loss Power</h3>
```bash
polarising_loss_power = fso.polarising_loss_power(pt, theta_mis)
```
<h3>Ambient Noise</h3>
```bash
ambient_noise = fso.ambient_noise(pt, pn)
```
<h3>Beam Divergence Loss</h3>
```bash
divergence_loss = fso.beam_divergence_loss(theta, d, pt)
```
<h3>Scintillation Loss</h3>
```bash
scintillation_loss = fso.scintillation_loss(sigma_s, pt)
```
