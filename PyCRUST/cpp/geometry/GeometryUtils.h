#pragma once
#include "G4TransportationManager.hh"
#include "G4VPhysicalVolume.hh"
#include "G4LogicalVolume.hh"
#include "G4Material.hh"
#include "G4ScoringManager.hh"

G4double GetDensityAtPosition(float x, float y, float z){
    G4Navigator* nav; // =  G4TransportationManager::GetTransportationManager()->GetNavigatorForTracking();

    G4VPhysicalVolume* phys = nav->LocateGlobalPointAndSetup(G4ThreeVector(x,y,z));
    if (!phys) return 0;

    G4LogicalVolume* log = phys->GetLogicalVolume();
    if (!log) return 0;

    G4Material* mat = log->GetMaterial();
    if (!mat) return 0;

    return mat->GetDensity();
}

void InitializeScoring(){
     G4ScoringManager* scoringManager = G4ScoringManager::GetScoringManager();
}
