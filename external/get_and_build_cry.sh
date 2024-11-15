#wget https://nuclear.llnl.gov/simulation/cry_v1.7.tar.gz
#tar -zxvf cry_v1.7.tar.gz
#rm cry_v1.7.tar.gz
cd cry_v1.7
export CXXFLAGS="-fPIC"
export CPPFLAGS="-fPIC"
export CFLAGS="-fPIC"
make
rm -r install
mkdir install
mkdir install/include
mkdir install/lib

for file in $(find . -name "*.hh"); do cp $file install/include; done;
for file in $(find . -name "*.h"); do cp $file install/include; done;

cd ./geant/src/
sed -i '1i#include "G4SystemOfUnits.hh"' "PrimaryGeneratorAction.cc"
gcc --shared PrimaryGeneratorMessenger.cc PrimaryGeneratorAction.cc $(geant4-config --cflags) -o libG4CRY.so -I../include/  -I../../src/ $(geant4-config --libs) --std=c++17 -lstdc++ -lm -L../../lib/ -lCRY -fPIC
mv libG4CRY.so ../../install/lib/
cd ../../install/
cp -r ../data/ ./

echo "#!/bin/sh" > setup.CRY.sh
echo 'export CRY_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"' >> setup.CRY.sh
echo 'export G4PPYY_INCLUDE_DIRS="$CRY_ROOT/include/:$G4PPYY_INCLUDE_DIRS"'  >> setup.CRY.sh
echo 'export G4PPYY_INCLUDE_FILES="PrimaryGeneratorAction.hh:$G4PPYY_INCLUDE_FILES"'  >> setup.CRY.sh
echo 'export G4PPYY_LIBRARY_DIRS="$CRY_ROOT/lib/:$G4PPYY_LIBRARY_DIRS"' >> setup.CRY.sh
echo 'export G4PPYY_LIBRARY_FILES="libG4CRY.so:$G4PPYY_LIBRARY_FILES"' >> setup.CRY.sh
echo 'export CRY_DATA="$CRY_ROOT/data/"' >> setup.CRY.sh

cd ../../
