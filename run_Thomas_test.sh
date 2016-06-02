pushd $CMSSW_BASE/src/HiggsAnalysis/GBRLikelihood/macros/
#pushd $CMSSW_BASE/src/
root -b -l -q $CMSSW_BASE/src/HiggsAnalysis/GBRLikelihood/macros/eregtestThomas.C
popd
mkdir -p plots
mv *.eps plots/
mv *.png plots/