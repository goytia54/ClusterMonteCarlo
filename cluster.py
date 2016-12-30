# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 17:54:29 2016

@author: Michael
"""
import settings
from main import Fitfactor

'''#####################################################################################
near_neigh() determines the nearest neighbor molecules for each molecule
to be used in cluster_analyze()

cluster_analyze() uses cluster analysis to first figure out the size of each cluster
in the simulation,with the smallest cluster being two. This is done by calling
find_cluster(). The cluster is then probed, in which each molecule within the cluster is 
assigned a neighbor density which is summed at the end to determine the total density of 
all cluster. If density is greater than 50% then it is shifted towards being pure 
crystals with the greater than 80% being optimal.
#####################################################################################'''


#GLOBAL PARAMETERS USED JUST IN THIS FILE
in_cluster = [] # determines if molecule is in cluster
clusterSize = [] #array of all cluster sizes
nn = [] # number of nearest neighbor each molecule has
cluster_cl = [] # array of the actuall nearest neighbors for nn
nr_clusters = 0 #index holder 
max_nn = 6 

def near_neigh(box_dim,all_pos):    
    global nn,clusterSize,in_cluster,cluster_cl        
    mol_sig = [] #array of all sigs  
    for j in range(0,3):
        mol_sig.append(settings.sig[j])
    rc = (max(mol_sig)*2)+1 #determing the cut off raduis of neighbors
    lx = abs(float(box_dim[0][0]) - float(box_dim[0][1])) #box dimensions
    ly = abs(float(box_dim[1][0]) - float(box_dim[1][1])) #box dimensions
    num_part = len(all_pos)
    n_index = [0 for x_t in range(len(all_pos))]
    nn = [[0 for y_t in range(num_part)]for x_t in range(num_part)]
    in_cluster = [-1 for x_t in range(num_part)]
    clusterSize = [0 for x_t in range(num_part)]
    cluster_cl = [[0 for y_t in range(num_part)] for x_t in range(num_part)]

    #cycle through all molecules to build a neighbor list within the cut off radius 
    for i in range(0,len(all_pos)): # (n(n+1))/2
        for j in range(i+1,len(all_pos)): #len(g1_array) repalced with 10
            xDiff = abs(float(all_pos[i][1])-float(all_pos[j][1]))
            yDiff = abs(float(all_pos[i][2])-float(all_pos[j][2]))
            xDiff = abs(xDiff - lx * int(round(xDiff/lx))) #account for mirror image 
            yDiff = abs(yDiff - ly * int(round(yDiff/ly)))
            if xDiff**2 + yDiff**2 <= rc**2:
                nn[i][n_index[i]] = j 
                nn[j][n_index[j]] = i 
                n_index[i] += 1
                n_index[j] += 1
    return num_part,n_index
    
def cluster_analyze(num_part,all_pos,n_index):
    global nr_clusters    
    nr_clusters = 0
    a_count,b_count,ic,nic,same_nn,likeneigh = 0.0,0.0,0.0,0.0,0.0,0.0
    atomsInCluster = 0.0
    ic_index = []
    
    # Cycle through all molecules to start building the cluster lists
    for i in range(0,num_part):
        find_cluster(i,1,n_index)
    # determine the type of neighbor for each molecule and if in cluster, 3 being one handedness and 4 bein the other
    for j in range(0,nr_clusters):
    	if clusterSize[j] >= 3:
	   ic_index.append(j)
        for k in range(0,clusterSize[j]):
	    index = all_pos[cluster_cl[j][k]][0]
            if clusterSize[j] >= 3:
	        ic += 1
	    	if int(index) == 4:
                	a_count +=1
            	else:
                	b_count +=1
	    else:
	    	nic +=1 #count of atoms not in cluster
        a_count = 0
        b_count = 0
    #calculating the neighbor density of each cluster
    for l in range(0,len(ic_index)):
	atomsInCluster += clusterSize[ic_index[l]]
    	for m in range(0,clusterSize[ic_index[l]]):
	   atom_id = cluster_cl[ic_index[l]][m]
	   for n in range(0,n_index[atom_id]):
		if int(all_pos[atom_id][0]) == int(all_pos[nn[atom_id][n]][0]):
		   same_nn +=1
           likeneigh +=  same_nn/n_index[atom_id]
	   same_nn = 0.0
    fitness = Fitfactor(likeneigh/atomsInCluster,float(max(clusterSize))/float(num_part))
    return fitness
    # above returns the fitness factors: 
    # 1. fraction of like neighbors/atoms in a cluster > 75%
    # 2. largest cluster/number of particles > 30 %

def find_cluster(n,first,n_index):
    global nn,clusterSize,in_cluster,cluster_cl,nr_clusters 
    if in_cluster[n] != -1:
        return    
    nr_clusters += first # number of clusters
    cc = nr_clusters - 1 #index of current cluster
    in_cluster[n] = cc #index of particle n cluster
    cluster_cl[cc][clusterSize[cc]] = n #[cluster id][particle id]
    clusterSize[cc] += 1; #increment clustersize
    max_nn = n_index[n]    
    for i in range(0,max_nn):
        find_cluster(nn[n][i],0,n_index)
   
