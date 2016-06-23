
# Goto cmssw base
cd /afs/cern.ch/work/t/tklijnsm/public/CMSSW_8_0_4/src/

eval `scramv1 runtime -sh`

cd RegressionTrainingCopy

./create_config_and_run.sh electron

echo "End of job"