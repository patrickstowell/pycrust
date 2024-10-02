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
#ifndef __CRESTA_OpticalStackingAction_HH__
#define __CRESTA_OpticalStackingAction_HH__
#include "G4Headers.hh"
#include "CorePackage.hh"
#include "FluxPackage.hh"

namespace CRESTA { // Main CRESTA Namespace
namespace Construction { // CRESTA Construction Sub Namespace
// ---------------------------------------------------------------------------

/// \class OpticalStackingAction
/// \brief Stacking action class : manage the newly generated particles
class OpticalStackingAction : public G4UserStackingAction
{
public:

  /// Constructor
  OpticalStackingAction();
  /// Destructor
  virtual ~OpticalStackingAction();

  /// Return classification status of new track
  virtual G4ClassificationOfNewTrack ClassifyNewTrack(const G4Track*);

  void SetTargetBoxes(std::vector<G4Box*> targetboxes,
                                            std::vector<G4ThreeVector> targetpos,
                                            std::vector<G4double> targetcuts);
private:
  std::vector<G4Box*> fTargetBoxes; ///< List of user defined targets
  std::vector<G4ThreeVector> fTargetBoxPositions; ///< Position of user defined targets in world
  std::vector<G4double> fTargetBoxRadiusCutoff;
  bool fEnableTargetBoxCut;
};

// ---------------------------------------------------------------------------
} // - namespace CRESTA
} // - namespace CRESTA
#endif
