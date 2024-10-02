G4ClassificationOfNewTrack OpticalStackingAction::ClassifyNewTrack(const G4Track* track){

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
                    
return G4UserStackingAction::ClassifyNewTrack(track);
}