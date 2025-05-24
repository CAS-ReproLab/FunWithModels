#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 17 11:32:13 2025

@author: cas108
"""

from components import VoltageSource, Resistor, Capacitor, Oscilloscope

from circuit import Circuit

ckt= Circuit()

# Simple steady state divider; uses simulate()
'''
# Create a voltage dividor: 5V -> R1 -> out -> R2 -> GND
ckt.add_component(VoltageSource(5.0, 'V+', 'GND'))
ckt.add_component(Resistor(1000, 'V+', 'OUT'))
ckt.add_component(Resistor(2000, 'OUT', 'GND'))
'''

# Analog Integrator Vrsc -> R -> node -> C -> GND
ckt.add_component(VoltageSource(1.0, 'V_IN', 'GND')) # step input
ckt.add_component(Resistor(1000, 'V_IN', 'OUT')) # 1 kilaOhm resistance
ckt.add_component(Capacitor(1e-6, 'OUT', 'GND')) # 1 micro Faraday capacitance

# Add oscilloscope device at OUT
osc= Oscilloscope('OUT')
ckt.add_oscilloscopes(osc)

'''
# Simulate the simple divider circuit at steady state
ckt.simulate()

# print results
ckt.print_node_voltages()
'''

# Non-steady state simulation for 50 ms
ckt.simulate_transient(dt= 0.001, T= 0.05)


print("Number of samples recorded:", len(osc.trace))
print("First 10 values:", osc.trace[:10])

# plot the results on the oscilloscope
osc.plot(dt= 0.001)


