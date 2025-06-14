#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 17 11:32:13 2025

@author: cas108
"""

from components import VoltageSource, Resistor, Capacitor, Inductor, Oscilloscope, Sensor
from signals import pulse
from circuit import Circuit

# Create the circuit
ckt= Circuit()

# Add voltage souce that starts at 0
Vsrc= VoltageSource(0.0, 'V_IN', 'GND')
ckt.add_component(Vsrc)

# attach the Sensor (voltage modulator)
# call from the list of importable functions in signals.py
signal_fn= lambda t: pulse(t, t_start= 0.1e-4, duration= .1, amplitude= 1.0)
mod= Sensor(Vsrc, signal_fn)
ckt.add_component(mod)

'''
# Add a resistor
rst= Resistor(100, 'V_IN', 'OUT') # Ohms
ckt.add_component(rst)
'''
# Add an inductor
ind= Inductor(0.25, 'V_IN', 'OUT') # Henrys
ckt.add_component(ind)

# Add a capacitor
cpctr= Capacitor(0.5, 'OUT', 'GND') # Farads
ckt.add_component(cpctr)


# Add oscilloscope device at OUT
osc= Oscilloscope('OUT', signal_function=signal_fn)
ckt.add_oscilloscopes(osc)

# Non-steady state simulation for time (T)
ckt.simulate_transient(dt= 1e-3, T= 4)

# plot the results on the oscilloscope
osc.plot(dt= 1e-3)


