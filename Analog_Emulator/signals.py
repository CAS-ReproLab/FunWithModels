# -*- coding: utf-8 -*-
"""
Created on Mon May 26 17:17:39 2025

@author: cameron schmidt
"""

import math
import random
import numpy as np

# Constant (step) input
def constant(t, V=1.0, noise=True, sigma= 0.1):
    if noise == True:
        n_t= np.random.normal(0, sigma)
        
    if noise == False: 
        n_t= 0
        
    return V + n_t

# Step Function
def step_input(t, t0= 0.1, amplitude= 1.0): 
    return amplitude if t >= t0 else 0.0

# Sine wave
def sine_wave(t, freq= 1.0, amplitude= 1.0, offset= 0.0):
    return amplitude * math.sin(2 * math.pi * freq * t) + offset

# square wave
def square_wave(t, freq=1.0, amplitude=1.0, offset=0.0):
    period= 1.0 / freq
    return amplitude + offset if (t% period) < (period / 2) else offset

# triangle wave
def triangle_wave(t, freq=1.0, amplitude=1.0, offset=0.0):
    period= 1.0 / freq
    phase = ( t% period) / period
    val= 4 * amplitude * abs(phase - 0.5) - amplitude
    return val + offset

# ramp (linear rise)
def ramp(t, slope=1.0, t_start= 0.0):
    return slope * (t-t_start) if t >= t_start else 0.0

# pulse (single burst)
def pulse(t, t_start= 0.2, duration= 0.1, amplitude= 1.0):
    return amplitude if t_start <= t < t_start + duration else 0.0

# noise
def noise(t, amplitude= 1.0):
    return random.uniform(-amplitude, amplitude)

# Gaussian Pulse
def gaussian_pulse(t, t0=0.5, width=0.1, amplitude= 1.0, sigma= 0.1, noise= True):
    if noise == True:
        n_t= np.random.normal(0, sigma)
        
    if noise == False: 
        n_t= 0
    return amplitude * math.exp(-((t-t0) **2) / (2 * width **2)) + n_t