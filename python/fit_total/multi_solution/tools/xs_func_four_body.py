#/usr/bin/env python
#-*- Coding: UTF-8 -*-

__author__ = "Lianjin WU <wulj@ihep.ac.cn>"
__copyright__ = "Copyright (c) Lianjin WU"
__created__ = "[2020-11-06 Fri 23:18]"

import ROOT as root
import math
import os.path, sys
# from phi_n import PhiN

class xs_func():
    # def __init__(self, nbin, lower, upper, mass1 = 0.13957, mass2 = 0.13957, mass3 = 1.86965, mass4 = 1.86965):
    def __init__(self):
        """ bin, lower, upper limits for PHSP factor, three particle masses  """
        self._gr = root.TGraph()
        # m = [mass1, mass2, mass3, mass4]
        # for ibin in range(nbin):
        #     m0 = lower + ibin*(upper - lower)/float(nbin)
        #     ps = PhiN(m0*m0, 4, m)
        #     self._gr.SetPoint(ibin, lower + ibin*(upper - lower)/float(nbin), ps)
        if not os.path.isfile('/scratchfs/bes/jingmq/bes/DDPIPI/v0.2/run/ana/fit/four_body_phase_space_test.txt'):
            print('Four body decay phase space factor must be sampled, run ./sub/sub_four_body.sh first!')
            sys.exit()
        with open('/scratchfs/bes/jingmq/bes/DDPIPI/v0.2/run/ana/fit/four_body_phase_space_test.txt', 'r') as f:
            lines = f.readlines()
            ibin = 0
            for line in lines:
                try:
                    fargs = map(float, line.strip().split())
                except:
                    fargs = list(map(float, line.strip().split()))
                self._gr.SetPoint(ibin, fargs[0], fargs[1])
                ibin += 1

    ### defined BW (PHSP factors are considered) 
    def getOneBreitWigner(self, xx, mass, width, eewidth, minMotherEnergy):
        """ minMotherEnergy = m1 + m2 + m3 + m4"""
        if mass < minMotherEnergy or xx < minMotherEnergy or width < 0.0 or eewidth < 0.0: 
            return complex(0.0, 0.0)

        right = math.sqrt(self._gr.Eval(xx) / self._gr.Eval(mass))
        numerator = math.sqrt(12.0*math.pi*width*eewidth)
        denominator = complex(xx*xx-mass*mass, mass*width)
        left = numerator/denominator
        
        return left*right

    def getPHSP(self, xx):
        return self._gr.Eval(xx)

    ### defined correlated N BW (PHSP factors are included)
    def getCorrelatedBreitWigners(self, xx, resonances, minMotherEnergy):
        """ minMotherEnergy = m1 + m2 + m3 + m4
                resonance: [mass, width, eewidth, phi] """
        bw = complex(0.0, 0.0)
        for i, resonance in enumerate(resonances):
            mass, width, eewidth, phi = resonance
            bw = bw + self.getOneBreitWigner(xx, mass, width, eewidth, minMotherEnergy)*(self.getExpIPhi(phi))
        return bw
    
    ### defined exp(i*phi) = cos(phi) + i*sin(phi)
    def getExpIPhi(self, phi):
        """ exp(i*phi) = cos(phi) + i*sin(phi) """
        return complex(math.cos(phi), math.sin(phi))
