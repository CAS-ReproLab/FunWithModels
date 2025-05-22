#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 17 11:32:13 2025

@author: cas108
"""

from components import VoltageSource
from components import Resistor
from circuit import Circuit

# Create a circuit
ckt= Circuit()

# Create a voltage dividor: 5V -> R1 -> out -> R2 -> GND
ckt.add_component(VoltageSource(5.0, 'V+', 'GND'))
ckt.add_component(Resistor(1000, 'V+', 'OUT'))
ckt.add_component(Resistor(2000, 'OUT', 'GND'))

# Simulate
ckt.simulate()

# print results
ckt.print_node_voltages()

