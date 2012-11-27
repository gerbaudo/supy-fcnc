import calculables, steps, supy, ROOT as r

class genLook(supy.analysis) :

    def listOfSteps(self,config) :
        shv = supy.steps.histos.value
        shpt, shmass = supy.steps.histos.pt, supy.steps.histos.mass
        shaeta, sheta = supy.steps.histos.absEta, supy.steps.histos.eta
        stepsList = [
            supy.steps.printer.progressPrinter(),
            supy.steps.histos.multiplicity("genP4", max=50),
            #steps.gen.particlePrinter(),
            steps.gen.ttbarPrinter(),
            ]
        return stepsList

    def listOfCalculables(self,config) :
#        kin = calculables.kinematic
        return ( supy.calculables.zeroArgs(supy.calculables) +
                 [supy.calculables.other.fixedValue('Two',2) ] +
                 [calculables.gen.genP4(),]
                 )

    def listOfSampleDictionaries(self) :
        exampleDict = supy.samples.SampleHolder()
        baseDir = '/home/gerbaudo/physics/atlas/fcnc/data/user.burdin.NTUP_TOP_ttbar_hqwb_109999_protos6000w2allLeptons_sample1.121020094657/'
        exampleDict.add("tHc", 'utils.io.fileListFromDisk("%s")'%baseDir,   xs = 1.0e+5 ) # pb
        return [exampleDict]

    def listOfSamples(self,config) :
        test = True #False
        nEventsMax= 10 if test else None

        return (
            supy.samples.specify(names = "tHc", nEventsMax=nEventsMax, color = r.kBlack, markerStyle = 20)
            )

    def conclude(self,pars) :
        #make a pdf file with plots from the histograms created above
        org = self.organizer(pars)
        org.scale(lumiToUseInAbsenceOfData=1.0e-3) # /pb
        supy.plotter(org,
                     pdfFileName = self.pdfFileName(org.tag),
                     ).plotAll()
