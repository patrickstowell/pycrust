# from geant4 import *
# # Material Manager
# import os
# import glob
# import json
# import yaml

# def UI(val):
#     gUImanager.ApplyCommand(val)

# def MACRO(filename):
#   for line in filename:
#     UI(line)


# allowed_builtins = {"__builtins__": {"min": min, "max": max}, "mm":mm, "m":m}

# global local_variables
# local_variables = {}

# class parametertable:
#   def __init__(self, dict):
#     self.dt = dict

#   def parse(self, name):
#     try:
#       return exec(self.dt[name], allowed_builtins, {})
#     except:
#       return self.dt[name]

#   def __getitem__(self, arg):
#         return self.dt[arg]

#   def __getattr__(self, name):
#     try:
#       return self.parse(name)
#     except:
#       raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

# def get_len(key):
#     return len(key[0])

# class datatable:
#   def __init__(self, dict):
#     self.dt = dict

#   def parse(self, name):
  
#     expression = str(self.dt[name])
#     for subkey in local_variables:
#       subtable = local_variables[subkey].dt

#       test_dict_list = list(subtable.keys())
#       test_dict_list.sort(key = get_len, reverse=True)

#       for subsubkey in test_dict_list:
#           idkey = subkey + "." + subsubkey
#           idvalue = subtable[subsubkey]
#           expression = expression.replace(idkey, idvalue)

#     try:
#       parsedvalue = eval(expression, allowed_builtins, local_variables)
#       return parsedvalue
#     except:
#       return self.dt[name]

#   def __getitem__(self, arg):
#         return self.dt[arg]

#   def __getattr__(self, name):
#     try:
#       return self.parse(name)
#     except:
#       raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


# class database:

#     def __init__(self):
#         self.PYCRUST_DB = os.getenv("PYCRUST_DB")
#         self.database = {}


#     def add(self, data):
#         if isinstance(data,dict):
#             data = [data]
            
#         for dt in data:

#             tabletype  = dt["type"]
#             tableindex = dt["index"]

#             if tabletype == "PARAMETER" or tabletype == "VARIABLE":
#                local_variables[tableindex] = parametertable(dt)

#             if tabletype not in self.database: self.database[tabletype] = {}
#             self.database[tabletype][tableindex] = dt
        
#     def initialize(self):
        
#         global local_variables

#         self.database = {}
#         for filename in glob.glob(f"{self.PYCRUST_DB}/**.db"):
#             # try:
#             data = yaml.safe_load(open(filename))

#             self.add(data)

#     def __getattr__(self, name):

#       if name in local_variables:
#          return local_variables[name]

#       try:
#         return self.database[name]
#       except:
#         raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

#     def __getitem__(self, name):
#         return self.database[name]

# global db
# db = database()
# db.initialize()

# def material(str):
#     return gNistManager.FindOrBuildMaterial(str)      

# class material_library:
#   def __init__(self):
#     self.mdata = {}

#   def initialize(self):
#     self.mdata = {}
#     if "MATERIAL" not in db.database: return
#     # for obj in db.database["MATERIAL"]:

#   def get_material(name):
#     if name not in self.mdata:
#       self.mdata[name] = material(name)
#     return self.mdata[name]

#   def __getattr__(self, name):
#         try:
#           return self.get_material(name)
#         except:
#             raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

# global materials
# materials = material_library()
# materials.initialize()





