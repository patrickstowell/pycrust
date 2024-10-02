#!/bin/sh

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
CURDIR=$SCRIPT_DIR

export PYCRUST_DB=$CURDIR/database/
export PYTHONPATH=$CURDIR:$PYTHONPATH
#export LD_LIBRARY_PATH=$CURDIR/PyCRUST/dependencies/:$LD_LIBRARY_PATH

#export G4NEUTRONHPDATA="$CURDIR/PyCRUST/dependencies/G4NDL4.6"
#export G4LEDATA="$CURDIR/PyCRUST/dependencies/data/G4EMLOW7.13"
#export G4LEVELGAMMADATA="$CURDIR/PyCRUST/dependencies/data/PhotonEvaporation5.7"
#export G4RADIOACTIVEDATA="$CURDIR/PyCRUST/dependencies/data/RadioactiveDecay5.6"
#export G4PARTICLEXSDATA="$CURDIR/PyCRUST/dependencies/data/G4PARTICLEXS3.1.1"
#export G4PIIDATA="$CURDIR/PyCRUST/dependencies/data/G4PII1.3"
#export G4REALSURFACEDATA="$CURDIR/PyCRUST/dependencies/data/RealSurface2.2"
#export G4SAIDXSDATA="$CURDIR/PyCRUST/dependencies/data/G4SAIDDATA2.0"
#export G4ABLADATA="$CURDIR/PyCRUST/dependencies/data/G4ABLA3.1"
#export G4INCLDATA="$CURDIR/PyCRUST/dependencies/data/G4INCL1.0"
#export G4ENSDFSTATEDATA="$CURDIR/PyCRUST/dependencies/data/G4ENSDFSTATE2.3"


