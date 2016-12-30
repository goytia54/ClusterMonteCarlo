import settings
import math as m
import random


'''####################################################################################
 rand_angle() returns the angle between  A,B,C of molecule. If sigmas are equal 
 then the angle would be 60 degrees, isolateral triangle. 
####################################################################################'''
def rand_angle():
    # determine angle from cosine rule
    sig = settings.sig
    settings.rc = sig[4]*1.5
    siga = sig[0]/2
    sigb = sig[1]/2
    sigc = sig[2]/2
    
    sigAsigB = siga*sigb
    sigAsigC = siga*sigc
    sigBsigC = sigb*sigc
    sigBsigB = sigb*sigb
    
    top = sigAsigC-sigBsigB-sigAsigB-sigBsigC
    bot = -sigAsigC-sigBsigB-sigAsigB-sigBsigC
    
    a_mol = m.acos(top/bot)*57.2958 #converted from radians
    random_angle = a_mol
    #random_angle = random.randrange(int(a_mol),180,1) #bring this back for random angle
    return random_angle

'''######################################################################################
mol_xyz() takes the angle from rand_angle and computes the coordinates for all the 
atoms in the trimer, A,B,C and determines a centroid particle(D) which will serve
as indicator if it is left or right handed
######################################################################################'''
def mol_xyz(random_angle):
    sig = settings.sig
    siga = sig[0]/2
    sigb = sig[1]/2
    sigc = sig[2]/2
    
    rand_rad = random_angle/57.2958 # random angle in randians     
    r_angle = abs(random_angle)
    #using cosine rule again
    a = sigb + sigc
    c = siga + sigb
    b = (a**2)+(c**2)-2*a*c*m.cos(rand_rad)    
    if r_angle <= 90:
        rand_rad = r_angle/57.2958
    else:
        rand_rad = (180-r_angle)/57.2958
    Cy = a*m.sin(rand_rad)
    Dy = Cy**2
    first = b-Dy
    
    Cx = m.sqrt(first) - (sigb+siga)
    sign = random.randint(0,1)
    if sign == 0:
        Cy = -Cy
    #determining the cooridates of the centroid particle
    A = [-(sigb+siga),0,0]
    B = [0,0,0]
    C = [Cx,Cy,0]
    Dx = 0-(A[0]+B[0]+C[0])/3
    Dy=  0-(A[1]+B[1]+C[1])/3
    #recenter everything
    D = [0,0,0]
    A = [Dx+A[0],Dy+A[1],0]
    B = [Dx+B[0],Dy+B[1],0]
    C = [Dx+C[0],Dy+C[1],0]
    return A, B, C, D

'''##############################################################################################
cell_coords determines uses the cooridantes of the molecule to then make string coordinates
for a^2 (a is number of molcules in 1D) molecules in the box with equal amounts of each handedness
################################################################################################'''

def cell_coords(A,B,C,D):
    sig = settings.sig
    den = 1.40256 #amu/Angstrom^3 of silicon
    a = 14.0 # amount of unit cells
    m = 7.0 # distanc between m.lecules
    deltay = -float((m*a/2)-m/2)                    
    posstr,bodystr,diamstr,masstr,typestr = "","","","",""
    n_ID = 1
    m_ID = 1
    flip = 1
    masses = []
    for i in range(0,3):
        mass = den*(4/3)*(sig[i]**3)*3.141592653589793
        masses.append(mass)
    for i in xrange(int(a)):
        deltax = -float((m*a/2)-m/2)
        for j in xrange(int(a)):
           posstr += str(A[0]+deltax) + ' ' +  str(flip*A[1]+deltay) + ' ' + str(A[2]) +'\n'
           posstr += str(B[0]+deltax) + ' ' +  str(flip*B[1]+deltay) + ' ' + str(B[2]) +'\n'
           posstr += str(C[0]+deltax) + ' ' +  str(flip*C[1]+deltay) + ' ' + str(C[2]) +'\n'
           if flip == 1:
               D_type = 4
               flip -= 2
           else: 
               D_type = 5
               flip += 2
           posstr += str(D[0] +deltax) + ' ' +  str(D[1]+deltay) + ' ' + str(D[2]) +'\n'
           bodystr += 4*(str(m_ID-1) + "\n")
           diamstr += str(sig[0]) + "\n" + str(sig[1])+ "\n" + str(sig[2]) +"\n" + "0.5\n"
           masstr += str(masses[0]) +'\n' + str(masses[1]) + '\n' + str(masses[2]) +'\n 0.000001\n'
           typestr += "1\n" + "2\n" + "3\n" + str(D_type) + "\n"
           deltax += m
           m_ID += 1          
        deltay = deltay + m           
    n_ID -= 1
    m_ID -= 1
    masses = [] 
    xlo = -(m*a)/2
    xhi = (m*a/2) 
    ylo = -(m*a)/2
    yhi = (m*a)/2
    lx = abs(xlo-xhi)
    ly = abs(ylo-yhi)
    
    strings = [posstr,typestr,bodystr,diamstr,masstr]
    return m_ID,strings,lx,ly 
