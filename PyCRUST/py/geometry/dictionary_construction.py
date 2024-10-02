# from geant4 import *
# from ..core.core import *

# def material(str):
#     return gNistManager.FindOrBuildMaterial(str)      


# # Function to load in a JSON Material table from CRESTA database and load it here.
# class dictionary_construction(G4VUserDetectorConstruction):
#     "My Detector Construction"

#     def __init__(self):

#         G4VUserDetectorConstruction.__init__(self)
#         self.hierarchy = {}

#     def __getitem__(self, item):
#         if item in self.hierarchy:
#           return self.hierarchy.get(item)
#         else:
#           self.hierarchy[item] = {
#             "logical": None,
#             "physical": None,
#             "solid": None,
#             "visual": None
#           }
#         return self.hierarchy.get(item)

#     def create_solid(self, table):

#         solid_type = table["solid"]
#         table["pName"] = table["index"]

#         t = datatable(table)

#         if solid_type == "G4Box":    return G4Box(t.pName, t.pX, t.pY, t.pZ)
#         if solid_type == "G4Cons":   return G4Cons(t.pName,t.pRmin1,t.pRmax1,t.pRmin2,t.pRmax2,t.pDz,t.pSPhi,t.pDPhi)
#         if solid_type == "G4Orb":    return G4Orb(t.pName,t.pRmax)
#         if solid_type == "G4Para":   return G4Para(t.pName,t.pDx,t.pDy,t.pDz,t.pAlpha,t.pTheta,t.pPhi)
#         if solid_type == "G4Sphere": return G4Sphere(t.pName, t.pRmin, t.pRmax, t.pSPhi, t.pDPhi, t.pSTheta, t.pDTheta)
#         if solid_type == "G4Sphere": return G4Torus(t.pName, t.pRmin, t.pRmax, t.pRtor, t.pSPhi, t.pDPhi)
#         if solid_type == "G4Tubs":   return G4Tubs( t.pName, t.pRMin, t.pRMax, t.pDz, t.pSPhi, t.pDPhi)
#         if solid_type == "G4Trd":    return G4Trd( t.pName, t.pdx1, t.pRMax, t.pDz, t.pSPhi, t.pDPhi )
#         raise AttributeError(f"Unkown solid type! {table}")

#     #G4Trap (const G4String &pName, G4double pDz, G4double pTheta, G4double pPhi, G4double pDy1, G4double pDx1, G4double pDx2, G4double pAlp1, G4double pDy2, G4double pDx3, G4double pDx4, G4double pAlp2)


#     def create_world(self, **kwargs):

#         world_material = material(kwargs['material'])
#         side = kwargs['side']
#         kwargs["pX"] = side
#         kwargs["pY"] = side
#         kwargs["pZ"] = side
#         kwargs["solid"] = "G4Box"
#         kwargs["index"] = "world"
#         self.hierarchy['world'] = {}
#         self.hierarchy['world']['solid'] = self.create_solid(kwargs)
        
#         self.hierarchy['world']['logical'] = G4LogicalVolume(self.hierarchy['world']['solid'], 
#                                                 world_material, 
#                                                 "world")
        
#         self.hierarchy['world']['physical'] = G4PVPlacement(G4Transform3D(), 
#                                                    self.hierarchy['world']["logical"], 
#                                                    "world", 
#                                                    None, 
#                                                    False, 
#                                                    0)

#         # visual = G4VisAttributes()
#         # visual.SetVisibility(True)
        
#         # self.hierarchy['world']['visual'] = visual
#         # self.hierarchy['world']['logical'].SetVisAttributes(visual)


#     # -----------------------------------------------------------------
#     def Construct(self): # return the world volume
#         return self.hierarchy['world']['physical']

#     def build_object_from_table(self, table):
        
#         object_name = table["index"]
#         mother_name = table["mother"]
#         self.hierarchy[object_name] = {}
        
#         self.hierarchy[object_name]['configuration'] = table
        
#         self.hierarchy[object_name]['solid'] = self.create_solid(table)

#         self.hierarchy[object_name]['material'] = material(table['material'])
        
#         self.hierarchy[object_name]['logical'] = G4LogicalVolume(
#                                             self.hierarchy[object_name]['solid'], 
#                                             self.hierarchy[object_name]['material'], 
#                                             object_name)

#         # visual = G4VisAttributes()
#         # visual.SetVisibility(True)
#         # visual.SetForceSolid(True)
        
#         # self.hierarchy[object_name]['visual'] = visual
#         # self.hierarchy[object_name]['logical'].SetVisAttributes(visual)

#         if "position" in table:
#             self.hierarchy[object_name]["position"] = G4ThreeVector(table["position"][0]*mm,
#                                                                     table["position"][1]*mm,
#                                                                     table["position"][2]*mm)
#         else:
#             self.hierarchy[object_name]["position"] = G4ThreeVector()

#         self.hierarchy[object_name]["rotation"] = G4RotationMatrix()
#         if "rotation" in table:
#             self.hierarchy[object_name]["rotation"].rotateX(table["rotation"][0])
#             self.hierarchy[object_name]["rotation"].rotateY(table["rotation"][1])
#             self.hierarchy[object_name]["rotation"].rotateZ(table["rotation"][2])
        
#         if mother_name:
#             self.hierarchy[object_name]['physical'] = G4PVPlacement(
#                 self.hierarchy[object_name]["rotation"],
#                 self.hierarchy[object_name]["position"],
#                 self.hierarchy[object_name]["logical"], 
#                 object_name, 
#                 self.hierarchy[mother_name]["logical"],  
#                 False, 
#                 0)
#         else:
#             self.hierarchy[object_name]['physical'] = G4PVPlacement(
#                 self.hierarchy[object_name]["rotation"],
#                 self.hierarchy[object_name]["position"],
#                 self.hierarchy[object_name]["logical"], 
#                 object_name, 
#                 0,
#                 False, 
#                 0)
        

#         self.hierarchy[object_name]['mother_logical'] = self.hierarchy[mother_name]["logical"]
#         self.hierarchy[object_name]['mother_physical'] = self.hierarchy[mother_name]["physical"]



#     def build_geo_from_database(self):

#         if "GEO" not in db.database: return
#         geo_tables_to_handle = db.database["GEO"]
        
#         count = 0
#         while len(geo_tables_to_handle) > 0:

#             all_tables = geo_tables_to_handle.copy()
#             for tablekey in all_tables:

#                 current_table = all_tables[tablekey]
#                 mother_id = current_table["mother"]

#                 if not mother_id in self.hierarchy: continue
                    
#                 self.build_object_from_table( current_table )

#                 geo_tables_to_handle.pop(tablekey)



#         for key in self.hierarchy: 
#             print("-->", key)
#             # print(self.hierarchy[key])


#             # all_tables = geo_tables_to_handle.copy()
#             # print(geo_tables_to_handle)
            
#             # table_added = False
#             # for table in all_tables:
#             #     print(table, geo_tables_to_handle[table])
            
#             #     if geo_tables_to_handle[table]["mother"] != mother_id: continue
#             #     print("BUILDING", table, geo_tables_to_handle[table]["mother"])
#             #     mother_id = table
#             #     print("NEW MOTHER", mother_id)

#             #     self.build_object_from_table( geo_tables_to_handle[table] )
#             #     geo_tables_to_handle.pop(table)

#             #     table_added = True
#             #     break

#             # if not table_added:
#             #     print("Warning can't find mother in hierarchy!")


                
                

# class jupyer_construction(G4VUserDetectorConstruction):
#     def __init__(self):
#         G4VUserDetectorConstruction.__init__(self)
#         self.hierarchy = {}

#     def __getitem__(self, item):
#         if item in self.hierarchy:
#           return self.hierarchy.get(item)
#         else:
#           self.hierarchy[item] = {
#             "logical": None,
#             "physical": None,
#             "solid": None,
#             "visual": None
#           }
#         return self.hierarchy.get(item)

#     def create_solid(self, table):

#         solid_type = table["solid"]
#         table["pName"] = table["index"]

#         t = datatable(table)

#         if solid_type == "G4Box":    return G4Box(t.pName, t.pX, t.pY, t.pZ)
#         if solid_type == "G4Cons":   return G4Cons(t.pName,t.pRmin1,t.pRmax1,t.pRmin2,t.pRmax2,t.pDz,t.pSPhi,t.pDPhi)
#         if solid_type == "G4Orb":    return G4Orb(t.pName,t.pRmax)
#         if solid_type == "G4Para":   return G4Para(t.pName,t.pDx,t.pDy,t.pDz,t.pAlpha,t.pTheta,t.pPhi)
#         if solid_type == "G4Sphere": return G4Sphere(t.pName, t.pRmin, t.pRmax, t.pSPhi, t.pDPhi, t.pSTheta, t.pDTheta)
#         if solid_type == "G4Sphere": return G4Torus(t.pName, t.pRmin, t.pRmax, t.pRtor, t.pSPhi, t.pDPhi)
#         if solid_type == "G4Tubs":   return G4Tubs( t.pName, t.pRMin, t.pRMax, t.pDz, t.pSPhi, t.pDPhi)
#         if solid_type == "G4Trd":    return G4Trd( t.pName, t.pdx1, t.pRMax, t.pDz, t.pSPhi, t.pDPhi )
#         raise AttributeError(f"Unkown solid type! {table}")

#     #G4Trap (const G4String &pName, G4double pDz, G4double pTheta, G4double pPhi, G4double pDy1, G4double pDx1, G4double pDx2, G4double pAlp1, G4double pDy2, G4double pDx3, G4double pDx4, G4double pAlp2)


#     def create_world(self, **kwargs):

#         world_material = material(kwargs['material'])
#         side = kwargs['side']
#         kwargs["pX"] = side
#         kwargs["pY"] = side
#         kwargs["pZ"] = side
#         kwargs["solid"] = "G4Box"
#         kwargs["index"] = "world"
#         self.hierarchy['world'] = {}
#         self.hierarchy['world']['solid'] = self.create_solid(kwargs)
        
#         self.hierarchy['world']['logical'] = G4LogicalVolume(self.hierarchy['world']['solid'], 
#                                                 world_material, 
#                                                 "world")
        
#         self.hierarchy['world']['physical'] = G4PVPlacement(G4Transform3D(), 
#                                                    self.hierarchy['world']["logical"], 
#                                                    "world", 
#                                                    None, 
#                                                    False, 
#                                                    0)

#         # visual = G4VisAttributes()
#         # visual.SetVisibility(True)
        
#         # self.hierarchy['world']['visual'] = visual
#         # self.hierarchy['world']['logical'].SetVisAttributes(visual)


#     # -----------------------------------------------------------------
#     def Construct(self): # return the world volume
#         return self.hierarchy['world']['physical']

#     def build_object_from_table(self, table):
        
#         object_name = table["index"]
#         if "mother" in table:
#             mother_name = table["mother"]
#         else:
#             mother_name = None
#         self.hierarchy[object_name] = {}
        
#         # self.hierarchy[object_name]['configuration'] = table
        
#         self.hierarchy[object_name]['solid'] = self.create_solid(table)

#         self.hierarchy[object_name]['material'] = material(table['material'])
        
#         self.hierarchy[object_name]['logical'] = G4LogicalVolume(
#                                             self.hierarchy[object_name]['solid'], 
#                                             self.hierarchy[object_name]['material'], 
#                                             object_name)

#         # visual = G4VisAttributes()
#         # visual.SetVisibility(True)
#         # visual.SetForceSolid(True)
        
#         # self.hierarchy[object_name]['visual'] = visual
#         # self.hierarchy[object_name]['logical'].SetVisAttributes(visual)

#         if "position" in table:
#             self.hierarchy[object_name]["position"] = G4ThreeVector(table["position"][0]*mm,
#                                                                     table["position"][1]*mm,
#                                                                     table["position"][2]*mm)
#         else:
#             self.hierarchy[object_name]["position"] = G4ThreeVector()

#         self.hierarchy[object_name]["rotation"] = G4RotationMatrix()
#         if "rotation" in table:
#             self.hierarchy[object_name]["rotation"].rotateX(table["rotation"][0])
#             self.hierarchy[object_name]["rotation"].rotateY(table["rotation"][1])
#             self.hierarchy[object_name]["rotation"].rotateZ(table["rotation"][2])
        
#         if mother_name:
#             self.hierarchy[object_name]['physical'] = G4PVPlacement(
#                 self.hierarchy[object_name]["rotation"],
#                 self.hierarchy[object_name]["position"],
#                 self.hierarchy[object_name]["logical"], 
#                 object_name, 
#                 self.hierarchy[mother_name]["logical"],  
#                 False, 
#                 0)
#             self.hierarchy[object_name]['mother_logical'] = self.hierarchy[mother_name]["logical"]
#             self.hierarchy[object_name]['mother_physical'] = self.hierarchy[mother_name]["physical"]


#         else:
#             self.hierarchy['world']['physical'] = G4PVPlacement(G4Transform3D(), 
#                 self.hierarchy['world']["logical"], 
#                 "world", 
#                 None, 
#                 False, 
#                 0)
        



#     def build(self, current_table):

#         if "index" not in current_table:
#             current_table["index"] = "world"

#         self.build_object_from_table( current_table )

#         if "children" in current_table:
#             for obj in current_table["children"]:
#                 new_table = current_table["children"][obj]
#                 new_id = obj
#                 new_table["index"] = obj
#                 new_table["mother"] = current_table["index"]

#                 self.build(new_table)
        
