from supy import wrappedChain,utils,calculables
import ROOT as r
###############################
#class genSumP4(wrappedChain.calculable) :
#    def update(self,_) :
#        genP4 = self.source['genP4']
#        self.value = genP4.at(4) + genP4.at(5)
###############################
#class wNonQQbar(wrappedChain.calculable) :
#    def update(self,_) :
#        self.value = None if self.source['genQQbar'] else 1
###############################
#class wQQbar(wrappedChain.calculable) :
#    def update(self,_) :
#        self.value = 1 if self.source['genQQbar'] else None
###############################
#class genQQbar(wrappedChain.calculable) :
#    def update(self,_) :
#        if self.source['isRealData'] :
#            self.value = ()
#            return
#        ids = list(self.source['genPdgId'])
#        iHard = self.source['genIndicesHardPartons']
#        self.value = tuple(sorted(iHard,key = ids.__getitem__,reverse = True)) \
#                     if not sum([ids[i] for i in iHard]) else tuple()
###############################
#class genIndicesHardPartons(wrappedChain.calculable) :
#    def __init__(self,indices = (4,5)) : self.value = indices
#    def update(self,_) : pass
###############################
#class genStatus1P4(wrappedChain.calculable) :
#    def update(self,_) :
#        self.value = []
#        for i in range(self.source["genP4"].size()) :
#            if self.source["genStatus"].at(i)!=1 : continue
#            self.value.append(self.source["genP4"][i])
##############################
class genIndices(wrappedChain.calculable) :
    @property
    def name(self) : return "genIndices" + self.label

    def __init__(self, pdgs = [], label = None, status = [], motherPdgs = []) :
        self.label = label
        self.PDGs = frozenset(pdgs)
        self.status = frozenset(status)
        self.motherPdgs = frozenset(motherPdgs)
        self.moreName = "; ".join(["pdgId in %s" %str(list(self.PDGs)),
                                   "status in %s"%str(list(self.status)),
                                   "motherPdg in %s"%str(list(self.motherPdgs))
                                   ])

    def update(self,_) :
        pdg = self.source["genPdgId"]
        status = self.source["genStatus"]
        motherPdg = self.source["genMotherPdgId"]
        self.value = filter( lambda i: ( (not self.PDGs) or (pdg.at(i) in self.PDGs) ) and \
                                 ( (not self.status) or (status.at(i) in self.status) ) and \
                                 ( (not self.motherPdgs) or (motherPdg.at(i) in self.motherPdgs) ),
                             range(pdg.size()) )

#class genIndicesPtSorted(wrappedChain.calculable) :
#    @property
#    def name(self) :
#        return "%sPtSorted"%self.label
#
#    def __init__(self, label = "") :
#        self.label = "genIndices"+label
#
#    def update(self,_) :
#        p4 = self.source["genP4"]
#        self.value = sorted(self.source[self.label], key = lambda i:p4.at(i).pt(), reverse = True)
#
#class genRootSHat(wrappedChain.calculable) :
#    def update(self,_) :
#        iHard = self.source["genIndicesHardPartons"]
#        p4s = self.source["genP4"]
#        self.value = None if not iHard else (p4s.at(iHard[0])+p4s.at(iHard[1])).mass()
#
#class genSumPt(wrappedChain.calculable) :
#    @property
#    def name(self) :
#        return "_".join(["genSumPt"]+self.indexLabels)
#
#    def __init__(self, indexLabels = []) :
#        self.indexLabels = map(lambda s:s.replace("genIndices",""), indexLabels)
#
#    def update(self,_) :
#        indices = []
#        for label in self.indexLabels :
#            indices += self.source["genIndices"+label]
#        indices = set(indices)
#
#        self.value = 0.0
#        p4 = self.source["genP4"]
#        for i in indices :
#            self.value += p4.at(i).pt()
#
##############################
class genIndicesWqq(wrappedChain.calculable) :
    def update(self,_) :
        ids = self.source['genPdgId']
        mom = self.source['genMotherPdgId']
        self.value = filter(lambda i: abs(mom[i]) is 24 and abs(ids[i]) < 5, range(len(ids)))
##############################
class genParticleCounter(wrappedChain.calculable) :
    @property
    def name(self) : return "GenParticleCategoryCounts"

    def __init__(self) :
        self.value = {}
        self.pdgToCategory = {}

        #copied from PDG
        self.initPdgToCategory( 1, 6,"quark")
        self.initPdgToCategory(21,21,"gluon")

        self.initPdgToCategory(1000001,1000004,"squarkL")#left-handed
        self.initPdgToCategory(1000005,1000006,"squarkA")#ambiguous
        self.initPdgToCategory(1000011,1000016,"slepton")
        self.initPdgToCategory(2000001,2000004,"squarkR")#right-handed
        self.initPdgToCategory(2000005,2000006,"squarkA")#ambiguous
        self.initPdgToCategory(2000011,2000011,"slepton")
        self.initPdgToCategory(2000013,2000013,"slepton")
        self.initPdgToCategory(2000015,2000015,"slepton")
        self.initPdgToCategory(1000021,1000021,"gluino")
        self.initPdgToCategory(1000022,1000023,"chi0")
        self.initPdgToCategory(1000024,1000024,"chi+")
        self.initPdgToCategory(1000025,1000025,"chi0")
        self.initPdgToCategory(1000035,1000035,"chi0")
        self.initPdgToCategory(1000037,1000037,"chi+")
        self.initPdgToCategory(1000039,1000039,"gravitino")

        self.combineCategories(["squarkL","squarkR","squarkA"], "squark")
        self.combineCategories(["slepton","chi0","chi+","gravitino"], "otherSusy")

        self.badCategoryName = "noName"
        self.categories = list(set(self.pdgToCategory.values()))
        self.categories.append(self.badCategoryName)
        self.categories.sort()
        #self.printDict(self.pdgToCategory)

    def initPdgToCategory(self,lower,upper,label) :
        for i in range(lower,upper+1) :
            self.pdgToCategory[i]=label
        for i in range(-upper,-lower+1) :
            self.pdgToCategory[i]=label

    def combineCategories(self,someList,someLabel) :
        for key in self.pdgToCategory :
            if self.pdgToCategory[key] in someList :
                self.pdgToCategory[key]=someLabel
        
    def printDict(self,someDict) :
        for key in someDict :
            print key,someDict[key]

    def zeroCategoryCounts(self) :
        for key in self.categories :
            self.value[key]=0

    def incrementCategory(self,pdgId) :
        if pdgId in self.pdgToCategory:
            category=self.pdgToCategory[pdgId]
        else :
            category=self.badCategoryName
        self.value[category]+=1
        #print "found one:",iParticle,pdgId

    def update(self,_) :
        self.zeroCategoryCounts()
        if not self.source["genHandleValid"] : return
        nParticles = len(self.source["genPdgId"])

        #Susy counts
        for iParticle in self.source["susyIniIndices"] :
            self.incrementCategory(self.source["genPdgId"].at(iParticle))

        #initial state counts
        for iParticle in range(nParticles) :
            #consider only status 3 particles
            if self.source["genStatus"].at(iParticle)!=3 : continue
            #whose mothers are protons
            if self.source["genMotherPdgId"].at(iParticle)!=2212 : continue
            #whose mothers have index 0 or 1
            if self.source["genMotherIndex"].at(iParticle) not in [0,1] : continue
            self.incrementCategory(self.source["genPdgId"].at(iParticle))
