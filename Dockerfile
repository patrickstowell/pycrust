FROM johnpatrickstowell/g4ppyy:latest
WORKDIR /data/
COPY ./ ./
ENV PATH=/data/pycrust/scripts/:$PATH
USER root
RUN cd /data/external/; source ./get_and_build_cry.sh; source /data/external/cry_v1.7/install/setup.CRY.sh
RUN chmod -R 777 /data/
COPY ./macros/ /usr/local/lib/python3.9/site-packages/g4ppyy/macros/                 

USER g4user
RUN source /data/external/cry_v1.7/install/setup.CRY.sh
ENV CRY_DATA=/data/external/cry_v1.7/install/data/
ENV G4PPYY_LIBRARY_FILES=libG4CRY.so:
ENV G4PPYY_LIBRARY_DIRS=/data/external/cry_v1.7/install/lib/:
ENV G4PPYY_INCLUDE_FILES=PrimaryGeneratorAction.hh:
ENV CRY_ROOT=/data/external/cry_v1.7/install
ENV G4PPYY_INCLUDE_DIRS=/data/external/cry_v1.7/install/include/:
