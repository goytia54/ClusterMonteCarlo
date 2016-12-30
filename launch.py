import settings
import random

'''#####################################################################
EorS() changes one parameter of the epsilons at random 
####################################################################'''

def EorS(): # returns sigmas
    eps = settings.eps
    sig = settings.sig
    dSig = settings.dSig
    dEps = settings.dEps
    rand_parm = random.randint(0,5)
    x = 1
    x = 1
    while x > 0:
        delt_eps = dEps*(2*random.random()-1)
        mol_eps = delt_eps + eps[rand_parm]
        if mol_eps >= 0.1 or mol_eps <= 3.0:
           settings.eps[rand_parm] = mol_eps
           x -= 1
    return

