import supy, ROOT as r

class genLook(supy.analysis) :

    def listOfSteps(self,config) :
        shv = supy.steps.histos.value
        shpt, shmass = supy.steps.histos.pt, supy.steps.histos.mass
        shaeta, sheta = supy.steps.histos.absEta, supy.steps.histos.eta
        stepsList = [
            supy.steps.printer.progressPrinter(),
#            shv('n_jets',20, 0, 20),
#            shv('top_ene',20,0,1e4),
#            shpt("top_P4", 100,1,201),
#            shpt("jet_P4", 100,1,201, indices = 'Indicesjet_'),
#            sheta("top_P4", 100,-10,10),
#            sheta("antitop_P4", 100,-10,10),
#            shaeta("top_P4", 100,10,10),
#            shaeta("antitop_P4", 100,10,10),
#            shpt('TtbarP4', 50,0,+0.05e-4),
#            shmass('TtbarP4', 100,0,2e3),
#            shv('BoostZ',100, -1, +1),
#            shv('DeltaAbsRapidities',50, -3, +3),
            ]
#        dyh = steps.histos.DeltaAbsYHisto
        return stepsList

    def listOfCalculables(self,config) :
#        kin = calculables.kinematic
        return ( supy.calculables.zeroArgs(supy.calculables) +
                 [supy.calculables.other.fixedValue('Two',2) ]
#                 +[calculables.other.Indices(collection=("jet_",""))]
#                 +[kin.P4(collection = ("jet_",""))]
#                 +[kin.singleP4(collection = ("top_",""))]
#                 +[kin.singleP4(collection = ("antitop_",""))]
#                 +[kin.TtbarP4(),
#                   kin.AbsSumRapidities(),
#                   kin.DeltaAbsRapidities(),]
#                 +[kin.BoostZ()]
                 )

    def listOfSampleDictionaries(self) :
        exampleDict = supy.samples.SampleHolder()
        baseDir = '/home/gerbaudo/physics/atlas/fcnc/data/user.burdin.NTUP_TOP_ttbar_hqwb_109999_protos6000w2allLeptons_sample1.121020094657/'
        exampleDict.add("tHc", 'utils.io.fileListFromDisk("%s")'%baseDir,   xs = 1.0e+5 ) # pb
        return [exampleDict]

    def listOfSamples(self,config) :
        test = True #False
        nEventsMax= 1000 if test else None

        return (
            supy.samples.specify(names = "tHc", nEventsMax=nEventsMax, color = r.kBlack, markerStyle = 20)
            )

    def conclude(self,pars) :
        #make a pdf file with plots from the histograms created above
        org = self.organizer(pars)
        org.scale(lumiToUseInAbsenceOfData=1.0e-3) # /pb
        supy.plotter(org,
                     pdfFileName = self.pdfFileName(org.tag),
                     #samplesForRatios = ('SM', ['A2', 'A4', 'A6', 'P3']),
                     #sampleLabelsForRatios = ('SM','BSM'),
                     ).plotAll()
