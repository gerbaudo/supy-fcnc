from supy import wrappedChain,utils,calculables
import ROOT as r
#_____________________________
class P4(wrappedChain.calculable) :
    def __init__(self, collection = None) :
        self.fixes = collection
        self.stash(['pt','eta','phi','m',])
    @property
    def name(self) : return "P4".join(self.fixes)
    def update(self,ignored) :
        pts = self.source[self.pt]
        etas = self.source[self.eta]
        phis = self.source[self.phi]
        ms = self.source[self.m]
        self.value = [utils.LorentzV(P,e,p,m) for P,e,p,m in zip(pts, etas, phis, ms)]
#_____________________________
class Indices(wrappedChain.calculable) :
    def __init__(self, collection = None, ptMin = None, absEtaMax = 1000) :
        self.fixes = collection
        self.stash(["charge","author", "loose","P4","cb_d0_exPV","cb_z0_exPV"])
        self.ptMin = ptMin
        self.absEtaMax = absEtaMax
        self.moreName = "muon "\
            +("pt>%.1fGeV;"%ptMin if ptMin else "")\
            +(";|eta|<%.1f"%absEtaMax if absEtaMax<1000 else "")
    @property
    def name(self) : return 'Indices'.join(self.fixes)
    def update(self,ignored) :
        self.value = []        
        p4s    = self.source[self.P4]
        for i, p4 in enumerate(p4s) :
            if self.ptMin and p4.pt() < self.ptMin : continue
            if self.absEtaMax and self.absEtaMax < abs(p4.eta()) : continue
            self.value.append(i)
#_____________________________
class RelativeIso(wrappedChain.calculable) :
    def __init__(self, collection = None, isoMax = None, isoVar = None) :
        self.isoVar = isoVar
        self.isoMax = isoMax
        self.fixes = collection
        self.stash(['pt', 'ptcone20', 'ptcone30', 'ptcone40'])
    @property
    def name(self) : return "RelativeIso".join(self.fixes)
    def update(self,ignored) :
        pts = self.source[self.pt]
        isoMax = self.isoMax
        isoVals = self.source[eval('self.'+self.isoVar)]
        self.value = [v/p < isoMax if p else None for v,p in zip(isoVals,pts)]

class RelativeIso02PtCone30(RelativeIso) :
    def __init__(self,collection) :
        super(RelativeIso02PtCone30,self).__init__(collection,0.2,'ptcone30')
        
