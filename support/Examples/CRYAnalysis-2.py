#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os

import cppyy.ll
cppyy.ll.set_signals_as_exception(True)

import pandas as pd
import matplotlib.pyplot as plt

import g4ppyy as g4
from g4ppyy import new, G4ThreeVector
from g4ppyy.SI import mm, cm, m, eV, MeV, GeV, twopi, deg

import random
gRunManager = g4.G4RunManager()

        


# In[2]:


class neutron_tracker(g4.G4VSensitiveDetector):
    def Reset(self):
        self.neutron_event = {
            "eid": [],
            "edep": [],
            "x": [],
            "y": [],
            "z": []        
        }
                
    def ProcessHits(self, aStep, ROhist):
        
        pdg = (aStep.GetTrack().GetParticleDefinition().GetPDGEncoding())           
        if not (pdg == 22): return 0

        eid = int(gRunManager.GetCurrentEvent().GetEventID())

        self.neutron_event["eid"].append( eid )
        
        pos = aStep.GetPreStepPoint().GetPosition() 
        dirs = aStep.GetTrack().GetMomentumDirection() 
        ek = aStep.GetPreStepPoint().GetTotalEnergy() 

        self.neutron_event["edep"].append(aStep.GetTotalEnergyDeposit())
        self.neutron_event["x"].append(pos.x())
        self.neutron_event["y"].append(pos.y())
        self.neutron_event["z"].append(pos.z())
        
        aStep.GetTrack().SetTrackStatus(g4.G4TrackStatus.fStopAndKill)

        return 1

    def StartOfRunAction(self):
        self.Reset()

    def EndOfRunAction(self):
        self.df = pd.DataFrame(data=self.neutron_event)

    def VisualizationAction(self):
        
        plt.scatter(self.df.x, self.df.y, c=self.df.edep)
        plt.title(str(self.GetName()) + " : XY Edep")
        plt.xlabel("x [mm]")
        plt.ylabel("z [mm]")
        plt.show()
        
        plt.scatter(self.df.x, self.df.z, c=self.df.edep)
        plt.title(str(self.GetName()) + " : XZ Edep")
        plt.xlabel("x [mm]")
        plt.xlabel("z [mm]")
        plt.show()



# In[3]:


import numpy as np
nm = 1.267

def nmtoev(x):
    h=4.1357e-15 #eVs 
    c=299792458  #ms-1
    x = np.array(x)*1e-9
    val = (h*c/x)*mm #in units of m
    return list(val) #default units of mm

# list.nmtoev = nmtoev
# np.array.nmtoev = nmtoev

class custom_world(g4.cppyy.gbl.G4VUserDetectorConstruction):         
    def BuildMaterials(self):
        # Material definitions
        self.water_mat = g4.gNistManager.FindOrBuildMaterial("G4_WATER")        
        self.air_mat = g4.gNistManager.FindOrBuildMaterial("G4_AIR")
        
        self.loaded_water = g4.builder.build_material("LoadedWater",
                                                      density=1*g4.g/g4.cm3,
                                                      materials=["G4_WATER","G4_GADOLINIUM_OXYSULFIDE"],
                                                      fractions=[0.998,0.002],
                                                      RINDEX_X=nmtoev([100,500,600]),
                                                      RINDEX_Y=[1.2,1.2,1.2],
                                                      ABSLENGTH_X=nmtoev([100,500,600]),
                                                      ABSLENGTH_Y=[2.0*m, 2.0*m, 2.0*m],
                                                      RAYLEIGH_X=nmtoev([100,500,600]),
                                                      RAYLEIGH_Y=[10.0*m,10.0*m,10.0*m])
        
        self.loaded_water.GetMaterialPropertiesTable().DumpTable()
                                                      

    def BuildWorld(self):
        # Mother Box
        self.world = g4.builder.build_component("world", solid="box", 
                                                x=4*m, y=4*m, z=2*m, 
                                                material=self.air_mat)

        # World Geometries        
        self.hdpe_outer   = g4.builder.build_component("shell", 
                                                       solid="tubs", 
                                                       rot=[90*deg, 0.0, 0.0], 
                                                       rmax=11*cm, z=0.6*m/2, 
                                                       mother=self.world, 
                                                       material="G4_POLYETHYLENE", 
                                                       color=[0.0,0.0,1.0,0.8], 
                                                       drawstyle="solid")
        
        self.water_inner  = g4.builder.build_component("water", solid="tubs", 
                                                       rmax=9*cm, z=0.6*m/2, 
                                                       mother=self.hdpe_outer, 
                                                       material=self.loaded_water, 
                                                       color=[0.5,0.5,1.0,0.1], 
                                                       drawstyle="solid")

        self.ptdet = neutron_tracker("ptdet")
        self.ptdet.Reset()

        self.water_inner .GetLogicalVolume().SetSensitiveDetector(self.ptdet)
        pos_scale = +1
        self.hdpe_endcap1 = g4.builder.build_component("cap1", solid="tubs", rmax=9*cm, 
                                                       z=1*cm, 
                                                       mother=self.water_inner, 
                                                       material="G4_POLYETHYLENE", 
                                                       color=[1.0,0.2,1.0,0.8], 
                                                       drawstyle="solid", 
                                                       pos=[0.0, 0.0, pos_scale*(+0.6*m/2 - 1*cm)])
        
        self.hdpe_endcap1_hollow = g4.builder.build_component("cap1_hollow", solid="tubs", rmax=2.5*cm, 
                                                       z=1*cm, 
                                                       mother=self.hdpe_endcap1, 
                                                       material="G4_AIR", 
                                                       color=[1.0,0.2,1.0,0.8], 
                                                       drawstyle="solid", 
                                                       pos=[0.0, 0.0, 0.0])
        
        self.hdpe_endcap1_frontring = g4.builder.build_component("cap1_frontring", solid="tubs", rmax=5*cm, 
                                                       z=1*cm,  
                                                       mother=self.water_inner, 
                                                       material="G4_POLYETHYLENE", 
                                                       color=[1.0,0.2,1.0,0.8], 
                                                       drawstyle="solid", 
                                                       pos=[0.0, 0.0, pos_scale*(+0.6*m/2-3*cm)])

        self.hdpe_endcap1_fronthollow = g4.builder.build_component("cap1_fronthollow", solid="tubs", rmax=2.5*cm, 
                                                       z=1*cm, 
                                                       mother=self.hdpe_endcap1_frontring, 
                                                       material="G4_AIR", 
                                                       color=[1.0,0.2,1.0,0.8], 
                                                       drawstyle="solid", 
                                                       pos=[0.0, 0.0, 0.0])
        
        self.hdpe_endcap1_outerring = g4.builder.build_component("cap1_outerring", solid="tubs", rmax=5*cm, 
                                                       z=1*cm, rot=[90*deg, 0.0, 0.0], 
                                                       mother=self.world, 
                                                       material="G4_POLYETHYLENE", 
                                                       color=[1.0,0.2,1.0,0.8], 
                                                       drawstyle="solid", 
                                                       pos=[0.0,pos_scale*(+0.6*m/2+1*cm),0.0])
        
        self.hdpe_endcap1_outerhollow = g4.builder.build_component("cap1_outerhollow", solid="tubs", rmax=2.5*cm, 
                                                       z=1*cm, 
                                                       mother=self.hdpe_endcap1_outerring, 
                                                       material="G4_AIR", 
                                                       color=[1.0,0.2,1.0,0.8], 
                                                       drawstyle="solid", 
                                                       pos=[0.0, 0.0, 0.0])

        pos_scale = -1
        self.hdpe_endcap2 = g4.builder.build_component("cap2", solid="tubs", rmax=9*cm, 
                                                       z=1*cm, 
                                                       mother=self.water_inner, 
                                                       material="G4_POLYETHYLENE", 
                                                       color=[1.0,0.2,1.0,0.8], 
                                                       drawstyle="solid", 
                                                       pos=[0.0, 0.0, pos_scale*(+0.6*m/2 - 1*cm)])
        
        self.hdpe_endcap2_hollow = g4.builder.build_component("cap2_hollow", solid="tubs", rmax=2.5*cm, 
                                                       z=1*cm, 
                                                       mother=self.hdpe_endcap2, 
                                                       material="G4_AIR", 
                                                       color=[1.0,0.2,1.0,0.8], 
                                                       drawstyle="solid", 
                                                       pos=[0.0, 0.0, 0.0])
        
        self.hdpe_endcap2_frontring = g4.builder.build_component("cap2_frontring", solid="tubs", rmax=5*cm, 
                                                       z=1*cm, 
                                                       mother=self.water_inner, 
                                                       material="G4_POLYETHYLENE", 
                                                       color=[1.0,0.2,1.0,0.8], 
                                                       drawstyle="solid", 
                                                       pos=[0.0, 0.0, pos_scale*(+0.6*m/2-3*cm)])

        self.hdpe_endcap2_fronthollow = g4.builder.build_component("cap2_fronthollow", solid="tubs", rmax=2.5*cm, 
                                                       z=1*cm, 
                                                       mother=self.hdpe_endcap2_frontring, 
                                                       material="G4_AIR", 
                                                       color=[1.0,0.2,1.0,0.8], 
                                                       drawstyle="solid", 
                                                       pos=[0.0, 0.0, 0.0])
        
        self.hdpe_endcap2_outerring = g4.builder.build_component("cap2_outerring", solid="tubs", rmax=5*cm, 
                                                       z=1*cm, rot=[90*deg, 0.0, 0.0], 
                                                       mother=self.world, 
                                                       material="G4_POLYETHYLENE", 
                                                       color=[1.0,0.2,1.0,0.8], 
                                                       drawstyle="solid", 
                                                       pos=[0.0,pos_scale*(+0.6*m/2+1*cm),0.0])
        
        self.hdpe_endcap2_outerhollow = g4.builder.build_component("cap2_outerhollow", solid="tubs", rmax=2.5*cm, 
                                                       z=1*cm, 
                                                       mother=self.hdpe_endcap2_outerring, 
                                                       material="G4_AIR", 
                                                       color=[1.0,0.2,1.0,0.8], 
                                                       drawstyle="solid", 
                                                       pos=[0.0, 0.0, 0.0])

        # Build the PMTs
        pmt_con = new(g4.G4Cons("PMTGlass1",0, 2.5*cm, 0, 130*mm/2, 46*mm/2, 0, twopi))
        pmt_front = new(g4.G4Tubs("PMTGlass2", 0, 130*mm/2, 32*mm/2, 0, twopi))
        pmt_base = new(g4.G4Tubs("PMTGlass3", 0, 2.5*cm, 50*mm/2, 0, twopi))
        pmt_union = new(g4.G4UnionSolid("PMTGlass4", pmt_con, pmt_front, 0, G4ThreeVector(0,0,+46*mm/2+32*mm/2-0*mm)))
        pmt_union2 = new(g4.G4UnionSolid("PMTGlass5", pmt_union, pmt_base, 0, G4ThreeVector(0,0,-46*mm/2-50*mm/2+0*mm)))

        vac_con = new(g4.G4Cons("PMTVac1",0, 2.5*cm-1*mm, 0, 130*mm/2-1*mm, 46*mm/2-1*mm, 0, twopi))
        vac_front = new(g4.G4Tubs("PMTVac2", 0, 130*mm/2-1*mm, 32*mm/2-1*mm, 0, twopi))
        vac_base = new(g4.G4Tubs("PMTVac3", 0, 2.5*cm-1*mm, 50*mm/2-1*mm, 0, twopi))
        vac_union = new(g4.G4UnionSolid("PMTVac4", vac_con, vac_front, 0, G4ThreeVector(0,0,+46*mm/2+32*mm/2-0*mm)))
        vac_union2 = new(g4.G4UnionSolid("PMTVac5", vac_union, vac_base, 0, G4ThreeVector(0,0,-46*mm/2-50*mm/2+0*mm)))
        
        self.pmt1 = g4.builder.build_component("pmt1", solid=pmt_union2, 
                                               mother=self.water_inner, 
                                               material="G4_GLASS_PLATE", 
                                               color=[0.0,1.0,0.2,1.0], 
                                               drawstyle="solid", 
                                               pos=[0.0, 0.0, -0.6*m/2+50*mm+46*mm/2])

        self.vac1 = g4.builder.build_component("pmt1", solid=vac_union2, 
                                               mother=self.pmt1, 
                                               material="G4_AIR", 
                                               color=[0.0,0.0,0.2,0.5], 
                                               drawstyle="solid", 
                                               pos=[0.0, 0.0, 0.0])

        self.pcathode1 = g4.builder.build_component("pcathode1", solid="tubs",
                                               rmax=128*mm/2, z=0.01*mm,
                                               mother=self.pmt1, 
                                               material="G4_GLASS_PLATE", 
                                               color=[1.0,0.0,0.0,1.0], 
                                               drawstyle="solid", 
                                               pos=[0.0, 0.0, (46/2+32)*mm-0.01*mm/2])

        self.pmt2 = g4.builder.build_component("pmt2", solid=pmt_union2, 
                                               mother=self.water_inner, 
                                               rot=[180*g4.deg,0.0,0.0],
                                               material="G4_GLASS_PLATE", 
                                               color=[0.0,1.0,0.2,1.0], 
                                               drawstyle="solid", 
                                               pos=[0.0, 0.0, +0.6*m/2-50*mm-46*mm/2])

        self.vac2 = g4.builder.build_component("pmt1", solid=vac_union2, 
                                               mother=self.pmt2, 
                                               material="G4_AIR", 
                                               color=[0.0,0.0,0.2,0.5], 
                                               drawstyle="solid", 
                                               pos=[0.0, 0.0, 0.0])

        self.pcathode2 = g4.builder.build_component("pcathode2", solid="tubs",
                                               rmax=128*mm/2, z=0.01*mm,
                                               mother=self.pmt2, 
                                               material="G4_GLASS_PLATE", 
                                               color=[1.0,0.0,0.0,1.0], 
                                               drawstyle="solid", 
                                               pos=[0.0, 0.0, (46/2+32)*mm-0.01*mm/2])
        
        
    def BuildDetectors(self):
        pass
        # self.hdpe_det = neutron_tracker("hdpe_det")        
        # self.hdpe_outer.GetLogicalVolume().SetSensitiveDetector(self.hdpe_det)
        # g4.run.register_detector_hooks(detector.hdpe_det)

    def Construct(self):
        self.BuildMaterials()
        self.BuildWorld()
        self.BuildDetectors()
        
        # Return the mother
        return self.world # top mother volume

w = custom_world()
# w.Construct()



# In[4]:


class custom_generator(g4.G4VUserPrimaryGeneratorAction):
    "Flat Energy Spectrum Upward Neutron Generator"
    def __init__(self):
        super().__init__()
        self.particle = g4.G4Neutron.Definition()
        self.particleGun = g4.G4ParticleGun()
        self.particleGun.SetParticleDefinition(self.particle)
        self.particleGun.SetParticleMomentumDirection(g4.G4ThreeVector(0, 0, -1))
        self.particleGun.SetParticlePosition(g4.G4ThreeVector(0.0,0.0,+20.0*cm))
        self.particleGun.SetNumberOfParticles(1)  
        self.particleGun.SetParticleTime(0)

    def GeneratePrimaries(self, anEvent):
        print("GEN MUON")
        energy = random.random() * 200 * MeV
        self.particleGun.SetParticleEnergy(energy)  
        self.particleGun.GeneratePrimaryVertex(anEvent)


# In[ ]:


physics = g4.QGSP_BERT()
# op = g4.G4OpticalPhysics()
# physics.RegisterPhysics(op)
gRunManager.SetUserInitialization(physics)

# Add a World
detector = g4.new(custom_world())
gRunManager.SetUserInitialization(detector)

# Add a Generator
gen = g4.new(g4.PrimaryGeneratorAction("", 0.25*m))
g4.mc.CRY.input("returnNeutrons 1")
g4.mc.CRY.input("returnProtons 1")
g4.mc.CRY.input("returnGammas 1")
g4.mc.CRY.input("returnPions 1")
g4.mc.CRY.input("returnKaons 1")
g4.mc.CRY.input("date 7-1-2012")
g4.mc.CRY.input("latitude 90.0")
g4.mc.CRY.input("altitude 0")
g4.mc.CRY.input("subboxLength 1")
g4.mc.CRY.update()

# gen = g4.new(custom_generator())
gRunManager.SetUserAction(gen)

# Add standard GEANT4 Actions
g4.run.add_default_actions(gRunManager)

# Setup vis to check geometry (optioonal)
g4.run.create_visualization(gRunManager)

g4.mc.vis.scene.add.trajectories("rich")

traj_mc = g4.mc.vis.modeling.trajectories
traj_mc.create.drawByParticleID()
traj_mc.drawByParticleID_0.default.setDrawStepPts(True)
traj_mc.drawByParticleID_0.default.setStepPtsSize(1)
traj_mc.drawByParticleID_0.set("e+","white")
traj_mc.drawByParticleID_0.set("e-","white")
traj_mc.drawByParticleID_0.set("gamma","yellow")
traj_mc.drawByParticleID_0.set("neutron","magenta")
traj_mc.drawByParticleID_0.set("proton","blue")
traj_mc.drawByParticleID_0.set("pi+","red")
traj_mc.drawByParticleID_0.set("pi-","red")
traj_mc.drawByParticleID_0.set("pi0","grey")
traj_mc.drawByParticleID_0.set("mu-","red")
traj_mc.drawByParticleID_0.set("mu+","red")
traj_mc.drawByParticleID_0.set("opticalphoton","white")
traj_mc.drawByParticleID_0.set("optical_photon","white")



# Generate some events

g4.run.handle_beam(gRunManager, 100)


# In[ ]:


# Draw the vis plot (optional)
g4.run.draw_visualization(gRunManager)


# g4.run.handle_beam(gRunManager, 10000)

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




