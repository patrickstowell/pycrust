FROM almalinux:9.3

RUN yum update -y && yum install -y expat-devel libXmu-devel freeglut-devel git gcc g++ cmake nano wget python3 python3-pip git python3-devel && pip install "pybind11[global]"

WORKDIR /app
RUN <<EOF
wget https://geant4-data.web.cern.ch/releases/lib4.11.2.p02/Linux-g++11.4.1-Alma9.tar.gz
tar -zxf Linux-g++11.4.1-Alma9.tar.gz 
mkdir /app/Geant4-11.2.2-Linux/share/Geant4/data/
source /app/Geant4-11.2.2-Linux/bin/geant4.sh
EOF

RUN <<EOF
cd /app/Geant4-11.2.2-Linux/share/Geant4/data/
#wget https://cern.ch/geant4-data/datasets/G4NDL.4.7.1.tar.gz &
#wget https://cern.ch/geant4-data/datasets/G4EMLOW.8.5.tar.gz &
#wget https://cern.ch/geant4-data/datasets/G4PhotonEvaporation.5.7.tar.gz &
#wget https://cern.ch/geant4-data/datasets/G4RadioactiveDecay.5.6.tar.gz &
#wget https://cern.ch/geant4-data/datasets/G4PARTICLEXS.4.0.tar.gz &
#wget https://cern.ch/geant4-data/datasets/G4PII.1.3.tar.gz &
#wget https://cern.ch/geant4-data/datasets/G4RealSurface.2.2.tar.gz &
#wget https://cern.ch/geant4-data/datasets/G4SAIDDATA.2.0.tar.gz &
#wget https://cern.ch/geant4-data/datasets/G4ABLA.3.3.tar.gz &
#wget https://cern.ch/geant4-data/datasets/G4INCL.1.2.tar.gz &
wget https://cern.ch/geant4-data/datasets/G4ENSDFSTATE.2.3.tar.gz &
#wget https://cern.ch/geant4-data/datasets/G4TENDL.1.4.tar.gz & 

while true; do
  wait -n || {
    code="$?"
    ([[ $code = "127" ]] && exit 0 || exit "$code")
    break
  }
done;

for f in ./*.tar.gz;
do 
  tar -zxf $f
done

rm ./*.tar.gz
EOF


WORKDIR /app
ENV LD_LIBRARY_PATH=/app/Geant4-11.2.2-Linux/lib64
ENV GEANT4_DATA_DIR=/app/Geant4-11.2.2-Linux/share/Geant4/data
ENV PATH=/app/Geant4-11.2.2-Linux/bin:/root/.local/bin:/root/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin


RUN <<EOF
git clone https://github.com/patrickstowell/g4python.git
cd g4python
mkdir build
cd build   
cmake ../
make
make install
EOF

ENV PYTHONPATH=/root/opt/geant4/geant4py-11.0.0/site-packages/

WORKDIR /app/Geant4-11.2.2-Linux/bin/
RUN cat <<EOF > geant4-download
#!/bin/sh

LIBRARY=\$1
echo \$LIBRARY
cd \$GEANT4_DATA_DIR

if [[ "\$LIBRARY" == "" ]]
then
  echo "geant4-download [LIBNAME]"
  echo "- available options: ALL G4NDL G4EMLOW G4PhotonEvaporation G4RadioactiveDecay G4PARTICLEXS G4PII G4RealSurface G4SAIDDATA G4ABLA G4INCL G4ENSDFSTATE G4TENDL"
fi

if [[ "\$LIBRARY" == "G4NDL" || "\$LIBRARY" == "ALL" ]];
then
  if [ ! -d "G4NDL.4.7.1" ]; then
    wget https://cern.ch/geant4-data/datasets/G4NDL.4.7.1.tar.gz
    tar -zxf G4NDL.4.7.1.tar.gz
    rm G4NDL.4.7.1.tar.gz
  else
    echo "G4NDL present : \$GEANT4_DATA_DIR/G4NDL.4.7.1"
  fi
fi

if [[ "\$LIBRARY" == "G4EMLOW" || "\$LIBRARY" == "ALL" ]];
then
  if [ ! -d "G4EMLOW8.5" ]; then
    wget https://cern.ch/geant4-data/datasets/G4EMLOW.8.5.tar.gz
    tar -zxf G4EMLOW.8.5.tar.gz
    rm G4EMLOW.8.5.tar.gz
  else
    echo "G4EMLOW present : \$GEANT4_DATA_DIR/G4EMLOW8.5"
  fi
fi

if [[ "\$LIBRARY" == "G4PhotonEvaporation" || "\$LIBRARY" == "ALL" ]];
then
  if [ ! -d "PhotonEvaporation5.7" ]; then
    wget https://cern.ch/geant4-data/datasets/G4PhotonEvaporation.5.7.tar.gz
    tar -zxf G4PhotonEvaporation.5.7.tar.gz
    rm G4PhotonEvaporation.5.7.tar.gz
  else
    echo "G4PhotonEvaporation present : \$GEANT4_DATA_DIR/PhotonEvaporation5.7"
  fi
fi

if [[ "\$LIBRARY" == "G4RadioactiveDecay" || "\$LIBRARY" == "ALL" ]];
then
  if [ ! -d "RadioactiveDecay5.6" ]; then
    wget https://cern.ch/geant4-data/datasets/G4RadioactiveDecay.5.6.tar.gz
    tar -zxf G4RadioactiveDecay.5.6.tar.gz
    rm G4RadioactiveDecay.5.6.tar.gz
  else
    echo "G4RadioactiveDecay present : \$GEANT4_DATA_DIR/RadioactiveDecay5.6"
  fi
fi

if [[ "\$LIBRARY" == "G4PARTICLEXS" || "\$LIBRARY" == "ALL" ]];
then
  if [ ! -d "G4PARTICLEXS4.0" ]; then
    wget https://cern.ch/geant4-data/datasets/G4PARTICLEXS.4.0.tar.gz
    tar -zxf G4PARTICLEXS.4.0.tar.gz
    rm G4PARTICLEXS.4.0.tar.gz
  else
    echo "G4PARTICLEXS present : \$GEANT4_DATA_DIR/G4RealSurface2.2"
  fi
fi

if [[ "\$LIBRARY" == "G4PII" || "\$LIBRARY" == "ALL" ]];
then
  if [ ! -d "G4PII1.3" ]; then
    wget https://cern.ch/geant4-data/datasets/G4PII.1.3.tar.gz
    tar -zxf G4PII.1.3.tar.gz
    echo "G4PII downloaded ."
    rm G4PII.1.3.tar.gz
  else
    echo "G4PII present : \$GEANT4_DATA_DIR/G4PII1.3"
  fi
fi

if [[ "\$LIBRARY" == "G4RealSurface" || "\$LIBRARY" == "ALL" ]];
then
  if [ ! -d "RealSurface2.2" ]; then
    wget https://cern.ch/geant4-data/datasets/G4RealSurface.2.2.tar.gz
    tar -zxf G4RealSurface.2.2.tar.gz
    rm G4RealSurface.2.2.tar.gz
  else
    echo "G4RealSurface present : \$GEANT4_DATA_DIR/RealSurface2.2"
  fi
fi

if [[ "\$LIBRARY" == "G4SAIDDATA" || "\$LIBRARY" == "ALL" ]];
then
  if [ ! -d "G4SAIDDATA2.0" ]; then
    wget https://cern.ch/geant4-data/datasets/G4SAIDDATA.2.0.tar.gz
    tar -zxf G4SAIDDATA.2.0.tar.gz
    rm G4SAIDDATA.2.0.tar.gz
  else
    echo "G4SAIDDATA2 present : \$GEANT4_DATA_DIR/G4SAIDDATA2.0"
  fi
fi

if [[ "\$LIBRARY" == "G4ABLA" || "\$LIBRARY" == "ALL" ]];
then
  if [ ! -d "G4ABLA3.3" ]; then
    wget https://cern.ch/geant4-data/datasets/G4ABLA.3.3.tar.gz
    tar -zxf G4ABLA.3.3.tar.gz
    rm G4ABLA.3.3.tar.gz
  else
    echo "G4ABLA present : \$GEANT4_DATA_DIR/G4ABLA3.3"
  fi
fi

if [[ "\$LIBRARY" == "G4INCL" || "\$LIBRARY" == "ALL" ]];
then
  if [ ! -d "G4INCL1.2" ]; then
    wget https://cern.ch/geant4-data/datasets/G4INCL.1.2.tar.gz
    tar -zxf G4INCL.1.2.tar.gz
    rm G4INCL.1.2.tar.gz
  else
    echo "G4INCL present : \$GEANT4_DATA_DIR/G4INCL1.2"
  fi
fi

if [[ "\$LIBRARY" == "G4ENSDFSTATE" || "\$LIBRARY" == "ALL" ]];
then
  if [ ! -d "G4ENSDFSTATE2.3" ]; then
    wget https://cern.ch/geant4-data/datasets/G4ENSDFSTATE.2.3.tar.gz
    tar -zxf G4ENSDFSTATE.2.3.tar.gz
    rm G4ENSDFSTATE.2.3.tar.gz
  else
    echo "G4ENSDFSTATE present : \$GEANT4_DATA_DIR/G4INCL2.3"
  fi
fi

if [[ "\$LIBRARY" == "G4TENDL" || "\$LIBRARY" == "ALL" ]];
then
  if [ ! -d "G4TENDL1.4" ]; then
    wget https://cern.ch/geant4-data/datasets/G4TENDL.1.4.tar.gz
    tar -zxf G4TENDL.1.4.tar.gz
    rm G4TENDL.1.4.tar.gz
  else
    echo "G4EMLOW present : \$GEANT4_DATA_DIR/G4TENDL1.4"
  fi
fi

cd \$OLDPWD
EOF

RUN chmod +x /app/Geant4-11.2.2-Linux/bin/geant4-download





