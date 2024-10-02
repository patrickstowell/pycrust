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
#ifndef __CRESTA_OpticalRunAction_HH__
#define __CRESTA_OpticalRunAction_HH__
#include "G4Headers.hh"
#include "CorePackage.hh"
#include "FluxPackage.hh"
#include "OpticalRun.hh"

namespace CRESTA { // Main CRESTA Namespace
namespace Construction { // CRESTA Construction Sub Namespace
// ---------------------------------------------------------------------------

/// \class OpticalRunAction
/// \brief  User's OpticalRunAction class.
/// this class implements all the user actions to be executed at each run.
class OpticalRunAction : public G4UserRunAction
{
public:

  /// constructor
  OpticalRunAction();
  /// destructor
  virtual ~OpticalRunAction();

  /// Create a new run
  virtual G4Run* GenerateRun();

  /// Called at the beginning of each run
  virtual void BeginOfRunAction(const G4Run*);
  /// Called at the end of each run
  virtual void   EndOfRunAction(const G4Run*);

protected:
  int fCurrentRun; ///< Index of current run
};

// ---------------------------------------------------------------------------
} // - namespace CRESTA
} // - namespace CRESTA
#endif
