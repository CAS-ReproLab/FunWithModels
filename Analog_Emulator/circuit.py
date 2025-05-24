#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 17 11:49:42 2025

@author: cas108
"""

import numpy as np

class Circuit: 
    def __init__(self): 
        self.components= []
        self.nodes= set()
        self.voltage_sources= []
        self.scopes= []
        
    def add_component(self, component): 
        self.components.append(component)
        
        # Try to extract nodes
        for attr in ['node1', 'node2', 'node_pos', 'node_neg']:
            if hasattr(component, attr):        
                self.nodes.add(getattr(component, attr))
        if hasattr(component, 'V'):
            self.voltage_sources.append(component)
        
        
    def simulate(self): 
        nodes= list(self.nodes - {'GND'}) # GND is reference
        node_map= {node: idx for idx, node in enumerate(nodes)}
        size= len(nodes) + len(self.voltage_sources)
        
        G= [[0.0 for _ in range(size)] for _ in range(size)]
        I= [0.0 for _ in range(size)]
        
        # Stamp passive components
        for comp in self.components:
            if hasattr(comp, 'stamp'):
                if hasattr(comp, 'V'):
                    idx = len(nodes) + self.voltage_sources.index(comp)
                    comp.stamp(G, I, node_map, idx)
                else:
                    comp.stamp(G, I, node_map)
                
        # Solve Gx = I
        G = np.array(G)
        print(G)
        I = np.array(I)
        print(I)
        x = np.linalg.solve(G, I)

        # Map results to voltages
        self.node_voltages = {'GND': 0.0}
        for node, idx in node_map.items():
            self.node_voltages[node] = x[idx]

    def print_node_voltages(self):
        print("Node Voltages:")
        for node, voltage in self.node_voltages.items():
            print(f"  {node}: {voltage:.4f} V")
            
    def oscillosopes(self, scope): 
        self.scopes.append(scope)
         
    