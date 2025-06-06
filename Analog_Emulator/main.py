#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 17 11:32:13 2025

@author: cas108
"""

from components import VoltageSource, Resistor, Capacitor, Oscilloscope, Sensor
from signals import gaussian_pulse
from circuit import Circuit

# Create the circuit
ckt= Circuit()

# Add voltage souce that starts at 0
Vsrc= VoltageSource(0.0, 'V_IN', 'GND')
ckt.add_component(Vsrc)

# attach the Sensor (voltage modulator)
# call from the list of importable functions in signals.py
signal_fn= lambda t: gaussian_pulse(t, t0=0.5, width=0.1, amplitude= 1.0, sigma= 0.1, noise= True)
mod= Sensor(Vsrc, signal_fn)
ckt.add_component(mod)

# add the RC integrator
rst= Resistor(1000, 'V_IN', 'OUT')
ckt.add_component(rst)
cpctr= Capacitor(1e-6, 'OUT', 'GND')
ckt.add_component(cpctr)

# Add oscilloscope device at OUT
osc= Oscilloscope('OUT', signal_function=None)
ckt.add_oscilloscopes(osc)

# Non-steady state simulation for time (T)
ckt.simulate_transient(dt= 0.0001, T= 2.0)


# plot the results on the oscilloscope
osc.plot(dt= 0.0001)


