#for testing
def hello(num):
    print(num)
    return num
#actual
import math

"""wl = wavelength"""
"""d= distance between transmitter and receiver"""
"""alpha= atmospheric attenuation coefficient"""
"""dt= diameter of transmitter antenna"""
"""dr = diameter of receiver antenna"""
"""pt = power total"""
"""pn = power of ambient noise"""
"""sigma_p = standard deviation of pointing error"""
"""sigma_s= standard deviation due to scintillation"""
"""gamma = initial intensity of optical beam"""
"""cn = refractive structure parameter"""
"""theta= angle of divergence"""
"""theta_mis = mismatch angle divergence"""


def atmospheric_attenuation_loss(gamma, alpha, d):
  return gamma * math.exp(-alpha * d)


def geometric_loss(dr, dt, d, wl, pt):
  return pt * (((dr * wl) / (dt * 4 * math.pi * d))**2)


def pointing_misalignment_loss(d, sigma_p, pt):
  return pt * math.exp(-(d * d) / (2 * sigma_p**2))


def atmospheric_turbulence(pt, cn, d, wl):
  """log_amp_var= log amplitude variance"""
  log_amp_var = 1.23 * ((2 * math.pi / wl)**(7 / 6)) * (cn**2) * (d**(11 / 6))
  return pt * math.exp(-log_amp_var / 2)


def polarising_loss_power(pt, theta_mis):
  """l_pol = polarising loss"""
  l_pol = -10*math.log((math.cos(theta_mis))**2,10)
  return pt*(10**(-l_pol/10))


def ambient_noise(pt, pn):
  return pt + pn


def beam_divergence_loss(theta, d, pt):
  divergence_factor = 1 + ((theta * d)**2)
  return pt / divergence_factor


def scintillation_loss(sigma_s, pt):
  scintillation_factor = math.exp(-(sigma_s**2) / 2)
  return pt * scintillation_factor

import numpy as np

def calculate_received_power(P_t, D_r, d):
    """
    Calculate the received power in an indoor FSO communication system.

    Parameters:
    - P_t: Transmitted power in mW
    - D_r: Receiver aperture diameter in meters
    - d: Distance between transmitter and receiver in meters

    Returns:
    - P_r: Received power in mW
    """
    P_r = P_t * (D_r / d) ** 2
    return P_r

def calculate_path_loss(P_t, P_r):
    """
    Calculate the path loss in an indoor FSO communication system.

    Parameters:
    - P_t: Transmitted power in mW
    - P_r: Received power in mW

    Returns:
    - L_p: Path loss in dB
    """
    L_p = 10 * np.log10(P_t / P_r)
    return L_p

def calculate_snr(P_r, N_0):
    """
    Calculate the Signal-to-Noise Ratio (SNR) in an indoor FSO communication system.

    Parameters:
    - P_r: Received power in mW
    - N_0: Noise power spectral density in mW/Hz

    Returns:
    - SNR: Signal-to-Noise Ratio (unitless)
    """
    SNR = P_r / N_0
    return SNR