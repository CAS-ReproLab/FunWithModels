#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 17 11:34:37 2025

@author: cas108
"""

import numpy as np
import matplotlib.pyplot as plt

class VoltageSource:
    
    def __init__(self, voltage, node_pos, node_neg):
        self.V= voltage
        self.node_pos= node_pos # positive node
        self.node_neg= node_neg # negative node
        
    # V_pos - V_neg = V_source    
    def stamp(self, G, I , node_map, current_index, dt = None, voltage_lookup= None):
        p= node_map.get(self.node_pos) # index for pos node
        n= node_map.get(self.node_neg) # index for neg node
        row= current_index # index for source voltage
        
        # stamp + 1 for pos terminal node
        if p is not None: 
            G[p][row]= 1 # from node p to source current
            G[row][p]= 1 # from source to node p
        # -1 for neg terminal node
        if n is not None:
            G[n][row]= -1 # from node n to source current
            G[row][n]= -1 # source to node n
        
        I[row]= self.V

        
class Resistor: 
    def __init__(self, resistance, node1, node2): 
        self.R= resistance
        self.node1= node1
        self.node2= node2
        
    def stamp(self, G, I, node_map, dt= None, Voltage_lookup= None): 
        # two nodes connected to the resistor
        n1= node_map.get(self.node1)
        n2= node_map.get(self.node2)
        conductance= 1/self.R # conductance G = 1/R
        
        # current flowing into node 1 from the resistor
        if n1 is not None: 
            G[n1][n1]+= conductance
        
        # current flowing into node 2    
        if n2 is not None: 
            G[n2][n2]+=conductance
        
        # current flowing between the two nodes    
        if n1 is not None and n2 is not None: 
            G[n1][n2]-= conductance
            G[n2][n1]-= conductance
            
class Inductor: 
    def __init__(self, inductance, node1, node2):
        self.L= inductance
        self.node1= node1
        self.node2= node2
        self.current= 0.0 # current through the inductor
        
    def stamp(self, G, I, node_map, dt, voltage_lookup): 
        n1= node_map.get(self.node1)
        n2= node_map.get(self.node2)
        
        if self.L == 0: 
            raise ValueError('Inductance must be non-zero')
        
        conductance= dt / self.L
        
        # stamp the G matrix
        if n1 is not None: 
            G[n1][n1] += conductance
        if n2 is not None:
            G[n2][n2] += conductance
        if n1 is not None and n2 is not None: 
            G[n1][n2] -= conductance
            G[n2][n1] -= conductance
            
        # stamp the 'old' inductor current
        i_old= self.current
        if n1 is not None: 
            I[n1]-= i_old
        if n2 is not None: 
            I[n2]+= i_old
            
        # update the inductor's state for the next time step
        v1= voltage_lookup.get(self.node1, 0.0)
        v2= voltage_lookup.get(self.node2, 0.0)
        
        # update the current estimate using backward Euler
        I_source= i_old + conductance * (v1- v2)
            
        # update the inductor current for the next step
        self.current= I_source
               
            
class Capacitor:
    def __init__(self, capacitance, node1, node2):
        self.C= capacitance
        self.node1= node1
        self.node2= node2
        
    def stamp(self, G, I , node_map, dt= None, voltage_lookup= None):
        n1= node_map.get(self.node1)
        n2= node_map.get(self.node2)
        Gval= self.C / dt # backward Euler conductance
        Vn1= voltage_lookup.get(self.node1, 0.0)
        Vn2= voltage_lookup.get(self.node2, 0.0)
        Ival= Gval * (Vn1 - Vn2) 
        
        if n1 is not None: 
            G[n1][n1] += Gval
            I[n1] += Ival
            
        if n2 is not None: 
            G[n2][n2] += Gval
            I[n2] -= Ival
            
        if n1 is not None and n2 is not None: 
            G[n1][n2] -= Gval
            G[n2][n1] -= Gval
         
class Diode:
    def __init__(self, node_a, node_k, I_s=1e-15, n=1.0, V_t=25e-3):
        self.node_a= node_a
        self.node_k= node_k
        self.I_s= I_s
        self.n= n
        self.V_t= V_t
        
    def stamp(self, G, I, node_map, dt=None, voltage_lookup=None):
        Va= voltage_lookup.get(self.node_a, 0.0)
        Vk= voltage_lookup.get(self.node_k, 0.0)
        Vd= Va - Vk
        
        # Diode current and small-signal conductance
        Id= self.I_s * (np.exp(Vd /( self.n * self.V_t)) - 1)
        gd= (self.I_s / (self.n * self.V_t)) * np.exp(Vd / (self.n * self.V_t))
        
        na= node_map.get(self.node_a)
        nk= node_map.get(self.node_k)
        
        # Stamp the G matrix
        if na is not None: 
            G[na][na] += gd
            if nk is not None:
                G[na][nk] -= gd
        if nk is not None: 
            G[nk][nk] += gd
            if na is not None: 
                G[nk][na] -= gd
                
        # Stamp the I vector (subtract the linearized term)
        I_term= Id - gd * Vd
        if na is not None: 
            I[na] -= I_term
        if nk is not None: 
            I[nk] += I_term
            
class Sensor:
    def __init__(self, target_source, voltage_function):
        # voltage_function is a callable F(t) that is designated in main.py
        self.target_source= target_source
        self.voltage_function= voltage_function
        
    def update(self, t): 
        # update voltage based on current time
        self.target_source.V= self.voltage_function(t)
    
            
class Oscilloscope:
    def __init__(self, node_name, signal_function=None):
        self.node= node_name
        self.signal_function= signal_function
        self.output_trace= [] # initialize a list to hold the output voltage trace
        self.input_trace= [] # initialize a list to hold the input voltage trace from the sensor
        
    # Record the voltage
    def record(self, node_voltages, time=None):
        #Record ouput signal
        if self.node in node_voltages:
            self.output_trace.append(node_voltages[self.node])
        else: 
            self.output_trace.append(None)
        
        # Record input signal if available    
        if self.signal_function is not None:
            self.input_trace.append(self.signal_function(time))
            
    def plot(self, dt):
        time= [i * dt for i in range(len(self.output_trace))] # will be same for both traces
        plt.style.use('dark_background')
        plt.plot(time, self.output_trace, label='output (V_OUT)')
        if self.signal_function is not None: 
            plt.plot(time, self.input_trace, label='Input (V_in)', linestyle='--', color='magenta')
        plt.title('Circuit Response')
        plt.xlabel('Time (s)')
        plt.ylabel('Voltage (V)')
        plt.legend()
        plt.grid(True)
        plt.show()
        
        