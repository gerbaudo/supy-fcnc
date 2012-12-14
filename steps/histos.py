import ROOT as r
from supy import analysisStep
import supy
from math import fabs, pi

# for all the deltas, the first value is the reference one, so
# delta = val_i+1 - val_1
# deltaFrac = (val_i+1 - val_1)/val_1

MeV2GeV = 1.0e-3
def phi_mpi_pi(value) :
    "same as r.Math.GenVector.VectorUtil.Phi_mpi_pi (for some reason cannot import it...)"
    pi = r.TMath.Pi()
    if value > pi and value <= pi:
        return value
    while value <= -pi: value = value+2.*pi
    while value >  +pi: value = value-2.*pi
    return value

class deltaEta(analysisStep) :
    def __init__(self, indexLabel1='', indexLabel2='',title="#Delta #eta",
                 N=20,low=-4.,up=+4.,
                 collP4='genP4') :
        for item in ['indexLabel1','indexLabel2','title','N','low','up','collP4'] : setattr(self,item,eval(item))
        self.hName = 'deltaEta%s%s'%(indexLabel1,indexLabel2)
    def uponAcceptance(self, eventVars) :
        p4s = eventVars[self.collP4]
        p1,p2 = p4s[eventVars[self.indexLabel1][0]], p4s[eventVars[self.indexLabel2][0]]
        self.book.fill(p2.eta - p1.eta, self.hName, self.N, self.low, self.up, title=self.title)

class deltaPhi(analysisStep) :
    def __init__(self, indexLabel1='', indexLabel2='',title="#Delta #phi",
                 N=20,low=-pi,up=+pi,
                 collP4='genP4') :
        for item in ['indexLabel1','indexLabel2','title','N','low','up','collP4'] : setattr(self,item,eval(item))
        self.hName = 'deltaPhi%s%s'%(indexLabel1,indexLabel2)
    def uponAcceptance(self, eventVars) :
        p4s = eventVars[self.collP4]
        p1,p2 = p4s[eventVars[self.indexLabel1][0]], p4s[eventVars[self.indexLabel2][0]]
        self.book.fill(abs(phi_mpi_pi(r.Math.VectorUtil.DeltaPhi(p1,p2))), self.hName, self.N, self.low, self.up, title=self.title)

class deltaR(analysisStep) :
    def __init__(self, indexLabel1='', indexLabel2='',title="#Delta R",
                 N=20,low=-pi,up=+pi,
                 collP4='genP4') :
        for item in ['indexLabel1','indexLabel2','title','N','low','up','collP4'] : setattr(self,item,eval(item))
        self.hName = 'deltaR%s%s'%(indexLabel1,indexLabel2)
    def uponAcceptance(self, eventVars) :
        p4s = eventVars[self.collP4]
        p1,p2 = p4s[eventVars[self.indexLabel1][0]], p4s[eventVars[self.indexLabel2][0]]
        self.book.fill(r.Math.VectorUtil.DeltaR(p1, p2), self.hName, self.N, self.low, self.up, title=self.title)
