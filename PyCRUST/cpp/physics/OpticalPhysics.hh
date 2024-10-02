#ifndef OpticalPhysics_h
#define OpticalPhysics_h 1
// #include "G4Headers.hh"
// #include "CorePackage.hh"
// #include "ProcessorPackage.hh"
// #include "DetectorPackage.hh"
// #include "DBPackage.hh"
// #include "TriggerPackage.hh"
// #include "GeometryPackage.hh"

#include "G4DecayPhysics.hh"
#include "G4RadioactiveDecayPhysics.hh"
#include "G4EmStandardPhysics.hh"
#include "G4OpticalPhysics.hh"
#include "Shielding.hh"
#include "G4HadronPhysicsShielding.hh"
#include "G4VModularPhysicsList.hh"
// #include "construction/GeometryManager.hh"

// namespace CRESTA { // Main CRESTA Namespace
// namespace Construction { // CRESTA Construction Sub Namespace
// ---------------------------------------------------------------------------

class OpticalPhysics: public G4VModularPhysicsList
{
public:
  /// constructor
  OpticalPhysics()
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
  auto params = G4OpticalParameters::Instance();
  params->SetBoundaryInvokeSD(true);
  params->Dump();

  G4OpticalPhysics* opticalPhysics = new G4OpticalPhysics();
  RegisterPhysics( opticalPhysics );
  // std::cout << opticalPhysics->GetOpRayleighProcess() << std::endl;


  //  opticalPhysics->SetWLSTimeProfile("delta");

  // opticalPhysics->SetScintillationYieldFactor(1.0);
  // opticalPhysics->SetScintillationExcitationRatio(0.0);

  // opticalPhysics->SetMaxNumPhotonsPerStep(10000);
  // opticalPhysics->SetMaxBetaChangePerStep(10.0);

  // opticalPhysics->SetTrackSecondariesFirst(kCerenkov,false);
  // opticalPhysics->SetTrackSecondariesFirst(kScintillation,false);

};


};

// ---------------------------------------------------------------------------
// } // - namespace Construction
// } // - namespace CRESTA
#endif
