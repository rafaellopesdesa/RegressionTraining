if [ $# -eq 0 ]; then
    echo "No arguments supplied; argument should be 'photon' or 'electron'"
    return 1
fi

PARTICLE="$1"

echo "Running training for $PARTICLE"

if [ $PARTICLE = "photon" ]; then
    cd python
    python Make_conf_photons.py
    cd ..
    ./regression.exe python/photon_config.config
elif [ $PARTICLE = "electron" ]; then
    cd python
    python Make_conf_electrons.py
    cd ..
    ./regression.exe python/electron_config.config
fi
