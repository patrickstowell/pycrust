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
#include "OpticalRunAction.hh"

namespace CRESTA { // Main CRESTA Namespace
namespace Construction { // CRESTA Construction Sub Namespace
// ---------------------------------------------------------------------------

OpticalRunAction::OpticalRunAction() : G4UserRunAction(), fCurrentRun(0)
{
}

OpticalRunAction::~OpticalRunAction()
{
  delete G4AnalysisManager::Instance();
}

G4Run* OpticalRunAction::GenerateRun()
{
  return new OpticalRun;
}

void OpticalRunAction::BeginOfRunAction(const G4Run* run)
{
  // Logging Info
  std::cout << "**************************************************************" << std::endl;
  std::cout << "ACT: Beginning Run : " << fCurrentRun << std::endl;

  // Do start analysis processing
  Analysis::Get()->BeginOfRunAction(run);
}

void OpticalRunAction::EndOfRunAction(const G4Run* run)
{
  // Do any run processing
  Analysis::Get()->EndOfRunAction(run);

  // Add to the current counters
  fCurrentRun++;
  Analysis::Get()->IncrementSubRun();
  Analysis::Get()->PrintEndOfRunStatement();

  // Check exposure/trigger limits
  Analysis::Get()->CheckAbortState();
}

// ---------------------------------------------------------------------------
} // - namespace Construction
} // - namespace CRESTA
