from grasp import *
#This file implements the GRASP calculation documented here:

dir_6s = '/home/calvin/graspy/calc-outputs/safronova/est_6s2'
dir_6p = '/home/calvin/graspy/calc-outputs/safronova/est_6p'
dir_5d = '/home/calvin/graspy/calc-outputs/safronova/est_5d'
dir_ci = '/home/calvin/graspy/calc-outputs/safronova/ci'

clistordering = ['1s','2s','2p','3s','3p','3d','4s','4p','4d','5s','5p','4f','5d','6s','6p','5f','6d','7p','8s']
initialize(workdir=dir_6s,clist=clistordering)
mr_6s2 = Rcsfgenerate('Xe',
            ['4f(14,*)6s(2,*)'],
            activeset=[6,5,4,4],
            jlower=0,jhigher=0,exc=0,write_csf='rcsfmr.inp')

indices_6s2 = [[1]]

est6s2 =[
        Rnucleus(Z=70,A=172,neutralMass=171.936378,I=0,NDM=0,NQM=0),
        Rangular(),
        Rwfnestimate(orbdict=
            {'*':'../../../calc-scripts/cores/yb_6s2master.w'},
                     fallback='Thomas-Fermi'),
        Rmcdhf(indices_6s2,orbs=['6s'],specorbs=['*'],weightingmethod='Standard',runs=1000),
        Rwfnestimate(orbdict=
            {'*':os.path.join(dir_6s,'rwfn.out')},
                     fallback='Thomas-Fermi'),
        Rmcdhf(indices_6s2,orbs=['4f*'],specorbs=['*'],weightingmethod='Standard',runs=1000),
        Rwfnestimate(orbdict=
            {'*':os.path.join(dir_6s,'rwfn.out')},
                     fallback='Thomas-Fermi'),
        Rmcdhf(indices_6s2,orbs=['*'],specorbs=['*'],weightingmethod='Standard',runs=1000),
        ]

#
# Estimate 6p orbitals using 4f13 6s2 6p configurations
#
initialize(workdir=dir_6p,clist=clistordering)
mr_6p = Rcsfgenerate('Xe',
            ['4f(13,*)6s(2,*)6p(1,*)'],
            activeset=[6,6,4,4],
            jlower=0,jhigher=10,exc=0,write_csf = 'rcsfmr.inp')
indices_6p = [[1],[1,2,3],[1,2,3,4],[1,2,3],[1]]
est6p =[
        Rnucleus(Z=70,A=172,neutralMass=171.936378,I=0,NDM=0,NQM=0),
        Rangular(),
        Rwfnestimate(orbdict=
            {'*':os.path.join(dir_6s,'rwfn.out')},
                     fallback='Thomas-Fermi'),
        Rmcdhf(indices_6p,orbs=['6p*'],specorbs=['*'],weightingmethod='Standard',runs=1000)
        ]


#
# Estimate 5d orbitals using 4f13 6s2 5d configurations
#
initialize(workdir=dir_5d,clist=clistordering)
mr_5d = Rcsfgenerate('Xe',
            ['4f(13,*)5d(1,*)6s(2,*)'],
            activeset=[6,5,5,4],
            jlower=0,jhigher=14,exc=0,write_csf = 'rcsfmr.inp')
indices_5d = [[1],[1,2,3],[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3],[1]]
est5d =[
        Rnucleus(Z=70,A=172,neutralMass=171.936378,I=0,NDM=0,NQM=0),
        Rangular(),
        Rwfnestimate(orbdict=
            {'*':os.path.join(dir_6s,'rwfn.out')},
                     fallback='Thomas-Fermi'),
        Rmcdhf(indices_5d,orbs=['5d*'],specorbs=['*'],weightingmethod='Standard',runs=1000)
        ]



initialize(workdir=dir_ci,clist=clistordering)
zeros_6s2 = Rcsfgenerate('Xe',['4f(14,*)6s(2,*)'],activeset=[6,6,6,5],jlower=0,jhigher=2,exc=0,write_csf='rcsfmr.inp')
zeros_6s5d= Rcsfgenerate('Xe',['4f(14,*)5d(1,*)6s(1,*)'],activeset=[6,5,5,4],jlower=0,jhigher=8,exc=0,write_csf='rcsfmr.inp')
zeros_even = zeros_6s2 + zeros_6s5d

zeros_6s6p= Rcsfgenerate('Xe',['4f(14,*)6s(1,*)6p(1,*)',],activeset=[6,6,4,4],jlower=0,jhigher=4,exc=0,write_csf='rcsfmr.inp')
zeros_4f5d= Rcsfgenerate('Xe',['4f(13,*)5d(1,*)6s(2,*)',],activeset=[6,5,5,4],jlower=0,jhigher=14,exc=0,write_csf='rcsfmr.inp')
zeros_odd = zeros_6s6p + zeros_4f5d

multireference = zeros_odd + zeros_even

singles_6s2 = Rcsfgenerate('Xe',['4f(14,*)6s(2,*)'],activeset=[7,7,6,5],jlower=0,jhigher=2,exc=2,write_csf='rcsfmr.inp')
singles_4f5d = Rcsfgenerate('Xe',['4f(14,*)5d(1,*)6s(1,*)'],activeset=[7,7,6,5],jlower=0,jhigher=10,exc=2,write_csf='rcsfmr.inp')
singles_even = singles_6s2 + singles_4f5d

singles_6s6p= Rcsfgenerate('Xe',['4f(14,*)6s(1,*)6p(1,*)',],activeset=[7,7,6,5],jlower=0,jhigher=6 ,exc=2,write_csf='rcsfmr.inp')
singles_4f5d= Rcsfgenerate('Xe',['4f(13,*)5d(1,*)6s(2,*)',],activeset=[7,7,6,5],jlower=0,jhigher=16,exc=2,write_csf='rcsfmr.inp')
singles_odd = singles_6s6p + singles_4f5d
singles_exp = singles_even + singles_odd

# run
# python indexer.py rcsfmr.inp rcsf.inp
# in order to get these indices automatically
# note that one of the 1- levels is missing....

indices_mr = [[1],[1],[1],[1,2],[1],[1,2],[1],[1,2],[1],[1],[1],[1],[1],[1],[1]]
ci_run = [
         Rnucleus(Z=70,A=172,neutralMass=171.936378,I=0,NDM=0,NQM=0),
         singles_exp,
         Rcsfinteract('Dirac-Coulomb'),
         Rangular(),
         Rwfnestimate(orbdict={'6p*':os.path.join(dir_6p, 'rwfn.out'),
                               '5d*':os.path.join(dir_5d, 'rwfn.out'),
                               '*' :os.path.join(dir_6s,'rwfn.out')},
                               fallback='Thomas-Fermi'),
         Rmcdhf(indices_mr,orbs=['5f*,6d*,7s,7p*'],specorbs=[''],weightingmethod='Standard',runs=1000),
         Rsave('safronova'),
         Rci(files='safronova',
                 includetransverse=True,
                 modifyfreq=True,
                 scalefactor='1.d-6',
                 includevacpol = True,
                 includenms= False,
                 includesms = False,
                 estselfenergy= True,
                 largestn = 8,
                 asfidx = indices_mr),

         ]

readout = [
        Rmixextract('safronova',useCI=True,tolerance = 0.001,sort=True),
        JJtoLSJ('safronova',useCI=True,unique=True),
        Rlevels(files='safronova')
        ]

mr_6s2.execute(workdir = dir_6s) # define the multireference
[cmd.execute(workdir = dir_6s) for cmd in est6s2]
mr_5d.execute(workdir = dir_5d) # define the multireference
[cmd.execute(workdir = dir_5d) for cmd in est5d]
mr_6p.execute(workdir = dir_6p) # define the multireference
[cmd.execute(workdir = dir_6p) for cmd in est6p]

multireference.execute(workdir=dir_ci)
[cmd.execute(workdir=dir_ci) for cmd in ci_run]
[cmd.execute(workdir=dir_ci) for cmd in readout]
#        Rcsfinteract('Dirac-Coulomb'),
#        Rangular(),
#        Rwfnestimate(orbdict={'*':os.path.join(testdir,'rwfn.out')},
#            fallback='Thomas-Fermi'),
#        Rmcdhf(indices_6s6p,orbs=['5d'],specorbs=['*'],weightingmethod='Standard',runs=1000),
#        Rwfnestimate(orbdict={'*':os.path.join(testdir,'rwfn.out')},
#            fallback='Thomas-Fermi'),
#        Rmcdhf(indices_6s6p,orbs=['*'],specorbs=['*'],weightingmethod='Standard',runs=1000),
#        Rwfnestimate(orbdict={'*':os.path.join(testdir,'rwfn.out')},
#            fallback='Thomas-Fermi'),
#        Rmcdhf(indices_6s6p,orbs=['7s'],specorbs=['*'],weightingmethod='Standard',runs=1000),
#        ]

