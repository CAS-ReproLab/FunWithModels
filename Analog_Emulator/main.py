#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 17 11:32:13 2025

@author: cas108
"""

from components import VoltageSource, Resistor, Capacitor, Inductor, Diode, Oscilloscope, Sensor
from signals import pulse
from circuit import Circuit

# Create the circuit
ckt= Circuit()

# Add voltage souce that starts at 0
Vsrc= VoltageSource(0.0, 'V_IN', 'GND')
ckt.add_component(Vsrc)


# attach the Sensor (voltage modulator)
# call from the list of importable functions in signals.py
signal_fn= lambda t: pulse(t, t_start= 1e-4, duration= 0.1, amplitude= 1.0)
mod= Sensor(Vsrc, signal_fn)
ckt.add_component(mod)


# Add a resistor
rst= Resistor(0.1, 'V_IN', 'RES') # Ohms
ckt.add_component(rst)



# Add an inductor
ind= Inductor(0.25, 'RES', 'C_OUT') # Henrys
ckt.add_component(ind)



# Add a capacitor
cpctr= Capacitor(0.5, 'C_OUT', 'GND') # Farads
ckt.add_component(cpctr)

'''
# Add a diode
dde= Diode('NODE', 'GND', I_s= 1e-15, n= 1.0, V_t= 25e-3)
ckt.add_component(dde)
'''

# Add oscilloscope device at OUT
osc= Oscilloscope('C_OUT', signal_function=signal_fn)
ckt.add_oscilloscopes(osc)

# Non-steady state simulation for time (T)
ckt.simulate_transient(dt= 1e-3, T= 10)


# plot the results on the oscilloscope
osc.plot(dt= 1e-3)


