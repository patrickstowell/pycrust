#pragma once
#include "PyCRUST.h"

CRYPrimaryGeneratorAction(){
{
  // Setup Defaults
  fGenNeutrons  = true;
  fGenProtons   = true;
  fGenGammas    = true;
  fGenElectrons = true;
  fGenMuons     = true;
  fGenPions     = true;
  fAltitude     = 0.0; // Sea Level
  fLatitude     = 0.0; // Equator

  fDate = "1-1-2007"; // CRY Default
  fLateralBoxSize = 30*m;

  fDataDirectory = pc::get_source() + "/data/cry/";
  fGenNeutrons  = true;
  fGenProtons   = true;
  fGenGammas    = true;
  fGenElectrons = true;
  fGenMuons     = true;
  fGenPions     = true;

  // Call update CRY to load tables given the current config
  UpdateCRY();

  // create a vector to store the CRY particle properties
  vect = new std::vector<CRYParticle*>;

  // Create the table containing all particle names
  particleTable = G4ParticleTable::GetParticleTable();

  // define a particle gun
  particleGun = new G4ParticleGun();
}

//----------------------------------------------------------------------------//
CRYPrimaryGenerator::~CRYPrimaryGenerator()
{
  delete fSourceBox;
  delete gen;

  vect->clear();
  delete vect;
}

//----------------------------------------------------------------------------//
void CRYPrimaryGenerator::UpdateCRY()
{
  std::ostringstream cryconfigs;

  // Fill Particle Definitions
  cryconfigs << " returnNeutrons "  << int(fGenNeutrons);
  cryconfigs << " returnProtons "   << int(fGenProtons);
  cryconfigs << " returnGammas "    << int(fGenGammas);
  cryconfigs << " returnElectrons " << int(fGenElectrons);
  cryconfigs << " returnMuons "     << int(fGenMuons);

  // Fill Altitude, Latitude, and Date Definition
  cryconfigs << " altitude " << fAltitude;
  cryconfigs << " latitude " << fLatitude;
  cryconfigs << " date " << fDate;

  // Fill truncation if provided
  if (fNParticlesMin > 0) {
    cryconfigs << " nParticlesMin " << fNParticlesMin;
  }
  if (fNParticlesMax > 0) {
    cryconfigs << " nParticlesMax " << fNParticlesMax;
  }

  // Get Lateral Box Size from the current source box
  cryconfigs << " subboxLength " << fLateralBoxSize;

  // Make input setup
  std::string configinputs = cryconfigs.str();
  CRYSetup *setup = new CRYSetup(configinputs, fDataDirectory);

  // Replace Generator
  gen = new CRYGenerator(setup);

  // set random number generator
  RNGWrapper<CLHEP::HepRandomEngine>::set(CLHEP::HepRandom::getTheEngine(), &CLHEP::HepRandomEngine::flat);
  setup->setRandomFunction(RNGWrapper<CLHEP::HepRandomEngine>::rng);

  cryConfigured = true;
}



void CRYPrimaryGenerator::GeneratePrimaries(G4Event* anEvent)
{
  if (!cryConfigured) {
    G4String* str = new G4String("CRY library was not successfully initialized");
    //G4Exception(*str);
    G4Exception("CRYPrimaryGenerator", "1",
                RunMustBeAborted, *str);
  }

  G4String particleName;
  uint stacksize = 0;
  uint throws = 0;
  std::vector<bool> goodtrack;

  do {
    throws++;
    vect->clear();
    gen->genEvent(vect);
    fExposureTime = gen->timeSimulated();
    fNthrows++;

    goodtrack = std::vector<bool>(vect->size(), false);

    // Number of trajectories that intercept at least one targetbox
    stacksize = 0;
    // Loop over all vectors and change their y values to match our box position
    for (unsigned j = 0; j < vect->size(); j++) {

      // Apply offsets according to where the fSourceBox was placed.
      G4ThreeVector boxposthrow = fSourceBox->GetPointOnSurface() + fSourceBoxPosition;

      // Setup new vector position
      G4ThreeVector position  = G4ThreeVector((*vect)[j]->x() * m, (*vect)[j]->y() * m, boxposthrow[2]);
      (*vect)[j]->setPosition(position[0], position[1], position[2]);

      // Get Direction for trjacetory pre-selection
      G4ThreeVector direction = G4ThreeVector((*vect)[j]->u(), (*vect)[j]->v(), (*vect)[j]->w());
      bool good_traj = (fTargetBoxes.size() == 0);

      // If its outside our energy cut its a bad trajectory
      if ((fMaxEnergy > 0 && (*vect)[j]->ke()*MeV > fMaxEnergy) ||
          (fMinEnergy > 0 && (*vect)[j]->ke()*MeV < fMinEnergy)) {
        good_traj = false;
        continue;
      }

      // Make sure trajectory falls inside our target box if we have one.
      for (uint i = 0; i < fTargetBoxes.size(); i++) {
        G4double d = (fTargetBoxes.at(i))->DistanceToIn(
                       position - fTargetBoxPositions.at(i), direction);

        if (d != kInfinity) {
          good_traj = true;
          break;
        }
      }

      // If one good trajectory then event is good.
      if (good_traj) {
        stacksize++;
        goodtrack[j] = true;
      }
    }

    if (stacksize == 0) {
      for (unsigned j = 0; j < vect->size(); j++) {
        if (!(*vect)[j]) continue;
        delete (*vect)[j];
      }
      goodtrack.clear();
    }

  } while (stacksize < 1 and throws < 1E8);

  // Throw if couldn't create events with good trajectories
  if (throws >= 1E8) {
    std::cout << "Failed to find any good events in 1E8 tries!" << std::endl;
    throw;
  }

  fParticleMult = (G4double) vect->size();
  fParticlePDG = 0;
  fParticlePos = G4ThreeVector(0,0,0);
  fParticleDir = G4ThreeVector(0,0,0);
  fParticleEnergy = 0;

  for ( unsigned j = 0; j < vect->size(); j++) {

    // Skip if trajectory was NULL
    if (!(*vect)[j]) continue;

    if (!fTargetBoxes.size() or !fAggressiveSelection or goodtrack[j]) {

      // Add particles to gun
      particleGun->SetParticleDefinition(particleTable->FindParticle((*vect)[j]->PDGid()));
      particleGun->SetParticleEnergy((*vect)[j]->ke()*MeV);
      particleGun->SetParticlePosition(G4ThreeVector((*vect)[j]->x(), (*vect)[j]->y(), (*vect)[j]->z()));
      particleGun->SetParticleMomentumDirection(G4ThreeVector((*vect)[j]->u(), (*vect)[j]->v(), (*vect)[j]->w()));
      particleGun->SetParticleTime((*vect)[j]->t());
      particleGun->GeneratePrimaryVertex(anEvent);
    }

    // Remove this particle
    delete (*vect)[j];
  }

}
//------------------------------------------------------------------


