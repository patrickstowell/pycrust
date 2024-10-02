import geant4 as g4
from .. import core
import numpy as np
import plotly.graph_objects as go
import json
from .. import _PyCRUST as pc

from geant4 import G4VUserDetectorConstruction, gRunManager, G4Transform3D
from geant4 import G4UserSteppingAction, gNistManager, G4Material, G4LogicalVolume, G4PVPlacement, G4ThreeVector, G4RotationMatrix
from geant4 import G4Box, G4Cons, G4Orb, G4Para, G4Sphere, G4Torus, G4Tubs, G4Trd
from geant4 import s, ms, ns, m, cm, mm, cm2, cm3, g, kg, eV, MeV

# G4Box.__str__ = lambda self: json.dumps({"name": str(self.GetName()), 
#                                           "type": "box",
#                                           "x": self.GetXHalfLength(), 
#                                           "y": self.GetYHalfLength(), 
#                                           "z": self.GetZHalfLength()})
# G4Box.__repr__ = G4Box.__str__

# G4Material.__str__ = lambda self: json.dumps({"name": str(self.GetName())})
# G4Material.__repr__ = G4Material.__str__


# G4LogicalVolume.__str__ = lambda self: json.dumps({"name": str(self.GetName()), 
#                                          "material": eval(str(self.GetMaterial())), 
#                                          "solid": eval(str(self.GetSolid()))})
# G4LogicalVolume.__repr__ = G4LogicalVolume.__str__


# G4PVPlacement.__str__ = lambda self: json.dumps({"name": str(self.GetName()), 
#                                          "logical": eval(str(self.GetLogicalVolume()))})
# G4PVPlacement.__repr__ = G4PVPlacement.__str__


def BuildSolid(cfg):
    
    solid_type = cfg["type"].upper()
    if not solid_type.startswith("G4"): 
        solid_type = "G4" + solid_type

    table = cfg.copy()
    for key in cfg:
        table["p" + key] = table[key]

    table["pName"] = cfg["name"]

    t = core.datatable(table)

    if solid_type == "G4BOX":    return G4Box(t.pname, t.px, t.py, t.pz)
    if solid_type == "G4CONS":   return G4Cons(t.pname,t.prmin1,t.prmax1,t.prmin2,t.prmax2,t.pdz,t.psphi,t.pdphi)
    if solid_type == "G4ORB":    return G4Orb(t.pname,t.prmax)
    if solid_type == "G4PARA":   return G4Para(t.pname,t.pdx,t.pdy,t.pdz,t.palpha,t.ptheta,t.pphi)
    if solid_type == "G4SPHERE": return G4Sphere(t.pname, t.prmin, t.prmax, t.psphi, t.pdphi, t.pstheta, t.pdtheta)
    if solid_type == "G4TORUS":  return G4Torus(t.pname, t.prmin, t.prmax, t.prtor, t.psphi, t.pdphi)
    if solid_type == "G4TUBS":   return G4Tubs( t.pname, t.prmin, t.prmax, t.pdz, t.psphi, t.pdphi)
    if solid_type == "G4TRD":    return G4Trd( t.pname, t.pdx1, t.pRMax, t.pDz, t.pSPhi, t.pDPhi )
        
    raise AttributeError(f"Unkown solid type! {table}")

def BuildLogical(cfg):
    if isinstance(cfg["material"], str):
        cfg["material"] = gNistManager.FindOrBuildMaterial(cfg["material"])
        
    if not cfg["material"] or not isinstance(cfg["material"], G4Material):
        print("Warning invalid material")

    log = G4LogicalVolume(
        cfg['solid'], 
        cfg['material'], 
        cfg["name"])

    if "sensitive" in cfg:
        cfg["sensitive"] = cfg["sensitive"]( cfg["name"], cfg )
        log.SetSensitiveDetector(cfg["sensitive"])

    return log
    
def BuildPhysical(in_cfg):
    out_cfg = in_cfg.copy()

    if "position" not in in_cfg:
        in_cfg["position"] = G4ThreeVector()
        
    if isinstance(in_cfg["position"], list):
        out_cfg["position"] = G4ThreeVector(in_cfg["position"][0],
                                            in_cfg["position"][1],
                                            in_cfg["position"][2])
    else:
        out_cfg["position"] =  G4ThreeVector()
        
    out_cfg["rotation"] = G4RotationMatrix()
    if "rotation" in in_cfg and isinstance(in_cfg["rotation"], list):
        out_cfg["rotation"].rotateX(in_cfg["rotation"][0])
        out_cfg["rotation"].rotateY(in_cfg["rotation"][1])
        out_cfg["rotation"].rotateZ(in_cfg["rotation"][2])

    if "rotation" in in_cfg and isinstance(in_cfg["rotation"], G4ThreeVector):
        out_cfg["rotation"].rotateX(in_cfg["rotation"].x)
        out_cfg["rotation"].rotateY(in_cfg["rotation"].y)
        out_cfg["rotation"].rotateZ(in_cfg["rotation"].z)
    
    if "mother" in in_cfg:

        if isinstance(in_cfg["mother"], dict):
            out_cfg["mother"] = in_cfg["mother"]["logical"]
        elif isinstance(in_cfg["mother"], G4VUserDetectorConstruction):
            out_cfg["mother"] = in_cfg["mother"].root["logical"]
        else:
            out_cfg["mother"] = in_cfg["mother"]
        
    else:
        out_cfg["mother"] = None

    for key in out_cfg:
        in_cfg[key] = out_cfg[key]

    return G4PVPlacement(
            out_cfg["rotation"],
            out_cfg["position"],
            out_cfg["logical"],
            out_cfg["name"],
            out_cfg["mother"],  
            False, 
            0)
    
def PCObject(**kwargs):
    cfg = kwargs.copy()
    if "name" not in cfg: cfg["name"] = "OBJECT"
    
    if "solid" not in cfg:
        cfg["solid"]    = BuildSolid(cfg)
        
    cfg["logical"]  = BuildLogical(cfg)
    cfg["physical"] = BuildPhysical(cfg)
    return cfg

def PCBox(x, y, z, **kwargs):
    kwargs["type"] = "box"
    return PCObject(x=x,y=y,z=z,**kwargs)

def PCTubs(rmin=0., rmax=None, sphi=0.0, dphi=2*g4.pi, dz=None, **kwargs):
    kwargs["type"] = "tubs"
    return PCObject(rmin=rmin, rmax=rmax, sphi=sphi, dphi=dphi, dz=dz, **kwargs)


# Add this to action if you want a plot of all step positions
class VisualTracker(G4UserSteppingAction):

    def Clear(self):
        self.trajs = {}
        self.pdgs  = {}
        self.edep  = {}
        
    def UserSteppingAction(self, step):     
        eid = gRunManager.GetCurrentEvent().GetEventID()
        tid = step.GetTrack().GetTrackID()

        if eid not in self.trajs:
            self.trajs[eid] = {}
            self.pdgs[eid] = {}
            self.edep[eid] = {}

        if tid not in self.trajs[eid]:
            self.trajs[eid][tid] = [
                step.GetPreStepPoint().GetPosition(),
            ]
            self.pdgs[eid][tid] = step.GetTrack().GetParticleDefinition().GetPDGEncoding()
            self.edep[eid][tid] = [0.0]
            
        self.trajs[eid][tid].append(
            step.GetPostStepPoint().GetPosition()
        )

        self.edep[eid][tid].append( step.GetTotalEnergyDeposit() )
        



class PCWorld(G4VUserDetectorConstruction):
    def __init__(self, **kwargs):
        G4VUserDetectorConstruction.__init__(self)
        kwargs["name"] = "world"
        kwargs["type"] = "box"
        self.root = PCObject(**kwargs)
        self._visual = None

    def Construct(self):
        return self.root["physical"]
        
    def visual(self):
        if not self._visual:
            self._visual = VisualTracker()
        return self._visual
  
    def build_solid(self, solid, translation, opacity, name ):
    
        x=pc.geometry.GetVertices(solid, 0)
        y=pc.geometry.GetVertices(solid, 1)
        z=pc.geometry.GetVertices(solid, 2)
        solid_points = []
        for xx, yy, zz in zip(x,y,z):
            p = G4ThreeVector(xx,yy,zz)
            p = translation.getRotation()*p + translation.getTranslation()
            solid_points.append( [p.x, p.y, p.z] )

        all_points = []
        ni = pc.geometry.GetNFacets(solid)
        for j in range(len(ni)):
            f = pc.geometry.GetFacets(solid, j)
            ijk = f[0:3]
            
            ii = solid_points[ijk[0]-1]
            jj = solid_points[ijk[1]-1]
            kk = solid_points[ijk[2]-1]
            all_points.append( ii )
            all_points.append( jj )
            all_points.append( kk )
            
        solid_points = all_points
            
        
        
    
        # mesh = go.Mesh3d(
        #             # Set the coordinates
        #             x=[face[0] for face in solid_points],
        #             y=[face[1] for face in solid_points],
        #             z=[face[2] for face in solid_points],
        #             # Optional styling
        #             opacity=opacity,
        #             alphahull=0.01,
        #             showlegend=True,
        #             name=str(name)
        #         )

        mesh = go.Scatter3d(
                    # Set the coordinates
                    x=[face[0] for face in solid_points],
                    y=[face[1] for face in solid_points],
                    z=[face[2] for face in solid_points],
                    # Optional styling
                    showlegend=True,
                    name=str(name)
                )
        
        return mesh


    def plot(self, resolution=1000, opacity=0.4, draw_world = False, draw_tracks = False ):
                    
        global_data = []
            
        def traverse(physical, translation=None, name=""):
        
            if not physical: return
            solid = physical.GetLogicalVolume().GetSolid()
            
            if (str(solid.GetName()) == "world"):
                if (draw_world): name += ":" + str(solid.GetName())
                translation = G4Transform3D()
            else:
                name += ":" + str(solid.GetName())
                translation *= G4Transform3D(physical.GetRotation(),  physical.GetTranslation())
                
            logical = physical.GetLogicalVolume()
            if (str(solid.GetName()) != "world" or draw_world):
                global_data.append(self.build_solid(solid, translation, opacity, name))
        
            for i in range(logical.GetNoDaughters()):
                traverse( logical.GetDaughter(i), translation, name )
    

        x = self.root['solid'].GetXHalfLength()
        y = self.root['solid'].GetYHalfLength()
        z = self.root['solid'].GetZHalfLength()
        traverse(self.root['physical'])
        fig = go.Figure(data=global_data)
        fig.update_layout( autosize=False, width=800, height=800,        
            scene=dict(
                xaxis=dict(visible=False, range=[-x,x]),
                yaxis=dict(visible=False, range=[-y,y]),
                zaxis=dict(visible=False, range=[-z,z]),
                bgcolor='black'
            ),
            updatemenus=[
                {
                    'direction': 'down',
                    'pad': {'r': 10, 't': 10},
                    'showactive': True,
                    'type': 'buttons',
                    'x': 0.1,
                    'xanchor': 'left',
                    'y': 1.1,
                    'yanchor': 'top'
                }
            ]
        )
        
        if (draw_tracks):
            self.add_tracks(fig)
        
        return fig

    def add_tracks(self, fig):
        
        import matplotlib.pyplot as plt
        import plotly.graph_objects as go
        step = self._visual
        colormap = {
            2212 : "red",
            2112 : "yellow",
            -22: "white",
            22 : "cyan",
            11 : "yellow",
            -11 : "yellow"
        }
        
        data = []
        for ek in step.trajs:
            e = step.trajs[ek]
            
            for tk in e:
                t = e[tk]
                p = step.pdgs[ek][tk]
                edep = step.edep[ek][tk]
        
                while len(data) > 500: 
                    i = int(np.random.uniform(0.0,1.0)*(len(data)-1)/2)*2
                    del data[i+1]
                    del data[i]
                    break
        
                c = 'white'
                if p in colormap: c = colormap[p]
                    
                sc = go.Scatter3d(x=[v.x for v in t],
                                  y=[v.y for v in t],
                                  z=[v.z for v in t],
                                  mode='lines',
                                  hoverinfo='skip',
                                  uid=ek,
                                  name=f"pdg:{p}",
                                  showlegend=False,
                                  line=dict(color=c))
                data.append(sc)
        
                sc = go.Scatter3d(x=[v.x for v in t],
                                  y=[v.y for v in t],
                                  z=[v.z for v in t],
                                  marker=dict(color=c, size=[50*v for v in edep]),
                                  hoverinfo='skip',
                                  uid=ek,
                                  mode='markers',
                                  showlegend=False)        
                data.append(sc)
                
        fig.add_traces(data=data)

   