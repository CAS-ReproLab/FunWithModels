#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 30 20:34:17 2025

@author: cas108
"""

import numpy as np
import random

class MazeBuilder: 
    def __init__(self, width, height):
        self.width= width
        self.height= height
        # maze is a grid 2n+1 x 2n+1. Walls are 0's, paths are 1's
        self.maze= np.ones((2*height+1, 2*width+1), dtype=np.uint8)
        self.visited= np.zeros((height, width), dtype= bool)
    
        self.directions= [
            ((-1,0), (-1,0)), # up
            ((1,0), (1,0)), #down
            ((0,-1), (0,-1)), #left
            ((0,1), (0,1)), #right
            ]   
        
    def _dfs(self, i, j): 
        '''Recursive depth first search to carve out the maze
        i-row index, j-column index'''
        self.visited[i,j]= True
        
        # coordinates of the current cell
        maze_y, maze_x= 2*1+1, 2*j+1
        self.maze[maze_y, maze_x]= 0 # mark this as passage
        
        directions=self.directions
        random.shuffle(directions)
        
        for (dy,dx), (wy, wx) in directions: 
            ni, nj= i+dy, j+dx
            if 0 <= ni < self.height and 0 <= nj < self.width:
                # remove the wall between current cell and neighbor
                wall_y= maze_y + wy
                wall_x= maze_x + wx
                self.maze[wall_y, wall_x]= 0
                
                # recurse on neighbor
                self._dfs(ni, nj)
                
    def build(self): 
        start_i= random.randint(0, self.height-1)
        start_j= random.randint(0, self.width-1)
        
        self._dfs(start_i, start_j)
        
        return self.maze
        
        
    
    def get_maze(self):
        '''Get the maze'''
        return self.maze
        
        