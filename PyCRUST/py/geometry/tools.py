from geant4 import *
from .._PyCRUST import geometry
from ..core.core import *
# from .. import GetDensityAtPosition
import plotly.graph_objects as go
import numpy as np

# def map_density(xspace, yspace, zspace):

#     data = []
#     for i in range(len(xspace)):
#         val = GetDensityAtPosition(xspace[i],yspace[i],zspace[i])
#         data.append(val)

#     return np.array(data)

    
def sample_solid( solid, translation, opacity ):
    
    solid_points = []
    for i in range(resolution): 
        p = solid.GetPointOnSurface()
        p = translation.getRotation()*p + translation.getTranslation()
        
        solid_points.append( [p.x, p.y, p.z] )

    # vals = sorted(solid_points)
    vals = solid_points
    
    mesh = go.Scatter3d(
                # Set the coordinates
                x=[face[0] for face in vals],
                y=[face[1] for face in vals],
                z=[face[2] for face in vals],
                # Optional styling
                opacity=opacity,
                mode='lines',
                name=str(solid.GetName())
            )
    
    return mesh

# def build_solid( solid, translation, opacity ):

    

#     solid_points = []
#     for xx, yy, zz in zip(x,y,z):
#         p = G4ThreeVector(xx,yy,zz)
#         p = translation.getRotation()*p + translation.getTranslation()

#         solid_points.append( [p.x, p.y, p.z] )

#     mesh = go.Mesh3d(
#                 # Set the coordinates
#                 x=[face[0] for face in solid_points],
#                 y=[face[1] for face in solid_points],
#                 z=[face[2] for face in solid_points],
#                 # Optional styling
#                 opacity=opacity,
#                 alphahull=2,
#                 showlegend=True,
#                 name=str(solid.GetName())
#             )
    
#     return mesh


# def build_solid( solid, translation, opacity, name ):

#     x=geometry.GetVertices(solid, 0)
#     y=geometry.GetVertices(solid, 1)
#     z=geometry.GetVertices(solid, 2)
#     solid_points = []
#     for xx, yy, zz in zip(x,y,z):
#         p = G4ThreeVector(xx,yy,zz)
#         p = translation.getRotation()*p + translation.getTranslation()

#         solid_points.append( [p.x, p.y, p.z] )

#     mesh = go.Mesh3d(
#                 # Set the coordinates
#                 x=[face[0] for face in solid_points],
#                 y=[face[1] for face in solid_points],
#                 z=[face[2] for face in solid_points],
#                 # Optional styling
#                 opacity=opacity,
#                 alphahull=0.01,
#                 showlegend=True,
#                 name=str(name)
#             )
    
#     return mesh


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



# import plotly.graph_objects as go

# def build_geometry_plot( physical_geometry, resolution=1000, opacity=0.01, draw_world = False ):
        
    
#     global_data = []
#     # Transform3D (const CLHEP::HepRotation &m, const CLHEP::Hep3Vector &v)
        
#     def traverse(physical, translation=None, name=""):
    
#         if not physical: return
#         solid = physical.GetLogicalVolume().GetSolid()
        
#         if (str(solid.GetName()) == "world"):
#             if (draw_world): name += ":" + str(solid.GetName())
#             translation = G4Transform3D()
#         else:
#             name += ":" + str(solid.GetName())
#             translation *= G4Transform3D(physical.GetRotation(),  physical.GetTranslation())
            
#         logical = physical.GetLogicalVolume()
#         if (str(solid.GetName()) != "world" or draw_world):
#             global_data.append(build_solid(solid, translation, opacity, name))
    
#         for i in range(logical.GetNoDaughters()):
#             traverse( logical.GetDaughter(i), translation, name )

    
#     traverse(physical_geometry.hierarchy['world']['physical'])
#     fig = go.Figure(data=global_data)
#     fig.update_layout( autosize=False, width=800, height=800, ) 
    
#     return fig