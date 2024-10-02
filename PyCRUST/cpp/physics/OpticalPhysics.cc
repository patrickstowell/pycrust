// Copyright 2018 P. Stowell, C. Steer, L. Thompson

/*******************************************************************************
*    This file is part of CRESTA.
*
*    CRESTA is free software: you can redistribute it and/or modify
*    it under the terms of the GNU General Public License as published by
*    the Free Software Foundation, either version 3 of the License, or
*    (at your option) any later version.
*
*    CRESTA is distributed in the hope that it will be useful,
*    but WITHOUT ANY WARRANTY; without even the implied warranty of
*    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*    GNU General Public License for more details.
*
*    You should have received a copy of the GNU General Public License
*    along with CRESTA.  If not, see <http://www.gnu.org/licenses/>.
*******************************************************************************/
#include "OpticalPhysics.hh"

#include "G4DecayPhysics.hh"
#include "G4RadioactiveDecayPhysics.hh"
#include "G4EmStandardPhysics.hh"
#include "G4OpticalPhysics.hh"
#include "Shielding.hh"
#include "G4HadronPhysicsShielding.hh"

// namespace CRESTA { // Main CRESTA Namespace
// namespace Construction { // CRESTA Construction Sub Namespace
// ---------------------------------------------------------------------------

OpticalPhysics::OpticalPhysics()
: G4VModularPhysicsList(){

  // Create a modular physics list and register only a
  // few modules for it: EM interactions, decay of
  // particles and radioactive decay. No hadronic physics
  // is provided in the example.

  SetVerboseLevel(1);

  // Default Decay Physics
  RegisterPhysics(new G4DecayPhysics());

  // Default Radioactive Decay Physics
  RegisterPhysics(new G4RadioactiveDecayPhysics());

  // Standard EM Physics
  RegisterPhysics(new G4EmStandardPhysics());

  RegisterPhysics(new G4HadronPhysicsShielding());

  G4OpticalPhysics* opticalPhysics = new G4OpticalPhysics();
  RegisterPhysics( opticalPhysics );

  std::cout << opticalPhysics->GetOpRayleighProcess() << std::endl;

   opticalPhysics->SetWLSTimeProfile("delta");

  opticalPhysics->SetScintillationYieldFactor(1.0);
  opticalPhysics->SetScintillationExcitationRatio(0.0);

  opticalPhysics->SetMaxNumPhotonsPerStep(10000);
  opticalPhysics->SetMaxBetaChangePerStep(10.0);

  opticalPhysics->SetTrackSecondariesFirst(kCerenkov,false);
  opticalPhysics->SetTrackSecondariesFirst(kScintillation,false);

sdsad
}

OpticalPhysics::~OpticalPhysics()
{
}

void OpticalPhysics::SetCuts()
{
  // The method SetCuts() is mandatory in the interface. Here, one just use
  // the default SetCuts() provided by the base class.
  G4VUserPhysicsList::SetCuts();
}

// ---------------------------------------------------------------------------
// } // - namespace Construction
// } // - namespace CRESTA
