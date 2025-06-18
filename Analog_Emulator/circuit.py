#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 17 11:49:42 2025

@author: cas108
"""

import numpy as np
from components import Capacitor


class Circuit: 
    def __init__(self): 
        self.components= []
        self.nodes= set()
        self.voltage_sources= []
        self.scopes= []
        
    def add_component(self, component): 
        self.components.append(component)
        
        # Try to extract nodes
        for attr in ['node1', 'node2', 'node_pos', 'node_neg', 'node_a', 'node_k']:
            if hasattr(component, attr):        
                self.nodes.add(getattr(component, attr))
        if hasattr(component, 'V'):
            self.voltage_sources.append(component)

    def simulate_transient(self, dt= 0.001, T= 0.05):
        steps= int(T / dt)
        nodes= sorted(self.nodes - {'GND'})
        node_map= {node: idx for idx, node in enumerate(nodes)}
        size= len(nodes) + len(self.voltage_sources)
        
        # Set the initial conditions
        voltage_lookup= {node: 0.0 for node in nodes}
        self.node_voltages= {'GND': 0.0}
        x_prev= np.zeros(size)
        
        for step in range(steps): 
            time= step * dt # current simulation time
            
            # update time dependent components
            for comp in self.components: 
                # update sensor driven voltages
                if hasattr(comp, 'update'): 
                    comp.update(time)
            
            # Newton-Raphson solver for nonlinear stamps
            x= x_prev.copy()
            for _ in range(20): 
                # Rebuild MNA matrices
                G= [[0.0] * size for _ in range(size)]
                I= [0.0] * size
            
            # build MNA stamps
                for comp in self.components:    
                    # only stamp components that have a stamp() method
                    if hasattr(comp, 'stamp'):
                        if isinstance(comp, Capacitor):
                            comp.stamp(G, I, node_map, dt, voltage_lookup)
                        elif hasattr(comp, 'V'):
                            idx= len(nodes) + self.voltage_sources.index(comp)
                            comp.stamp(G, I, node_map, idx)
                        else: 
                            comp.stamp(G, I, node_map, dt, voltage_lookup) # changes dt, voltage_lookup
                
                      
                G= np.array(G) # convert to numpy array to solve wiht linalg
                I= np.array(I)
            
                # residual and correction
                res= I - G.dot(x)
                dx= np.linalg.solve(G, res)
                x += dx
            
                if np.linalg.norm(dx, np.inf) < 1e-6:
                    break
        
            # accept converged solution            
            x_prev= x
        
                # commit voltages for this timestep
            for node, idx in node_map.items(): 
                voltage_lookup[node]= x_prev[idx]
                self.node_voltages[node]= x_prev[idx]
            self.node_voltages['GND']= 0.0
        
            # record with oscilloscope if in circuit
            for scope in self.scopes:
                scope.record(self.node_voltages, time= time)
            
        
    def print_node_voltages(self):
        print("Node Voltages:")
        for node, voltage in self.node_voltages.items():
            print(f"  {node}: {voltage:.4f} V")
            
    def add_oscilloscopes(self, scope): 
        self.scopes.append(scope)
         
    