#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 30 20:33:24 2025

@author: cas108
"""

from builder import MazeBuilder
import numpy as np

def main(): 
    width= 10
    height= 10
    
    builder= MazeBuilder(width, height)
    maze= builder.build()
    return

if __name__ == "__main__": 
    main()