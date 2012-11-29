# largely based on
# https://github.com/betchart/susycaf/blob/master/calculables/gen.py
import collections, ROOT as r
from supy import utils,analysisStep
#####################################
try:
    import pdgLookup
    pdgLookupExists = True
except ImportError:
    pdgLookupExists = False
#####################################


class PdgLookup:
    def __init__(self) :
        self.names = {
            -1:'/d', 1:'d',
             -2:'/u', 2:'u',
             -3:'/s', 3:'s',
             -4:'/c', 4:'c',
             -5:'/b', 5:'b',
             -6:'/t', 6:'t',
             -11:'e+', 11:'e-',
             -12:'ve', 12:'ve',
             -13:'mu+', 13:'mu-',
             -14:'vmu', 14:'vmu',
             -15:'tau+', 15:'tau-',
             -16:'vtau', 16:'vtau',
             21:'g',
             -22:'gamma', 22:'gamma',
             -23:'Z', 23:'Z',
             -24:'W-', 24:'W+',
             -25:'h', 25:'h',
             -511:'/B0',511:'B0',
             -513:'/B*0',513:'B*0',
             -521:'B-',521:'B+',
             -523:'B*-',523:'B*+',
             -531:'/B0s',531:'B0s',
             -533:'/B*0s',533:'B*0s',
        }
    def pdgid_to_name(self,id) : return self.names[id] if id in self.names else 'unknown'

#####################################
class ParticleCountFilter(analysisStep) :
    def __init__(self, reqDict) :
        self.reqDict = reqDict
    def select (self,eventVars) :
        for key,value in self.reqDict.iteritems() :
            if eventVars["GenParticleCategoryCounts"][key]!=value : return False
        return True
#####################################
#####################################
class particlePrinter(analysisStep) :

    def __init__(self,minPt=-1.0,minStatus=-1):
        self.oneP4=utils.LorentzV()
        self.sumP4=utils.LorentzV()
        self.zeroP4=utils.LorentzV()
        self.minPt=minPt
        self.minStatus=minStatus
        
    def uponAcceptance (self,eventVars) :
        pdgLookupExists = True
        pdgLookup = PdgLookup()
        self.sumP4.SetCoordinates(0.0,0.0,0.0,0.0)

        parents=set([p for pp in eventVars['mc_parent_index'] for p in pp])
        #print "parents: ",parents
        print "-----------------------------------------------------------------------------------"
        print " i  st   par         id            name        E        pt       eta    phi    mass"
        print "-----------------------------------------------------------------------------------"

        size=len(eventVars["genP4"])
        maxPrintSize=50
        for iGen in range(min([maxPrintSize,size])) :

            p4=eventVars["genP4"][iGen]
            if p4.pt()<self.minPt : continue

            status=eventVars['mc_status'][iGen]
            if status<self.minStatus : continue

            pars = [i for i in eventVars['mc_parent_index'][iGen]]
            pdgId=eventVars['mc_pdgId'][iGen]
            outString=""
            outString+="%#2d"%iGen
            outString+=" %#3d"%status
            outString+= str(pars).rjust(6)
            outString+=" %#10d"%pdgId
            if pdgLookupExists : outString+=" "+pdgLookup.pdgid_to_name(pdgId).rjust(15)
            else :                 outString+="".rjust(16)
            outString+="  %#7.1f"%p4.E()
            outString+="  %#8.1f"%p4.pt()
            outString+="  %#8.1f"%p4.eta()
            outString+="  %#5.1f"%p4.phi()
            outString+="  %#6.1f"%p4.mass()        
            if not (iGen in parents) : outString+="   non-mo"
            print outString
        print
#####################################
class ttbarPrinter(analysisStep) :

    def uponAcceptance (self,ev) :
        ids = list(ev['mc_pdgId'])
        if not (6 in ids and -6 in ids) : return
        iTop = ids.index(6)
        iTbar= ids.index(-6)
        parents = ev['mc_parent_index'] #['mc_parents']
        parentIds = [[ids[p] for p in par] for par in parents]
        p4s = ev['genP4']
        status = ev['mc_status']
        pdg = PdgLookup()

        iGs = filter(lambda i: ids[i]==21, range(max(iTop,iTbar)+1,len(ids)))
        iTopChildren = [i for i,pars in enumerate(parentIds) if 6 in pars or -6 in pars]
        iWChildren = [i for i,pars in enumerate(parentIds) if 24 in pars or -24 in pars]
        iHChildren = [i for i,pars in enumerate(parentIds) if 25 in pars]
        width=15
        fieldNames = ['item','parents','parentIds','pt','eta','phi','status']
        print '-'*width*(len(fieldNames))
        print ''.join([("%s"%n).rjust(width) for n in fieldNames])
        print
        for i in [iTop,iTbar]+iTopChildren+iWChildren+iHChildren :
            print ''.join((("%s"%d).rjust(width) for d in ["%d (%s)"%(i,pdg.pdgid_to_name(ids[i])),
                                                           list(parents[i]),
                                                           list(parentIds[i])]\
                               +["%.3f"%v for v in [p4s[i].pt(),p4s[i].eta(), p4s[i].phi()]]\
                               +[status[i]]))
        print

#####################################
class genMotherHistogrammer(analysisStep) :

    def __init__(self, indexLabel, specialPtThreshold) :
        self.indexLabel = indexLabel
        self.specialPtThreshold = specialPtThreshold
        self.keyAll       = "motherIdVsPt%sAll"%self.indexLabel
        self.keyAllHighPt = "motherIdVsPt%sAllHighPt"%self.indexLabel        
        self.motherDict = collections.defaultdict(int)
        self.binLabels = []
        self.binLabels.append("other")

        self.addParticle( 1, "d"); self.addParticle(-1, "#bar{d}")
        self.addParticle( 2, "u"); self.addParticle(-2, "#bar{u}")
        self.addParticle( 3, "s"); self.addParticle(-3, "#bar{s}");
        self.addParticle( 4, "c"); self.addParticle(-4, "#bar{c}");
        self.addParticle(21, "gluon")
        self.addParticle(22, "photon")
        self.addParticle(111,"#pi^{0}")
        self.addParticle(221,"#eta")
        self.addParticle(223,"#omega")
        self.addParticle(331,"#eta^{/}")
        
    def addParticle(self, id, name) :
        self.binLabels.append(name)
        self.motherDict[id] = self.binLabels[-1]

    def fillSpecialHistos(self, eventVars, iParticle) :
        motherIndex = eventVars["genMother"].at(iParticle)
        #motherIndex = eventVars["genMotherIndex"].at(iParticle)
        p4 = eventVars["genP4"].at(iParticle)
        motherP4 = eventVars["genP4"].at(motherIndex)
        deltaRPhotonMother = r.Math.VectorUtil.DeltaR(p4,motherP4)
        deltaRPhotonOther  = r.Math.VectorUtil.DeltaR(p4,motherP4-p4)
        
        self.book.fill(motherP4.mass(), "mothersMass",
                                  20, -0.1, 0.4,
                                  title = ";mother's mass (GeV) [when GEN photon p_{T}> %.1f (GeV) and mother is u quark];photons / bin"%self.specialPtThreshold
                                  )
        self.book.fill(deltaRPhotonMother, "deltaRPhotonMother",
                                  20, 0.0, 1.5,
                                  title = ";#DeltaR(photon,mother) [when GEN photon p_{T}> %.1f (GeV) and mother is u quark];photons / bin"%self.specialPtThreshold
                                  )
        self.book.fill(deltaRPhotonOther, "deltaRPhotonOther",
                                  20, 0.0, 1.5,
                                  title = ";#DeltaR(photon,mother-photon) [when GEN photon p_{T}> %.1f (GeV) and mother is u quark];photons / bin"%self.specialPtThreshold
                                  )
        
    def uponAcceptance (self, eventVars) :
        indices = eventVars[self.indexLabel]
        if len(indices)==0 : return

        p4s = eventVars["genP4"]
        nBinsY = len(self.binLabels)
        for iParticle in indices :
            p4 = p4s.at(iParticle)
            pt = p4.pt()
            motherId = eventVars["genMotherPdgId"][iParticle]
            if not self.motherDict[motherId] :
                #print motherId,"not found"
                yValue = 0
            else :
                yValue = self.binLabels.index(self.motherDict[motherId])
            self.book.fill((pt,yValue), self.keyAll, (50,nBinsY), (0.0,-0.5), (500.0, nBinsY-0.5),
                                      title = ";GEN photon p_{T} (GeV);mother;photons / bin", yAxisLabels = self.binLabels)
            if pt>self.specialPtThreshold :
                self.book.fill(yValue, self.keyAllHighPt,
                                          nBinsY, -0.5, nBinsY-0.5,
                                          title = ";mother [when GEN photon p_{T}> %.1f (GeV)];photons / bin"%self.specialPtThreshold, xAxisLabels = self.binLabels)
                if motherId==2 : self.fillSpecialHistos(eventVars, iParticle)
#####################################
class zHistogrammer(analysisStep) :

    def __init__(self, jetCs) :
        self.jetCs = jetCs
        self.mhtName = "%sSumP4%s" % self.jetCs
        self.htName  = "%sSumEt%s"%self.jetCs
        
    def uponAcceptance (self,eventVars) :
        p4s = eventVars["genP4"]
        mht = eventVars[self.mhtName].pt()
        ht =  eventVars[self.htName]
        
        self.book.fill( len(cleanPhotonIndices), "photonMultiplicity", 10, -0.5, 9.5,
                        title=";number of %s%s passing ID#semicolon p_{T}#semicolon #eta cuts;events / bin"%self.cs)

        zIndices = eventVars["genIndicesZ"]
        if len(zS)>1 : return False
        for index in zIndices :
            Z = p4s.at(iPhoton)
            pt = photon.pt()


            self.book.fill(pt,           "%s%s%sPt" %(self.cs+(photonLabel,)), 50,  0.0, 500.0, title=";photon%s p_{T} (GeV);events / bin"%photonLabel)
            self.book.fill(photon.eta(), "%s%s%seta"%(self.cs+(photonLabel,)), 50, -5.0,   5.0, title=";photon%s #eta;events / bin"%photonLabel)

            self.book.fill((pt,mht), "%s%s%smhtVsPhotonPt"%(self.cs+(photonLabel,)),
                           (50, 50), (0.0, 0.0), (500.0, 500.0),
                           title=";photon%s p_{T} (GeV);MHT %s%s (GeV);events / bin"%(photonLabel,self.jetCs[0],self.jetCs[1])
                           )
            
            self.book.fill(mht/pt, "%s%s%smhtOverPhotonPt"%(self.cs+(photonLabel,)),
                           50, 0.0, 2.0, title=";MHT %s%s / photon%s p_{T};events / bin"%(self.jetCs[0],self.jetCs[1],photonLabel)
                           )

            #self.book.fill(pt-mht, "%s%s%sphotonPtMinusMht"%(self.cs+(photonLabel,)),
            #          100, -200.0, 200.0,
            #          title=";photon%s p_{T} - %s%sMHT (GeV);events / bin"%(photonLabel,self.jetCs[0],self.jetCs[1])
            #          )

            self.book.fill((pt-mht)/math.sqrt(ht+mht), "%s%s%sphotonPtMinusMhtOverMeff"%(self.cs+(photonLabel,)),
                           100, -20.0, 20.0,
                           title=";( photon%s p_{T} - MHT ) / sqrt( H_{T} + MHT )    [ %s%s ] ;events / bin"%(photonLabel,self.jetCs[0],self.jetCs[1])
                           )

class bqDotHistogrammer(analysisStep) :
    def f(self, x) :
        return x/5901.2 - 1.0

    def fill(self, x, y, sign = "") :
        self.book.fill((x, y), "bqDotHistogram%s"%sign, (100, 100), (-1.5, -1.5), (1.5, 1.5),
                       title = "W%s#rightarrowq#bar{q};(b.q)/5901.2 - 1.0;(b.#bar{q})/5901.2 - 1.0;events / bin"%sign)

    def uponAcceptance (self,eventVars) :
        p4s = eventVars["genP4"]
        for sign in ["+","-"] :
            b = p4s.at(eventVars["genIndicesb%s_t%sDaughters"%(sign,sign)][0])
            i0,i1 = eventVars["genIndicesW%sDaughters"%sign]
            if eventVars["genPdgId"][i0]>0 :
                q    = p4s.at(i0)
                qbar = p4s.at(i1)
            else :
                qbar = p4s.at(i0)
                q    = p4s.at(i1)
            self.fill(self.f(b.Dot(q)), self.f(b.Dot(qbar)), sign)
