#!/usr/bin/env python
"""
Thomas:
"""

########################################
# Imports
########################################

import os

import ROOT

from Config import Config


########################################
# Main
########################################

def main():

    # Instantiate the Config class which prints a .config file
    config = Config()

    # filename of the input root file
    #root_file = 'FlatNtupFull_13May_SepTrees.root'
    #root_file = 'FlatNtupFull_18May_DoubleElectron.root'
    #ntup_path = os.path.abspath('../../NTuples/')

    root_file = 'output.root'
    ntup_path = '/afs/cern.ch/work/t/tklijnsm/EGM/CMSSW_8_0_4/src/SimpleFlatTreeProducer/SimpleNtuplizer/cfgs/'

    if not os.path.isdir( ntup_path ):
        print 'Error: "{0}"" is not a directory'.format( ntup_path )
    physical_path = lambda input_root_file: os.path.join( ntup_path, input_root_file )


    ########################################
    # BDT settings
    ########################################

    config.InputFiles = physical_path( root_file )

    config.Options = [
        "MinEvents=200",
        "Shrinkage=0.1",
        "NTrees=1000",
        "MinSignificance=5.0",
        "EventWeight=min(1,exp(-(gen_pt-50)/50))",
        ]

    config.Target           = "gen_E / EP_totEnergy"
    config.TargetError      = "1.253*abs( BDTresponse - gen_E / EP_totEnergy )"
    config.TargetComb       = "( gen_E - EP_totEnergy*BDTresponse ) / ( EP_trkMomentum - EP_totEnergy*BDTresponse )"
    config.HistoConfig      = "jobs/dummy_Histo.config"
    
    config.CutBase          = "eventNumber%2==0"
    config.CutEB            = "isEB"
    config.CutEE            = "!isEB"
    config.CutError         = "(eventNumber%2!=0) && (((eventNumber-1)/2)%4==3)"
    config.CutComb          = "(eventNumber%2!=0) && (((eventNumber-1)/2)%4!=3)"


    ########################################
    # Order Electron tree branches
    ########################################

    # Try to read tree branches from the input root file
    tree_gDirectory = 'een_analyzer/ElectronTree'

    # A bit of a pain to maintain:
    #Read_branches_from_rootfile( physical_path( root_file ), tree_gDirectory )

    # Instead, do manually:
    EE_vars = [
        'nPV',
        # 'eventNumber',
        'pt',
        'SC_eta',
        'SC_phi',
        'SC_rawEnergy',
        'SC_etaWidth',
        'SC_phiWidth',
        'SS_r9',
        'SS_seedEnergy_overRaw',
        'SS_eMax_overRaw',
        'SS_e2nd_overRaw',
        'SS_eHorizontal',
        'SS_eVertical',
        'SS_sigmaIetaIeta',
        'SS_sigmaIetaIphi',
        'SS_sigmaIphiIphi',
        'preshowerEnergy_overRaw',
        'SC_numberOfClustersSC',
        # 'isEB',
        # 'iEtaCoordinate',
        # 'iPhiCoordinate',
        # 'cryEtaCoordinate',
        # 'cryPhiCoordinate',
        'iXCoordinate',
        'iYCoordinate',
        'cryXCoordinate',
        'cryYCoordinate',
        'MaxDRclusterDR',
        'MaxDRclusterDPhi',
        'MaxDRclusterDEta',
        'MaxDRclusterRawEnergy_overRaw',
        # 'clusterRawEnergy_overRaw',
        # 'clusterDPhiToSeed',
        # 'clusterDEtaToSeed',
        ]

    EB_vars = [
        'nPV',
        # 'eventNumber',
        'pt',
        'SC_eta',
        'SC_phi',
        'SC_rawEnergy',
        'SC_etaWidth',
        'SC_phiWidth',
        'SS_r9',
        'SS_seedEnergy_overRaw',
        'SS_eMax_overRaw',
        'SS_e2nd_overRaw',
        'SS_eHorizontal',
        'SS_eVertical',
        'SS_sigmaIetaIeta',
        'SS_sigmaIetaIphi',
        'SS_sigmaIphiIphi',
        'preshowerEnergy_overRaw',
        'SC_numberOfClustersSC',
        # 'isEB',
        'iEtaCoordinate',
        'iPhiCoordinate',
        'cryEtaCoordinate',
        'cryPhiCoordinate',
        # 'iXCoordinate',
        # 'iYCoordinate',
        # 'cryXCoordinate',
        # 'cryYCoordinate',
        'MaxDRclusterDR',
        'MaxDRclusterDPhi',
        'MaxDRclusterDEta',
        'MaxDRclusterRawEnergy_overRaw',
        # 'clusterRawEnergy_overRaw',
        # 'clusterDPhiToSeed',
        # 'clusterDEtaToSeed',
        ]


    # Add branches with indices manually
    for b in [ 'clusterRawEnergy_overRaw', 'clusterDPhiToSeed', 'clusterDEtaToSeed' ]:
        for i in range(3):
            EE_vars.append( b + '[{0}]'.format(i) )
            EB_vars.append( b + '[{0}]'.format(i) )

    print 'Using the following branches for EE:'
    print '    ' + '\n    '.join( EE_vars )
    print 'Using the following branches for EB:'
    print '    ' + '\n    '.join( EB_vars )

    # Write to class
    #config.Tree        = tree_gDirectory
    config.Tree          = tree_gDirectory
    config.VariablesEE   = EE_vars
    config.VariablesEB   = EB_vars

    #config.VariablesComb = Ep_branches
    config.VariablesComb = [
        'EP_totEnergy * BDTresponse',
        'BDTerror/BDTresponse',
        'EP_trkMomentum',
        'EP_trkMomentumRelError',
        'BDTerror/BDTresponse/EP_trkMomentumRelError',
        'EP_totEnergy*BDTresponse/EP_trkMomentum',
        ( 'EP_totEnergy*BDTresponse/EP_trkMomentum  *' +
          'sqrt( BDTerror/BDTresponse*BDTerror/BDTresponse + EP_trkMomentumRelError*EP_trkMomentumRelError)' ),
        'EP_ecalDriven',
        'EP_trackerDrivenSeed',
        'EP_classification',
        'EP_isEB',
        ]


    ########################################
    # Output config file
    ########################################

    out_filename = 'new_config.config'
    config.Parse( out_filename )

    # Test if the config file can be read by ROOT TEnv
    print '\nReading in {0} and trying ROOT.TEnv( ..., 0 ):'.format( out_filename )
    I_TEnv = ROOT.TEnv()
    I_TEnv.ReadFile( out_filename, 0 )
    I_TEnv.Print()
    print 'Exited normally'
    print '='*70
    print


########################################
# Functions
########################################

def Filter( full_list, sel_list ):
    # Functions that FILTERS OUT selection criteria

    # Return the full list if sel_list is empty or None
    if not sel_list:
        return full_list
    elif len(sel_list)==0:
        return full_list

    ret_list = []

    for item in full_list:
        
        # Loop over selection criteria; if found, don't add the item to the output list
        add_item = True
        for sel in sel_list:
            if sel in item:
                add_item = False

        if add_item:
            ret_list.append( item )

    return ret_list



def Read_branches_from_rootfile( root_file, tree_gDirectory ):

    root_fp = ROOT.TFile.Open( root_file )
    tree = root_fp.Get( tree_gDirectory )
    all_branches = [ i.GetName() for i in tree.GetListOfBranches() ]

    print 'All available branches in ' + root_file + ':'
    print '    ' + '\n    '.join( all_branches )

    # Split into regular branches and Ep branches
    branches    = [ b for b in all_branches if not 'EP_' in b ]
    Ep_branches = [ b for b in all_branches if 'EP_' in b ]

    # Apply filters
    exclusively_EB = [
        'iEtaCoordinate',
        'iPhiCoordinate',
        'cryEtaCoordinate',
        'cryPhiCoordinate',
        ]

    exclusively_EE = [
        'iXCoordinate',
        'iYCoordinate',
        'cryXCoordinate',
        'cryYCoordinate',
        'preshowerEnergy',
        ]

    exclude_vars = [

        # Only there for selection purposes
        'eventNumber',

        # Don't use the gen branches as regression variables
        'gen_',
        'match',

        # These variables need to be done with indices
        'clusterRawEnergy',
        'clusterDPhiToSeed',
        'clusterDEtaToSeed',

        ]

    EE_vars = Filter( Filter( branches, exclusively_EB ), exclude_vars )
    EB_vars = Filter( Filter( branches, exclusively_EE ), exclude_vars )

    return ( EE_vars, EB_vars )


########################################
# End of Main
########################################
if __name__ == "__main__":
    main()