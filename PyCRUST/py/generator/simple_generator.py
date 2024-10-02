from ..core import *
from geant4 import *

class simple_generator(G4VUserPrimaryGeneratorAction):
    "My Primary Generator Action"

    def __init__(self):
        G4VUserPrimaryGeneratorAction.__init__(self)
        particle_table = G4ParticleTable.GetParticleTable()
        particle = particle_table.FindParticle(G4String("neutron"))      

        offset = G4ThreeVector(0,0,30*cm)
        
        self.particleGun = G4ParticleGun()
        self.particleGun.SetParticleEnergy(14*MeV)
        self.particleGun.SetParticleMomentumDirection(G4ThreeVector(0,0,-1))
        self.particleGun.SetParticleDefinition(particle)
        self.particleGun.SetParticlePosition(offset)
        self.particleGun.SetParticleTime(0)
    
    def GeneratePrimaries(self, event):   
        self.particleGun.GeneratePrimaryVertex(event)


