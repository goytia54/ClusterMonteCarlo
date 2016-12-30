# -*- coding: utf-8 -*-i
"""
Created on Mon May 23 16:17:44 2016

@author: Michael Goytia aka the best
"""
###I would delete this if at all possible...
from __future__ import division

import random 
import math as m
import os
from launch import *
from molecalc import *
from reader import *
from fit import *
from cluster import *
from settings import *
from hoomd_write import *
import subprocess

class Fitfactor:
     def __init__(self,cloc,clust):
        self.cloc = cloc
        self.clust = clust

def main():
	rounds = settings.rounds
    	max_inter = settings.max_inter
   	while rounds < max_inter:
        	bias = settings.bias_eps
        	if rounds % 200 == 0 and rounds > 0 and bias > 0: #decrease bia
        		settings.bias_eps = bias * 0.9
		EorS()
		xyz_results = mol_xyz(rand_angle())
		coord_results = cell_coords(*xyz_results)
		m_ID = coord_results[0]
		coord_results = coord_results[1:]
		box_dim = hoomdXML(*coord_results)
		hoomdIN()
		CMD = 'hoomd run_hoomd.py'
		subprocess.call(CMD,shell=True)
		all_pos = readTraj(m_ID)
        	num_part,n_index = near_neigh(box_dim,all_pos)  
        	fitness=cluster_analyze(num_part,all_pos,n_index)
        	fit_param(fitness)
        	settings.rounds += 1
        	rounds = settings.rounds


if __name__=="__main__":
     main()
