#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 17 11:32:13 2025

@author: cas108
"""

from components import VoltageSource, Resistor, Capacitor, Oscilloscope, Sensor

from circuit import Circuit

import math

# Define the time varying input signal at the voltage source
def sensor_input(t):
    return 0.5 * math.sin(2 * math.pi * 1 * t) + 0.5 # oscillates from 0 to 1V

# Create the circuit
ckt= Circuit()

# Add voltage souce that starts at 0
Vsrc= VoltageSource(0.0, 'V_IN', 'GND')
ckt.add_component(Vsrc)

# attach the Sensor (voltage modulator)
mod= Sensor(Vsrc, sensor_input)
ckt.add_component(mod)

# add the RC integrator
rst= Resistor(1000, 'V_IN', 'OUT')
ckt.add_component(rst)
cpctr= Capacitor(1e-6, 'OUT', 'GND')
ckt.add_component(cpctr)

# Add oscilloscope device at OUT
osc= Oscilloscope('OUT')
ckt.add_oscilloscopes(osc)

# Non-steady state simulation for 10 ms
ckt.simulate_transient(dt= 0.0001, T= 1.0)


# plot the results on the oscilloscope
osc.plot(dt= 0.001)


