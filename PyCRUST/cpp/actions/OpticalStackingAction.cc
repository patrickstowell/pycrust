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
#include "OpticalStackingAction.hh"

#include "flux/cry/CRYPrimaryGenerator.hh"

namespace CRESTA { // Main CRESTA Namespace
namespace Construction { // CRESTA Construction Sub Namespace
// ---------------------------------------------------------------------------

OpticalStackingAction::OpticalStackingAction() {
  fEnableTargetBoxCut = 0;
  fTargetBoxes.clear();
  fTargetBoxPositions.clear();
  fTargetBoxRadiusCutoff.clear();
}

OpticalStackingAction::~OpticalStackingAction() {
}

void OpticalStackingAction::SetTargetBoxes(std::vector<G4Box*> targetboxes,
                                          std::vector<G4ThreeVector> targetpos,
                                          std::vector<G4double> targetcuts){
  fEnableTargetBoxCut = 1;
  fTargetBoxes = targetboxes;
  fTargetBoxPositions = targetpos;
  fTargetBoxRadiusCutoff = targetcuts;
}

G4ClassificationOfNewTrack OpticalStackingAction::ClassifyNewTrack(const G4Track* track)
{
  if (fEnableTargetBoxCut){
    G4ThreeVector position = track->GetPosition();
    G4ThreeVector direction = track->GetMomentumDirection();
    for (int i = 0; i < fTargetBoxes.size(); i++){

      // ONLY CUT OUTSIDE RADIUS
      G4double r = (position - fTargetBoxPositions.at(i)).mag();
      // std::cout << "Radius : " << r << " " << fTargetBoxRadiusCutoff.at(i) << std::endl;
      if (r < fTargetBoxRadiusCutoff.at(i)) continue;

      // GET IF INTERSECTION
      G4double d = (fTargetBoxes.at(i))->DistanceToIn(
                    position - fTargetBoxPositions.at(i), direction);
                    if (d == kInfinity) return fKill;
    }
  }

  if (track->GetParentID() > 0) {
    // Kill secondary neutrinos
    if (track->GetDefinition() == G4NeutrinoE::NeutrinoE()) return fKill;
    if (track->GetDefinition() == G4AntiNeutrinoE::AntiNeutrinoE()) return fKill;
    if (track->GetDefinition() == G4NeutrinoMu::NeutrinoMu()) return fKill;
    if (track->GetDefinition() == G4AntiNeutrinoMu::AntiNeutrinoMu()) return fKill;
    if (track->GetDefinition() == G4NeutrinoTau::NeutrinoTau()) return fKill;
    if (track->GetDefinition() == G4AntiNeutrinoTau::AntiNeutrinoTau()) return fKill;

    // Kill extremely low energy electrons/gammas < 5 MeV
    // Path length in Al about 1cm at 5 MeV?
    if (track->GetDefinition() == G4Electron::Electron() ||
        track->GetDefinition() == G4Positron::Positron() ||
        track->GetDefinition() == G4Gamma::Gamma()) {
          if (track->GetTotalEnergy() < 1 * MeV) {
            return fKill;
          }
    }
  }

  // otherwise, return what Geant4 would have returned by itself
  return G4UserStackingAction::ClassifyNewTrack(track);
}

// ---------------------------------------------------------------------------
} // - namespace Construction
} // - namespace CRESTA
