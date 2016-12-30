import os
from settings import *

def fit_param(fitness):
    currentRound = settings.rounds
    if not os.path.exists("good_traj/"):
        os.system('mkdir good_traj')
    os.chdir('good_traj')
    accept = 0
    if fitness.cloc < 0.85 or fitness.clust < 0.30 :
        settings.sig = [i for i in settings.old_sig]
        settings.eps = [i for i in settings.old_eps]
    else:
        settings.old_sig = [i for i in settings.sig]
        settings.old_eps = [i for i in settings.eps]
        accept += 1
        if currentRound % 100 == 0:
                os.system('cp ../random.xml random_{0}.xml'.format(currentRound))
                os.system('cp ../random.dcd random_{0}.dcd'.format(currentRound))
    os.chdir('..')
    if settings.rounds == 0:
        fit_file = open('fit.txt','w')
        fit_file.write('# rounds cloc clust bias sig1 sig2 sig3 eps11 eps12 eps13 eps22 eps23 eps33 accpet\n')
    else:
        fit_file = open('fit.txt','a')
    sig = settings.sig
    eps = settings.eps
    bias = settings.bias_eps
    fit_file.write('{0} {1} {2} {3} '.format(settings.rounds,fitness.cloc,fitness.clust,bias))
    fit_file.write('{0} {1} {2} '.format(sig[0],sig[1],sig[2]))
    fit_file.write('{0} {1} {2} '.format(eps[0],eps[1],eps[2]))
    fit_file.write('{0} {1} {2} '.format(eps[3],eps[4],eps[5]))
    fit_file.write('{0}\n'.format(accept))
    fit_file.close()


