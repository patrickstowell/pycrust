// ********************************************************************
// * License and Disclaimer                                           *
// *                                                                  *
// * The  Geant4 software  is  copyright of the Copyright Holders  of *
// * the Geant4 Collaboration.  It is provided  under  the terms  and *
// * conditions of the Geant4 Software License,  included in the file *
// * LICENSE and available at  http://cern.ch/geant4/license .  These *
// * include a list of copyright holders.                             *
// *                                                                  *
// * Neither the authors of this software system, nor their employing *
// * institutes,nor the agencies providing financial support for this *
// * work  make  any representation or  warranty, express or implied, *
// * regarding  this  software system or assume any liability for its *
// * use.  Please see the license in the file  LICENSE  and URL above *
// * for the full disclaimer and the limitation of liability.         *
// *                                                                  *
// * This  code  implementation is the result of  the  scientific and *
// * technical work of the GEANT4 collaboration.                      *
// * By using,  copying,  modifying or  distributing the software (or *
// * any work based  on the software)  you  agree  to acknowledge its *
// * use  in  resulting  scientific  publications,  and indicate your *
// * acceptance of all terms of the Geant4 Software license.          *
// ********************************************************************
#include "OpticalActionInitialization.hh"
#include "OpticalRunAction.hh"
#include "OpticalStackingAction.hh"
#include "OpticalSteppingAction.hh"
#include "construction/FluxConstruction.hh"

namespace CRESTA { // Main Optical Namespace
namespace Construction { // Optical Construction Sub Namespace
// ---------------------------------------------------------------------------

OpticalActionInitialization::OpticalActionInitialization()
  : G4VUserActionInitialization()
{
  // Get user defined target boxes
  BuildTargetBoxes();
}

OpticalActionInitialization::~OpticalActionInitialization()
{}

void OpticalActionInitialization::BuildForMaster() const
{


  // Set run action from factory
  G4UserRunAction* run = new OpticalRunAction();
  if (run) SetUserAction(run);
  else {
  	std::cout << "No run loaded in master!" << std::endl;
  	throw;
  }
}

void OpticalActionInitialization::Build() const
{
  // Set flux action from factory
  G4VUserPrimaryGeneratorAction* gen = FluxConstruction::Build();
  if (gen) { SetUserAction(gen); }
  else {
  	std::cout << "No generator loaded in master!" << std::endl;
  	throw;
  }

  // Set run action from factory
  G4UserRunAction* run = new OpticalRunAction();
  if (run) { SetUserAction(run); }
  else {
  	std::cout << "No run loaded in slave!" << std::endl;
  	throw;
  }

  // Set event action from factory
  // G4UserEventAction* event = NULL;
  // if (event) { SetUserAction(event); }

  // Set stacking action from factory
  OpticalStackingAction* stack = new OpticalStackingAction();
  if (stack) {
    stack->SetTargetBoxes(fTargetBoxes,
                          fTargetBoxPositions,
                          fTargetBoxRadiusCutoff);
    SetUserAction(stack);
  }


  // Set tracking action from factory
  //  G4UserTrackingAction* track = NULL;
  //  if (track) { SetUserAction(track); }

  // Set stepping action from factory
   G4UserSteppingAction* step = new OpticalSteppingAction();
   if (step) { SetUserAction(step); }

}

void OpticalActionInitialization::BuildTargetBoxes(){

  std::vector<DBTable> targetlinks = DB::Get()->GetTableGroup("FLUX");
  for (uint i = 0; i < targetlinks.size(); i++) {
    DBTable tbl = targetlinks[i];

    // Select tables with target box names
    std::string index = tbl.GetIndexName();
    if (index.find("target_box_") == std::string::npos) continue;

    // If it has position and size we can use it
    if (!tbl.Has("position") || !tbl.Has("size")) {
      std::cout << "Failed to find/create target box!" << std::endl;
      throw;
    }

    // Allow to be disabled.
    if (!tbl.Has("stackingcuts") || !tbl.GetB("stackingcuts")) continue;

    // Create objects
    std::vector<G4double> size = tbl.GetVecG4D("size");
    std::vector<G4double> pos = tbl.GetVecG4D("position");

    G4Box* box_sol = new G4Box(index, 0.5 * size[0], 0.5 * size[1], 0.5 * size[2]);
    G4ThreeVector box_pos = G4ThreeVector(pos[0], pos[1], pos[2]);
    std::cout << "Target box position: " << box_pos << std::endl;
    std::cout << "Target box size: " << G4ThreeVector(size[0],size[1],size[2]) << std::endl;

    G4double radiuscutoff = tbl.GetG4D("radiuscutoff");

    // Save Box
    fTargetBoxes.push_back(box_sol);
    fTargetBoxPositions.push_back(box_pos);
    fTargetBoxRadiusCutoff.push_back(radiuscutoff);
  }
}

// ---------------------------------------------------------------------------
} // - namespace Construction
} // - namespace Optical
