import calculables, steps, supy, ROOT as r

class isoLook(supy.analysis) :
    def parameters(self) :
        objects =  {'jet'  : ('jet_AntiKt4LCTopo_',''),
                    'met'  : ('MET_RefFinal_STVF_',''),
                    'muon' : ('mu_staco_',''),
                    'ele'  : ('el_','')
                    }
        lepton = self.vary()
        fieldsLepton =    ['name', 'ptMin', 'etaMax',   'isoVar', 'isoType']
        muonParameters =  ['muon',      10,      2.4, 'ptcone30', 'relative']
        lepton['mujets'] = dict(zip(fieldsLepton, muonParameters))
        #leptons['eljets'] = dict(zip(fieldsLepton, ['electron',  10,      2.4, '??',       'relative']))
        return {'objects'  : objects, 'lepton'   : lepton,
                'muon' : dict(zip(fieldsLepton, muonParameters)), 'minJetPt' : 10.0,
            }
    def listOfSteps(self,config) :
        ss = supy.steps
        shv = ss.histos.value
        shpt, shmass = ss.histos.pt, ss.histos.mass
        shaeta, sheta = ss.histos.absEta, ss.histos.eta
        pi = r.TMath.Pi()
        MeV2GeV = 1.0e+3
        objects = config['objects']
        lsteps = []
        lsteps += [ss.printer.progressPrinter()]
        #lsteps += [ss.printer.printstuff(['Indices'.join(objects['muon'])])]
        lsteps += [ss.histos.multiplicity('Indices'.join(objects['muon']), max=50),]

        return lsteps

    def listOfCalculables(self,config) :
        cg, cm = calculables.gen, calculables.muon
        objects = config['objects']
        muon = config['muon']
        lcals =  supy.calculables.zeroArgs(supy.calculables)
        lcals += [cm.Indices(objects['muon'], muon['ptMin'])]
        lcals += supy.calculables.fromCollections(calculables.muon, [objects['muon'],])

        return lcals

    def listOfSampleDictionaries(self) :
        exampleDict = supy.samples.SampleHolder()
        baseDir = '/home/gerbaudo/physics/atlas/fcnc/data/user.burdin.NTUP_TOP_ttbar_hqwb_109999_protos6000w2allLeptons_sample1.121020094657/'
        baseDir = '/tmp/gerbaudo/iso-2013-04-16/mc12_8TeV.105200.McAtNloJimmy_CT10_ttbar_LeptonFilter.merge.NTUP_TOP.e1513_a159_a171_r3549_p1269/'
        exampleDict.add("tHq", 'utils.io.fileListFromDisk("%s")'%baseDir,   xs = 1.0e+5 ) # pb
        return [exampleDict]

    def listOfSamples(self,config) :
        test = True #False
        nEventsMax= 10 if test else None

        return (
            supy.samples.specify(names = "tHq", nEventsMax=nEventsMax, color = r.kBlack, markerStyle = 20)
            )

    def conclude(self,pars) :
        #make a pdf file with plots from the histograms created above
        org = self.organizer(pars)
        org.scale(lumiToUseInAbsenceOfData=1.0e-3) # /pb
        supy.plotter(org,
                     pdfFileName = self.pdfFileName(org.tag),
                     ).plotAll()
