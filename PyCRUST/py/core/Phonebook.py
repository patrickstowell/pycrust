import geant4 as g4
from beartype import beartype
import PyCRUST as pc
import numpy as np
import plotly.graph_objects as go

twopi = 2*3.14159 


class helpers:

    @classmethod
    def material_from_elements(self, 
                               name : str,
                               density : float,
                               elements : list[str, g4.G4Element],
                               fractions : list[int]):
        
        if (g4.gNistManager.FindOrBuildMaterial(name)): 
            print("Found", name)
            return g4.gNistManager.FindOrBuildMaterial(name)
            
        mat = g4.G4Material(name, density, len(elements))
        print("NEW MATERIAL")
        
        for e,f in zip(elements, fractions):
            if (isinstance(e, str)):
                
                e = g4.gNistManager.FindOrBuildElement(e)
            if (e):
                mat.AddElement(e, f)

        return mat
    
    
    @classmethod
    def material_from_materials(self, 
                               name : str,
                               density : float,
                               materials : list[str, g4.G4Material],
                               fractions : list[int]):
        if (g4.gNistManager.FindOrBuildMaterial(name)): 
            return g4.gNistManager.FindOrBuildMaterial(name)
            
        mat = g4.G4Material(name, density, len(materials))

        for i, (m, f) in enumerate(zip(materials, fractions)):
            if (isinstance(m, str)):
                m = g4.gNistManager.FindOrBuildMaterial(m)
            if (m):
                mat.AddMaterial(m, f)
            else:
                raise Exception(f"Failed to load material {i}")

        return mat

    @classmethod
    def material_from_store(self, name : str):
        print("Finding",name)
        if g4.gNistManager.FindOrBuildMaterial(name):
            return g4.gNistManager.FindOrBuildMaterial(name)
        else: 
            return None

    @classmethod
    def set_material_properties(self, material, data : dict):  
        properties = {}
        data_found = False
        for p in data:
            if p == p.upper() and data[p]:
                properties[p] = data[p]
                data_found = True

        for key in properties:
            if "_X" in key:
                xv = properties[key]
                yv = properties[key.replace("_X","_Y")]

                vals = sorted(zip(xv, yv))
                xv, yv = zip(*vals)
                properties[key] = xv
                properties[key.replace("_X","_Y")] = yv

        if data_found:
          pc.geometry.SetMaterialProperties(material, properties)
        

material_store = {}

def build_material(name: str, 
             density: float = None, 
             elements: list[str, g4.G4Element] = None, 
             materials: list[str, g4.G4Material] = None, 
             fractions : list[float] = None,
             SCINTILLATIONTIMECONSTANT1 : float = None,
             SCINTILLATIONTIMECONSTANT2 : float = None,
             SCINTILLATIONYIELD : float = None,
             RESOLUTIONSCALE : float = None,
             ABSLENGTH_X : list[float] = None,
             ABSLENGTH_Y : list[float] = None,
             RINDEX_X : list[float] = None,
             RINDEX_Y : list[float] = None,
             SCINTILLATIONCOMPONENT1_X : list[float] = None,
             SCINTILLATIONCOMPONENT1_Y : list[float] = None,
             SCINTILLATIONCOMPONENT2_X : list[float] = None,
             SCINTILLATIONCOMPONENT2_Y : list[float] = None,
             WLSTIMECONSTANT : float = None,
             WLSCOMPONENT_X : list[float] = None, 
             WLSCOMPONENT_Y : list[float] = None,
             RAYLEIGH_X : list[float] = None, 
             RAYLEIGH_Y : list[float] = None,
             MIEHG_X : list[float] = None, 
             MIEHG_Y : list[float] = None,
             MIEHG_FORWARD_RATIO : float = None,
             MIEHG_FORWARD : float = None,
             MIEHG_BACKWARD : float = None,
             WLSABSLENGTH_X: list[float] = None,
             WLSABSLENGTH_Y: list[float] = None):

    material = None
    if elements and not materials:
        material = helpers.material_from_elements(name, density, elements, fractions) 
    elif not elements and materials:
        material = helpers.material_from_materials(name, density, materials, fractions)
    else:
        if name in material_store and material_store[name]: material = material_store[name]
        else: material = helpers.material_from_store(name)

    if not material: return None

    material_store[name] = material
    helpers.set_material_properties(material, locals())
    return material

@beartype
def position(x : (float, int) = 0.0,
             y : (float, int) = 0.0,
             z : (float, int) = 0.0):
    return [float(x),float(y),float(z)]

@beartype
def rotation(xy : (float, int) = 0.0,
             xz : (float, int) = 0.0,
             yz : (float, int) = 0.0):
    return [float(xy),float(xz),float(yz)]


def build_box(name, x, y, z):
    return g4.G4Box(name, x/2, y/2, z/2)

def build_sphere(name, rmin=0, rmax=1, phimin=0, phimax=twopi, thetamin=0, thetamax=twopi):
    return g4.G4Sphere(name, rmin, rmax, phimin, phimax, thetamin, thetamax)

def build_tubs(name, rmin=0, rmax=1, zmax=1, phimin=0, phimax=twopi):
    return g4.G4Tubs(name, rmin, rmax, zmax/2, phimin, phimax)

gSolidList = {}
def build_solid(name  : str,
                solid : str,
                x: float = 1,
                y: float = 1,
                z: float = 1,
                rmin : float = 0, 
                rmax : float = 1, 
                phimin : float = 0, 
                phimax : float = twopi, 
                thetamin : float = 0, 
                thetamax : float = twopi):
    """
        box(name, x, y, z)
        sphere(name, rmin, rmax, phimin, phimax, thetamin, thetamax)
        tubs(name, rmin, rmax, zmax/2, phimin, phimax)
    """

    print(locals())
    if solid == "box": obj= build_box(name, x, y, z)
    if solid == "sphere": obj= build_sphere(name, rmin, rmax, phimin, phimax, thetamin, thetamax)
    if solid == "tubs": obj= build_tubs(name, rmin, rmax, z/2, phimin, phimax)

    gSolidList[name] = obj
    return obj
    
def vis(detector, col, visible=True,drawstyle="solid"):
    
    if isinstance(detector, g4.G4VPhysicalVolume):
        detector = detector.GetLogicalVolume()
        
    detector.SetVisAttributes(g4.G4VisAttributes())
    detector.GetVisAttributes().SetVisibility(visible)
    if drawstyle == "solid":
        detector.GetVisAttributes().SetForceSolid()
    if len(col) <= 3:
        col.append(1.0)
    detector.GetVisAttributes().SetColor(g4.G4Color(col[0],col[1],col[2], col[3]))


def build_logical(name : str,
          solid : (str, g4.G4VSolid) = None,
          material: (str, g4.G4Material) = None,
          x: float = 1,
          y: float = 1,
          z: float = 1,
          rmin : float = 0, 
          rmax : float = 1, 
          phimin : float = 0, 
          phimax : float = twopi, 
          thetamin : float = 0, 
          thetamax : float = twopi,
          color: list[float,int] = [1.0,0.0,0.0,1.0],
          visible: bool = True,
          drawstyle: str = "solid"):

    if isinstance(solid, str):
        solid = build_solid(name, solid, x, y, z, rmin, rmax, phimin, phimax, thetamin, thetamax)

    if isinstance(material, str):
        material = build_material(material)

    log = g4.G4LogicalVolume(solid, material, name)
    vis(log, color, visible, drawstyle)
    
    return log

def build_component(name : str,
              solid : (str, g4.G4VSolid) = None,
              material: (str, g4.G4Material) = None,
              logical: (str, g4.G4LogicalVolume) = None,
              mother: (str, g4.G4LogicalVolume) = None,
              pos: list[float] = position(),
              rot: list[float] = rotation(),
              x: float = 1,
              y: float = 1,
              z: float = 1,
              rmin : float = 0, 
              rmax : float = 1, 
              phimin : float = 0, 
              phimax : float = twopi, 
              thetamin : float = 0, 
              thetamax : float = twopi,
              color: list[float,int] = [1.0,0.0,0.0,1.0],
              visible: bool = True,
              drawstyle: str = "solid"):
    """
    Examples:
    component('block', solid='box', x=5, y=5, z=5, material="G4_AIR")

    component('block', solid=box_solid_obj, material="G4_AIR")

    component('block', logical=box, pos=[0.0,5.0,0.0], mother=world)
    """

    if solid and material and logical:
        raise Exception("Define solid/material or logical, not both")

    if not logical:
        logical = build_logical(name, solid, material, 
                                x, y, z, rmin, rmax, phimin, 
                                phimax, thetamin, thetamax, color, visible, drawstyle)
        
    rotation_matrix = g4.G4RotationMatrix()
    if rot[0] != 0.0 or rot[1] != 0.0 or rot[2] != 0.0: 
        rotation_matrix.rotateX(rot[0])
        rotation_matrix.rotateY(rot[1])
        rotation_matrix.rotateZ(rot[2])

    local_pos = g4.G4ThreeVector(pos[0], pos[1], pos[2])
    print("POS", local_pos)
    
    if isinstance(mother, g4.G4PVPlacement):
        mother = mother.GetLogicalVolume()

    if not mother:
        rotation_matrix = None #g4.G4RotationMatrix()

    print("FINAL POS", local_pos.x, local_pos.y)
    return g4.G4PVPlacement(
            None,
            local_pos,
            logical,
            name,
            mother,  
            False, 
            0)


class World(g4.G4VUserDetectorConstruction):
    def __init__(self, world_obj):
        g4.G4VUserDetectorConstruction.__init__(self)
        self.physical = world_obj
        
    def Construct(self):
        return self.physical

def build_world(world_physical):
    return World(air)





from PyCRUST._PyCRUST import geometry

def draw_solid( solid, translation, name, style ):

    x=geometry.GetVertices(solid, 0)
    y=geometry.GetVertices(solid, 1)
    z=geometry.GetVertices(solid, 2)

    xi=np.array(geometry.GetFacets(solid, 0))-1
    yi=np.array(geometry.GetFacets(solid, 1))-1
    zi=np.array(geometry.GetFacets(solid, 2))-1
    ji=np.array(geometry.GetFacets(solid, 3))-1
    ki=np.array(geometry.GetFacets(solid, 4))-1
    

    
    solid_points = []
    for xx, yy, zz in zip(x,y,z):
        p = g4.G4ThreeVector(xx,yy,zz)
        p = translation.getRotation()*p + translation.getTranslation()

        solid_points.append( [p.x, p.y, p.z] )

    solid_vert = []
    for i in range(len(xi)):
        p = g4.G4ThreeVector(x[xi[i]], y[xi[i]], z[xi[i]])
        p = translation.getRotation()*p + translation.getTranslation()
        solid_vert.append( [p.x, p.y, p.z] )

        p = g4.G4ThreeVector(x[yi[i]], y[yi[i]], z[yi[i]])
        p = translation.getRotation()*p + translation.getTranslation()
        solid_vert.append( [p.x, p.y, p.z] )

        p = g4.G4ThreeVector(x[zi[i]], y[zi[i]], z[zi[i]])
        p = translation.getRotation()*p + translation.getTranslation()
        solid_vert.append( [p.x, p.y, p.z] )

        p = g4.G4ThreeVector(x[ji[i]], y[ji[i]], z[ji[i]])
        p = translation.getRotation()*p + translation.getTranslation()
        solid_vert.append( [p.x, p.y, p.z] )

        p = g4.G4ThreeVector(x[ki[i]], y[ki[i]], z[ki[i]])
        p = translation.getRotation()*p + translation.getTranslation()
        solid_vert.append( [p.x, p.y, p.z] )

    level = len(name.split(":"))
    colorlist = ["red","green","blue","yellow","orange","cyan","violet","white"]
    color = None
    if level < len(colorlist): color = colorlist[level]

    opacity = 1.0
    if style: 
        opacity = style.GetColor().GetAlpha()
        r = style.GetColor().GetRed()
        g = style.GetColor().GetBlue()
        b = style.GetColor().GetGreen()
        color = f"rgb({r*255},{g*255},{b*255})"

    
    if True or style and style.GetForcedDrawingStyle() == G4VisAttributes.ForcedDrawingStyle.solid:
        
        mesh = go.Mesh3d(
                    # Set the coordinates
                    x=[face[0] for face in solid_points],
                    y=[face[1] for face in solid_points],
                    z=[face[2] for face in solid_points],
                    alphahull=0.5,
                    # Optional styling
                    color=color,
                    opacity=opacity,
                    showlegend=True,
                    name=str(name)
                )
    
    else:
        
        mesh = go.Scatter3d(x=[face[0] for face in solid_vert],
                            y=[face[1] for face in solid_vert],
                            z=[face[2] for face in solid_vert],
                            mode='lines',
                            opacity=opacity,
                            showlegend=True,
                            line={"color":color},
                            name=str(name))
    
    # mesh = go.Mesh3d(
    #     x=[0, 1, 2, 0],
    #     y=[0, 0, 1, 2],
    #     z=[0, 2, 0, 1],        
    #     # i, j and k give the vertices of triangles
    #     # here we represent the 4 triangles of the tetrahedron surface
    #     i=[0, 0, 0, 1],
    #     j=[1, 2, 3, 2],
    #     k=[2, 3, 1, 3],
    #     name='y',
    #     showscale=True,
    #     opacity=0.1
    # )
    
    return mesh


# def build_geometry_plot( physical_geometry, resolution=1000, opacity=0.01 ):
        
    
#     global_data = []
#     # Transform3D (const CLHEP::HepRotation &m, const CLHEP::Hep3Vector &v)
        
#     def traverse(physical, translation=None):
    
#         if not physical: return
    
#         solid = physical.GetLogicalVolume().GetSolid()
        
#         if (str(solid.GetName()) == "world"):
#             translation = G4Transform3D()
#         else:
#             translation *= G4Transform3D(physical.GetRotation(),  physical.GetTranslation())
            
#         logical = physical.GetLogicalVolume()
#         if (str(solid.GetName()) != "world"):
#             global_data.append(build_solid(solid, translation, opacity))
    
#         for i in range(logical.GetNoDaughters()):
#             traverse( logical.GetDaughter(i), translation )

    
#     traverse(physical_geometry.hierarchy['world']['physical'])
#     fig = go.Figure(data=global_data)
#     fig.update_layout( autosize=False, width=800, height=800, ) 
    
#     return fig



import plotly.graph_objects as go

def build_geometry_plot( physical_geometry, resolution=1000, opacity=0.01, draw_world = False ):
        
    
    global_data = []
    # Transform3D (const CLHEP::HepRotation &m, const CLHEP::Hep3Vector &v)
        
    def traverse(physical, translation=None, name=""):
    
        if not physical: return
        solid = physical.GetLogicalVolume().GetSolid()
        
        if (str(solid.GetName()) == "world"):
            if (draw_world): name += ":" + str(solid.GetName())
            translation = g4.G4Transform3D()
        else:
            name += ":" + str(solid.GetName())
            translation *= g4.G4Transform3D(physical.GetRotation(),  physical.GetTranslation())
            
        logical = physical.GetLogicalVolume()
        style = logical.GetVisAttributes()
        if (str(solid.GetName()) != "world" or draw_world):
            if not style or style.IsVisible():
                global_data.append(draw_solid(solid, translation, name, style))
    
        for i in range(logical.GetNoDaughters()):
            traverse( logical.GetDaughter(i), translation, name )

    
    traverse(physical_geometry.physical)
    fig = go.Figure(data=global_data)
    fig.update_layout( autosize=False, width=800, height=800, ) 
    
    return fig



