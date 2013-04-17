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
        self.stash(["charge","author", "loose","P4",'Etcone20','Etcone20_pt_corrected'])
        self.ptMin = ptMin
        self.absEtaMax = absEtaMax
        self.moreName = "ele "\
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
