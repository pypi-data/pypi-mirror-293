import math
import numpy as np

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
    log_amp_var = 1.23 * ((2 * math.pi / wl)**(7 / 6)) * (cn**2) * (d**(11 / 6))
    return pt * math.exp(-log_amp_var / 2)


def polarising_loss_power(pt, theta_mis):
    l_pol = -10*math.log((math.cos(theta_mis))**2, 10)
    return pt*(10**(-l_pol/10))


def ambient_noise(pt, pn):
    return pt + pn


def beam_divergence_loss(theta, d, pt):
    divergence_factor = 1 + ((theta * d)**2)
    return pt / divergence_factor


def scintillation_loss(sigma_s, pt):
    scintillation_factor = math.exp(-(sigma_s**2) / 2)
    return pt * scintillation_factor


def calculate_received_power(p_t, d_r, d):

    p_r = p_t * (d_r / d) ** 2
    return p_r


def calculate_path_loss(p_t, p_r):

    l_p = 10 * np.log10(p_t / p_r)
    return l_p


def calculate_snr(p_r, p_0):

    snr = p_r / p_0
    return snr
