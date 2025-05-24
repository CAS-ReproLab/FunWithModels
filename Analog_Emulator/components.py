#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 17 11:34:37 2025

@author: cas108
"""

class VoltageSource:
    
    def __init__(self, voltage, node_pos, node_neg):
        self.V= voltage
        self.node_pos= node_pos # positive node
        self.node_neg= node_neg # negative node
        
    # V_pos - V_neg = V_source    
    def stamp(self, G, I , node_map, current_index):
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
        
    def stamp(self, G, I, node_map): 
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
            
class Capacitor:
    def __init__(self, capacitance, node1, node2):
        self.C= capacitance
        self.node1= node1
        self.node2= node2
        self.v_prev= 0.0 #voltage across the capacitor at the previous timestep
        
    def stamp(self, G, I , node_map, dt, voltage_lookup):
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
        
            
class Oscilloscope:
    def __init__(self, node_name):
        self.node= node_name
        self.trace= [] # initialize the set to hold the voltage trace
    
    # Record the voltage
    def record(self, node_voltages):
        if self.node in node_voltages:
            self.trace.append(node_voltages[self.node])
        else: 
            self.trace.append(None)
            
    def plot(self, dt):
        import matplotlib.pyplot as plt
        time= [i * dt for i in range(len(self.trace))]
        plt.plot(time, self.trace)
        plt.title('Voltage at node')
        plt.xlabel('Time (s)')
        plt.ylabel('Voltage (V)')
        plt.grid(True)
        plt.show()
        
        