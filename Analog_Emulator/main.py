#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 17 11:32:13 2025

@author: cas108
"""

from components import VoltageSource, Resistor, Capacitor, Inductor, Diode, Oscilloscope, Transistor, Sensor
from signals import pulse
from circuit import Circuit

# Create the circuit
ckt= Circuit()

# DC supply: VCC = 5 V
Vsrc= VoltageSource(5.0, 'VCC', 'GND')
ckt.add_component(Vsrc)

# Collector resistor node VCC to node C
rc= Resistor(2e3, 'VCC', 'C') # Ohms
ckt.add_component(rc)


# Base resistor node VCC to node B
rb= Resistor(1e5, 'VCC', 'B') # Ohms
ckt.add_component(rb)

# Transistor: collector = C, base = B, emitter = GND
q1= Transistor('C', 'B', 'GND')
ckt.add_component(q1)

# input source at the transistor base (starts at 0 V)
vin= VoltageSource(0.0, 'B', 'GND')
ckt.add_component(vin)

# Step input to the transistor
step_fn= lambda t: pulse(t, t_start= 0.5e-3, duration= 2e-3, amplitude= 0.7)
sensor_in= Sensor(vin, voltage_function=step_fn)
ckt.add_component(sensor_in)

# Add oscilloscope device at the collector
osc= Oscilloscope('C', signal_function=step_fn)
ckt.add_oscilloscopes(osc)

# Non-steady state simulation for time (T)
ckt.simulate_transient(dt= 1e-6, T= 2e-3)


# Static plot of the results on the oscilloscope
osc.plot(dt= 1e-6)

# Animated plot of the results on the oscilloscope
#osc.plot_anim(dt= 1e-3, filename='Oscilloscope.mp4', frame_skip=10, playback_fps=10, interval_ms=30)

