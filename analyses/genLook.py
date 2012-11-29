import calculables, steps, supy, ROOT as r

class genLook(supy.analysis) :

    def listOfSteps(self,config) :
        shv = supy.steps.histos.value
        shpt, shmass = supy.steps.histos.pt, supy.steps.histos.mass
        shaeta, sheta = supy.steps.histos.absEta, supy.steps.histos.eta
        def dropInd(idxName) :
            return idxName.replace('Index','').replace('genIndices','').replace('Indices','')
        indices = ['smTopIndex','fcncTopIndex']+["genIndices%s"%i for i in
                                                 ['b_tChild','W_tChild','l_WChild','v_WChild',
                                                  'higgs',
                                                  'b_hChild','bbar_hChild',
                                                  'q_tChild']]
        stepsList = [
            supy.steps.printer.progressPrinter(),
            supy.steps.histos.multiplicity("genP4", max=50),
            #steps.gen.particlePrinter(),
            #steps.gen.ttbarPrinter(),
            supy.steps.histos.multiplicity('smTopIndex', max=4),
            supy.steps.filters.multiplicity('genIndicesttbar',min=2,max=2),
            #supy.steps.printer.printstuff(['fcncTopIndex','genIndiceshiggs','genIndicesW_tChild','genIndicesq_tChild']),
            supy.steps.filters.multiplicity('genIndicesb_hChild',min=2,max=2),
            supy.steps.filters.multiplicity('genIndicesl_WChild',min=1,max=1),
            ] + \
            [supy.steps.histos.pt("genP4",  20, 0.0, 300.0*1.e3, indices = ii, index = 0, xtitle = dropInd(ii))
             for ii in indices] + \
            [supy.steps.histos.eta("genP4",  20, -4.0, +4.0, indices = ii, index = 0, xtitle = dropInd(ii))
             for ii in indices] + \
            [supy.steps.histos.phi("genP4",  20, -4.0, +4.0, indices = ii, index = 0, xtitle = dropInd(ii))
             for ii in indices]
        return stepsList

    def listOfCalculables(self,config) :
#        kin = calculables.kinematic
        return ( supy.calculables.zeroArgs(supy.calculables) +
                 [calculables.gen.genP4(),] +
                 [calculables.gen.genIndices([-6,+6],'ttbar'),
                  calculables.gen.genIndices([6],'t'),
                  calculables.gen.genIndices([-6],'tbar'),
                  calculables.gen.smTopIndex(),
                  calculables.gen.fcncTopIndex(),
                  calculables.gen.genIndices(pdgs = [-5,5], label = "b_tChild", parentPdgs = [-6,6]),
                  calculables.gen.genIndices(pdgs = [-24,24], label = "W_tChild", parentPdgs = [-6,6]),
                  calculables.gen.genIndices(pdgs = [-11,11]+[-13,13]+[-15,15], label = "l_WChild", parentIndexLabel='genIndicesW_tChild'),
                  calculables.gen.genIndices(pdgs = [-12,12]+[-14,14]+[-16,16], label = "v_WChild", parentIndexLabel='genIndicesW_tChild'),
                  calculables.gen.genIndices(pdgs = [25], label = "higgs", parentIndexLabel='fcncTopIndex'),
                  #calculables.gen.genIndices(label = "all_fcncTopChild", parentIndexLabel='fcncTopIndex'),
                  calculables.gen.genIndices(pdgs = [-5,5], label = "bbbar_hChild", parentPdgs = [25],maxLen=2),
                  calculables.gen.genIndices(pdgs = [ 5], label = "b_hChild", parentPdgs = [25],maxLen=2),
                  calculables.gen.genIndices(pdgs = [-5], label = "bbar_hChild", parentPdgs = [25],maxLen=2),
                  calculables.gen.genIndices(pdgs = [-1,1,-2,2,-3,3,-4,4], label = "q_tChild", parentIndexLabel='fcncTopIndex'),
                  ]
                 +[calculables.gen.p4Item(l) for l in
                   ['smTopIndex','fcncTopIndex']+
                   ["genIndices%s"%i for i in
                    ['b_tChild','W_tChild','l_WChild','v_WChild',
                     'higgs',
                     'b_hChild','bbar_hChild',
                     'q_tChild']]]
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
