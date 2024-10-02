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
#include "OpticalSteppingAction.hh"

namespace CRESTA { // Main CRESTA Namespace
namespace Construction { // CRESTA Construction Sub Namespace
// ---------------------------------------------------------------------------

OpticalSteppingAction::OpticalSteppingAction()
  : G4UserSteppingAction()
{}

OpticalSteppingAction::~OpticalSteppingAction()
{}

void OpticalSteppingAction::UserSteppingAction(const G4Step* step)
{
  // Call Default
  G4UserSteppingAction::UserSteppingAction(step);

  // If there is a step for the current volume, check if it
  G4StepPoint* posstep = step->GetPostStepPoint();
  G4VSensitiveDetector* postsd = posstep->GetSensitiveDetector();
  VDetector* det = NULL;
  // std::cout << "Checking User Step Action " << postsd << std::endl;
  if (postsd) {
    det = dynamic_cast<VDetector*>(postsd);
  }

  if (det) {
    G4TrackStatus trackstatus = det->ManuallyProcessHits(step, NULL);
  }

  return;
}

// ---------------------------------------------------------------------------
} // - namespace Construction
} // - namespace CRESTA
