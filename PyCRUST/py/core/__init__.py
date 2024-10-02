from geant4 import gRunManager, m, cm, mm, s, ms, eV, MeV, G4String, G4ThreeVector, G4RotationMatrix, G4intercoms
from geant4 import G4VUserPrimaryGeneratorAction, G4ParticleTable, G4ParticleGun, G4VSensitiveDetector
from geant4 import s, ms, ns, m, cm, mm, cm2, cm3, g, kg, eV, MeV, gRunManager

def gQuietPhysics():
        
    G4intercoms.ApplyUICommand("/process/verbose       0")
    
    G4intercoms.ApplyUICommand("/process/verbose       0")
    G4intercoms.ApplyUICommand("/process/em/verbose    0")
    G4intercoms.ApplyUICommand("/process/had/verbose   0")
    G4intercoms.ApplyUICommand("/process/eLoss/verbose 0")
    
    G4intercoms.ApplyUICommand("/control/verbose  0")
    G4intercoms.ApplyUICommand("/run/verbose      0")
    G4intercoms.ApplyUICommand("/physics/verbose      0")
    G4intercoms.ApplyUICommand("/event/verbose    0")
    G4intercoms.ApplyUICommand("/hits/verbose     0")
    G4intercoms.ApplyUICommand("/tracking/verbose 0")
    G4intercoms.ApplyUICommand("/stepping/verbose 0")

class datatable:
  def __init__(self, dict):
    self.dt = dict

  def __getitem__(self, arg):
        return self.dt[arg]

  def __getattr__(self, name):
    try:
      return self.__getitem__(name)
    except:
      raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
