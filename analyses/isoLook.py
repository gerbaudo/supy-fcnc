import calculables, samples, steps, supy, ROOT as r

class isoLook(supy.analysis) :
    def parameters(self) :
        GeV=1000.
        objects =  {'jet'  : ('jet_AntiKt4LCTopo_',''),
                    'met'  : ('MET_RefFinal_STVF_',''),
                    'muon' : ('mu_staco_',''),
                    'ele'  : ('el_','')
                    }
        lepton = self.vary()
        fieldsLepton =    ['name', 'ptMin', 'etaMax',   'isoVar', 'isoType']
        muonParameters =  ['muon',  20*GeV,      2.4, 'ptcone30', 'relative']
        eleParameters  =  ['ele',   20*GeV,      2.4, '',         '']
        lepton['mujets'] = dict(zip(fieldsLepton, muonParameters))
        lepton['mujets']['isoVars'] = ['etcone20', 'ptcone30']
        lepton['ejets'] = dict(zip(fieldsLepton, eleParameters))
        lepton['ejets']['isoVars'] = ['Etcone20', 'Etcone20_pt_corrected', 'ptcone30']
        #leptons['eljets'] = dict(zip(fieldsLepton, ['electron',  10,      2.4, '??',       'relative']))

        return {'objects'  : objects, 'lepton'   : lepton,
                'muon':  dict(zip(fieldsLepton, muonParameters)),
                'ele' :  dict(zip(fieldsLepton, eleParameters)),
                'minJetPt' : 10.0*GeV,
            }
    def listOfSteps(self,config) :
        ss = supy.steps
        shv = ss.histos.value
        shpt, shmass = ss.histos.pt, ss.histos.mass
        shaeta, sheta = ss.histos.absEta, ss.histos.eta
        pi = r.TMath.Pi()
        MeV2GeV = 1.0e+3
        objects = config['objects']
        isoVars = config['lepton']['isoVars']
        leptonObj = objects[config['lepton']['name']]
        lsteps = []
        lsteps += [ss.printer.progressPrinter()]
        #lsteps += [ss.printer.printstuff(['Indices'.join(objects['muon'])])]
        lsteps += [ss.filters.multiplicity('Indices'.join(leptonObj), min=1),]
        lsteps += [ss.histos.multiplicity('Indices'.join(leptonObj), 10),]
        lsteps += [shv(iv.join(leptonObj), 25, -4.*MeV2GeV, 26.*MeV2GeV, 'Indices'.join(leptonObj))
                   for iv in isoVars]

        return lsteps

    def listOfCalculables(self,config) :
        cg, cm = calculables.gen, calculables.muon
        objects = config['objects']
        muon = config['muon']
        ele = config['ele']
        lcals =  supy.calculables.zeroArgs(supy.calculables)
        lcals += [cm.Indices(objects['muon'], muon['ptMin'], muon['etaMax'])]
        lcals += supy.calculables.fromCollections(calculables.muon, [objects['muon'],])
        lcals += [cm.Indices(objects['ele'], ele['ptMin'], ele['etaMax'])]
        lcals += supy.calculables.fromCollections(calculables.electron, [objects['ele'],])

        return lcals

    def listOfSampleDictionaries(self) :
        return [samples.localTmp]

    def listOfSamples(self,config) :
        test = False #True
        nEventsMax= 1000 if test else None
        samples = ['tt-af',  'tt-fs',
                   'tHu-af', 'tHu-fs',
                   'tHb-af', 'tHb-fs',]
        return (
            supy.samples.specify(names ='tt-fs', nEventsMax=nEventsMax, color = r.kBlack, markerStyle = 20)
            +supy.samples.specify(names ='tt-af', nEventsMax=nEventsMax, color = r.kRed)
            +supy.samples.specify(names ='tHu-af', nEventsMax=nEventsMax, color = r.kBlue)
            +supy.samples.specify(names ='tHu-fs', nEventsMax=nEventsMax, color = r.kCyan)

            )

    def conclude(self,pars) :
        #make a pdf file with plots from the histograms created above
        org = self.organizer(pars)
        org.scale(lumiToUseInAbsenceOfData=1.0e-3) # /pb
        supy.plotter(org,
                     pdfFileName = self.pdfFileName(org.tag),
                     doLog=False,
                     blackList = ['lumiHisto','xsHisto','nJobsHisto',],
                     samplesForRatios=('tt-fs',['tt-af','tHu-af','tHu-fs']),
                     ).plotAll()
