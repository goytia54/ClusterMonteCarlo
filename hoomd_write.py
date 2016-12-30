# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 12:23:48 2016

@author: Michael
"""

import settings
import math as m

def hoomdXML(strings,lx,ly):
    d_file = settings.d_file
    datafile = open(d_file,'w')
    datafile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<hoomd_xml version=\"1.4\">\n<configuration time_step=\"0\" dimensions=\"2\">\n")
    datafile.write("<box Lx=\""+str(lx)+"\" Ly=\""+str(ly)+"\" Lz=\"5\"/>\n")
    datafile.write("<position>\n"+strings[0]+"</position>\n")
    datafile.write("<type>\n"+strings[1]+"</type>\n")
    datafile.write("<body>\n"+strings[2]+"</body>\n")
    datafile.write("<diameter>\n"+strings[3]+"</diameter>\n")
    datafile.write("<mass>\n"+strings[4]+"</mass>\n")
    datafile.write("</configuration>\n</hoomd_xml>\n")
    datafile.close()
    box_dim = [[-lx/2,lx/2],[-ly/2,ly/2]]
    return box_dim

def hoomdIN():
	sig = settings.sig #sigma values
        eps = settings.eps #epsilon values
        for i in xrange(len(eps)):
                eps[i] = eps[i]*4.184
        rc = max(settings.sig)*2.5
        kbol = 0.00831445986
        tempK = settings.temp
        rS = settings.rS
        tempi = kbol*tempK
        rSname = settings.rs_d_file
        thermo = settings.thermo
        movie = settings.dump
        bias = settings.bias_eps
        steps = settings.steps
        runfile = open('run_hoomd.py','w')
        runfile.write('import settings\n')
        runfile.write('from hoomd_script import *\n')
        runfile.write('system = init.read_xml(filename=\'init.xml\')\n')
        runfile.write('lj = pair.lj(r_cut={0})\n'.format(rc))
        count = 0
	for i in range(0,len(sig)):
                for j in range(i,len(sig)):
                        Rcut = (0.5*(sig[i]+sig[j]))*2.5
			lSIG = 0.5*(sig[i]+sig[j])
			lEPS = eps[count]
                        if i == 3 or i == 3 or j == 3 or j == 4:
				runfile.write('lj.pair_coeff.set(\'{0}\',\'{1}\',epsilon={2},sigma={3},r_cut={4})\n'.format(i+1,j+1,0,lSIG,Rcut))
        		else:
				runfile.write('lj.pair_coeff.set(\'{0}\',\'{1}\',epsilon={2},sigma={3},r_cut={4})\n'.format(i+1,j+1,lEPS,lSIG,Rcut))
				count += 1
	runfile.write('lj.set_params(mode="shift")\n')
        charge_const = 1389.35458*bias*0.5*0.5
        runfile.write('yuk = pair.yukawa(r_cut=10)\n')
        for i in range(0,len(sig)):
                for j in range(i,len(sig)):
                        if i == 3 and j == 4:
                                runfile.write('yuk.pair_coeff.set(\'{0}\',\'{1}\',epsilon={2},kappa=0.4)\n'.format(i+1,j+1,charge_const))
                        else:
        			runfile.write('yuk.pair_coeff.set(\'{0}\',\'{1}\',epsilon=0,kappa=0.4)\n'.format(i+1,j+1))
	runfile.write('yuk.set_params(mode="shift")\n')
        runfile.write('dump.xml(filename=\'random.xml\',vis=True,image=True)\n')
        runfile.write('dump.dcd(filename=\'random.dcd\', period={0},unwrap_rigid=True,overwrite=True)\n'.format(movie))
        runfile.write('logger = analyze.log(filename=\'random.log\', period={0},quantities=[\'temperature\',\'kinetic_energy\',\'pressure\',\'volume\'], header_prefix=\'#\', overwrite=True)\n'.format(thermo))
        runfile.write('xml = dump.xml(filename=\'{0}\', all=True, restart=True, period={1}, phase=0)\n'.format(rSname,rS))
        runfile.write('integrate.mode_standard(dt=0.05)\n')
        runfile.write('rigid = group.rigid()\n')
        runfile.write('bdr = integrate.bdnvt_rigid(group=rigid,T={0})\n'.format(tempi))
        runfile.write('run({0})\n'.format(steps))
	runfile.close()
	for i in xrange(len(eps)):
                eps[i] = eps[i]/4.184
	return

 
