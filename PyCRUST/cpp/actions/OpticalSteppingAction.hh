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
#ifndef __CRESTA_OpticalSteppingAction_HH__
#define __CRESTA_OpticalSteppingAction_HH__
#include "G4Headers.hh"
#include "CorePackage.hh"
#include "FluxPackage.hh"

namespace CRESTA { // Main CRESTA Namespace
namespace Construction { // CRESTA Construction Sub Namespace
// ---------------------------------------------------------------------------

/// \class OpticalSteppingAction
/// \brief Stepping Dummy Class (copies default geant4)
///
/// Handles Run/RunAction/Stacking/Stepping and the Flux.
/// Associated CRESTAWorld is called automatically in WorldConstruction.
class OpticalSteppingAction : public G4UserSteppingAction
{
  public:
    OpticalSteppingAction();
    virtual ~OpticalSteppingAction();

    // method from the base class
    virtual void UserSteppingAction(const G4Step*);
};

// ---------------------------------------------------------------------------
} // - namespace CRESTA
} // - namespace CRESTA
#endif
