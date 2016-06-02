if [ $# -eq 0 ]; then
    echo "No arguments supplied; argument should be 'photon' or 'electron'"
    return 1
fi
PARTICLE="$1"

NTUPLEPATH="${CMSSW_BASE}/src/NTuples/"

if [ "$PARTICLE" = "electron" ]; then
    export FLATNTUPLE="$NTUPLEPATH/Ntup_01June_DoubleElectron.root"
    export NTUPLETREE="ElectronTree"
    export TRAININGOUTPUT="electronConfig_results.root"
elif [ "$PARTICLE" = "photon" ]; then
    export FLATNTUPLE="$NTUPLEPATH/Ntup_01June_DoublePhoton.root"
    export NTUPLETREE="PhotonTree"
    export TRAININGOUTPUT="photonConfig_results.root"
fi

#export TESTRUN="Y"
export TESTRUN="N"

TESTMACRO="$CMSSW_BASE/src/HiggsAnalysis/GBRLikelihood/macros/eregtestThomas.C"

echo "Running test macro $TESTMACRO"
echo "  FLATNTUPLE     = $FLATNTUPLE"
echo "  NTUPLETREE     = $NTUPLETREE"
echo "  TRAININGOUTPUT = $TRAININGOUTPUT"
echo

pushd $CMSSW_BASE/src/HiggsAnalysis/GBRLikelihood/macros/
root -b -l -q $CMSSW_BASE/src/HiggsAnalysis/GBRLikelihood/macros/eregtestThomas.C
popd
mkdir -p plots
mv *.eps plots/
mv *.png plots/