##########GLOBAL VARIABLES################
d_file = 'init.xml' #data file name 
steps = 700000 # number of steps for MD run
rs_d_file = 'random.rS'
dim = '2' #dimension
thermo = 1000 # how often to output thermo variable (LAMMPS)
dump = 1000 # how often to dump to lammps trajectory (LAMMPS)
temp = 300 #temperature in kelvin
tstep = 5.0 # timestep in units picked (default: fs)
rS = 10000  # how often to write restart
g_sig = 2 #sigma of ghost particle
rounds = 0 #round number of simulations 
max_inter = 10000 # number of rounds to be run total
append_count = 0 #whether to append or then write, switch 
dSig = 0.1
dEps = 0.2
sig = [2.0,2.0,2.0,0.5, 0.5] #sigma values!!!!!!!!!!one space between values and double or float
eps = [1.5,1.5,1.5,1.5,1.5,1,5,0.0,0.0] #epsilon values !!!!!!!!!!!!!!!!one space between values and double or float values
old_sig=[2.0,2.0,2.0,0.5,0.5]     
old_eps=[1.5,1.5,1.5,1.5,1.5,1.5,0.0, 0.0] 
p_sig=[2.25,2.25,2.25,0.5,0.5]
bias_eps = 0.16  #added factor to bias of yukawa
qghost = 0.5 #charge of ghost 
##########################################
