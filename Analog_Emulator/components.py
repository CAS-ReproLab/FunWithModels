#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 17 11:34:37 2025

@author: cas108
"""

class VoltageSource:
    
    def __init__(self, voltage, node_pos, node_neg):
        self.V= voltage
        self.node_pos= node_pos
        self.node_neg= node_neg
        
    def stamp(self, G, I , node_map, current_index):
        p= node_map.get(self.node_pos)
        n= node_map.get(self.node_neg)
        row= current_index
        
        if p is not None: 
            G[p][row]= 1
            G[row][p]= 1
        
        if n is not None:
            G[n][row]= -1
            G[row][n]= -1
        
        I[row]= self.V

        
class Resistor: 
    def __init__(self, resistance, node1, node2): 
        self.R= resistance
        self.node1= node1
        self.node2= node2
        
    def stamp(self, G, I, node_map): 
        n1= node_map.get(self.node1)
        n2= node_map.get(self.node2)
        conductance= 1/self.R
        
        
        if n1 is not None: 
            G[n1][n1]+= conductance
            
        if n2 is not None: 
            G[n2][n2]+=conductance
            
        if n1 is not None and n2 is not None: 
            G[n1][n2]-= conductance
            G[n2][n1]-= conductance
        