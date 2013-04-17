from supy.samples import SampleHolder
localTmp = SampleHolder()

xSecVal = 1.0 #pb # just want to make a relative comparison
baseDir='/tmp/gerbaudo/iso-2013-04-16' # download these samples with dq2 to this tmp dir
samples = {
    #'tt-af'  : 'mc12_8TeV.105200.McAtNloJimmy_CT10_ttbar_LeptonFilter.merge.NTUP_TOP.e1513_a159_a171_r3549_p1269',
    #'tt-fs'  : 'mc12_8TeV.105200.McAtNloJimmy_CT10_ttbar_LeptonFilter.merge.NTUP_TOP.e1513_s1469_s1470_r3842_r3549_p1269', # empty?
    'tt-af' : 'mc12_8TeV.105200.McAtNloJimmy_CT10_ttbar_LeptonFilter.merge.NTUP_TOP.e1193_a159_a171_r3549_p1269',
    'tt-fs' :'mc12_8TeV.105200.McAtNloJimmy_CT10_ttbar_LeptonFilter.merge.NTUP_TOP.e1193_s1469_s1470_r3542_r3549_p1269',
    'tHu-af' : 'mc12_8TeV.110500.ProtosPythia_P2011CCTEQ6L1_tt_tbWlep_tuHincl.merge.NTUP_TOP.e1769_a188_a171_r3549_p1269',
    'tHu-fs' : 'mc12_8TeV.110500.ProtosPythia_P2011CCTEQ6L1_tt_tbWlep_tuHincl.merge.NTUP_TOP.e1769_s1581_s1586_r3658_r3549_p1269',
    'tHb-af' : 'mc12_8TeV.110501.ProtosPythia_P2011CCTEQ6L1_tt_tbWlep_tcHincl.merge.NTUP_TOP.e1769_a188_a171_r3549_p1269',
    'tHb-fs' : 'mc12_8TeV.110501.ProtosPythia_P2011CCTEQ6L1_tt_tbWlep_tcHincl.merge.NTUP_TOP.e1769_s1581_s1586_r3658_r3549_p1269'
}

for k,v in samples.iteritems() :
    localTmp.add(k, 'utils.io.fileListFromDisk("%s/%s/")'%(baseDir,v), xs=xSecVal)
