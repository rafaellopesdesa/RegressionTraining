
# Goto cmssw base
cd /afs/cern.ch/work/t/tklijnsm/public/CMSSW_8_0_4/src/
cmsenv

# Go to copied directory
cd RegressionTrainingCopy/python

# Make the .config file (will be called new_config.config by default)
python Make_conf_photons.py

cd ..

# Begin the training
./regression.exe python/photon_config.config