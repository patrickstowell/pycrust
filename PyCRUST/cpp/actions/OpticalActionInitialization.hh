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
#ifndef __CRESTA_OpticalActionInitialization_hh__
#define __CRESTA_OpticalActionInitialization_hh__
#include "G4Headers.hh"
#include "CorePackage.hh"
#include "FluxPackage.hh"

namespace CRESTA { // Main CRESTA Namespace
namespace Construction { // CRESTA Construction Sub Namespace
// ---------------------------------------------------------------------------

/// \class CRESTAActionInitialization
/// \brief Action initialization class for CRESTA run routines.
///
/// Handles Run/RunAction/Stacking/Stepping and the Flux.
/// Associated CRESTAWorld is called automatically in WorldConstruction.
class OpticalActionInitialization : public G4VUserActionInitialization
{
public:

  /// Constructor
  OpticalActionInitialization();
  /// Destructor
  virtual ~OpticalActionInitialization();

  /// Registers User Actions for the master (only Run Action)
  virtual void BuildForMaster() const;

  /// Register User Actions for the workers
  virtual void Build() const;

  /// Loads global target boxes for trajectory checking.
  void BuildTargetBoxes();

private:
  std::vector<G4Box*> fTargetBoxes; ///< List of user defined targets
  std::vector<G4ThreeVector> fTargetBoxPositions; ///< Position of user defined targets in world
  std::vector<G4double> fTargetBoxRadiusCutoff;

};

// ---------------------------------------------------------------------------
} // - namespace Construction
} // - namespace CRESTA
#endif
