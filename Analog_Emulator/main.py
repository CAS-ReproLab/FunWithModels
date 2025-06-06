#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 17 11:32:13 2025

@author: cas108
"""

from components import VoltageSource, Resistor, Capacitor, Inductor, Oscilloscope, Sensor
from signals import step_input
from circuit import Circuit

# Create the circuit
ckt= Circuit()

# Add voltage souce that starts at 0
Vsrc= VoltageSource(0.0, 'V_IN', 'GND')
ckt.add_component(Vsrc)

# attach the Sensor (voltage modulator)
# call from the list of importable functions in signals.py
signal_fn= lambda t: step_input(t, t0= 0.01, amplitude= 1.0)
mod= Sensor(Vsrc, signal_fn)
ckt.add_component(mod)

# Make an RLC circuit
rst= Resistor(100, 'V_IN', 'OUT')
ckt.add_component(rst)

ind= Inductor(1e-3, 'OUT', 'L_OUT')
ckt.add_component(ind)

cpctr= Capacitor(1e-6, 'L_OUT', 'GND')
ckt.add_component(cpctr)


# Add oscilloscope device at OUT
osc= Oscilloscope('L_OUT', signal_function=None)
ckt.add_oscilloscopes(osc)

# Non-steady state simulation for time (T)
ckt.simulate_transient(dt= 0.00001, T= 0.01)


# plot the results on the oscilloscope
osc.plot(dt= 0.00001)


