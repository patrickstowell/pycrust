# # License & Copyright
# # ===================
# #
# # Copyright 2012 Christopher M Poole <mail@christopherpoole.net>
# #
# # This program is free software: you can redistribute it and/or modify
# # it under the terms of the GNU General Public License as published by
# # the Free Software Foundation, either version 3 of the License, or
# # (at your option) any later version.
# #
# # This program is distributed in the hope that it will be useful,
# # but WITHOUT ANY WARRANTY; without even the implied warranty of
# # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# # GNU General Public License for more details.
# #
# # You should have received a copy of the GNU General Public License
# # along with this program.  If not, see <http://www.gnu.org/licenses/>.
# # from geant4 import *

from . import geometry 
from . import core
from . import physics 




# from ._PyCRUST import *
import geant4 as g4
import geant4

# geometry.__dict__.update(_pygeometry.__dict__)


# class var_container():
#     def __init__(self):
#         self.id = "container"
        
# class analysis_class():
#     def __init__(self, ids):
#         self.id = ids
#         self.flags = var_container()
#         self.variables  = var_container()
#         self.config  = var_container()
#         self.tuple = {}
#         self.triggered = False

#     def selection(self):
#         return self.triggered

#     def reset(self):
#         self.triggered = False
#         for v in vars(self.variables):
#             self.variables.__setattr__(v, 0)

#         for v in vars(self.flags):
#             self.flags.__setattr__(v, 0)

# global gAnalysis
# gAnalysis = analysis_class("PyCRUST Main")

# gAnalysis.tuple = analysis.Manager()
# gAnalysisManager = gAnalysis.tuple

# gAnalysis.flags = analysis_class("Flags")
# gAnalysis.vars = analysis_class("Vars")
# gAnalysis.committed = False

# def dummy_selection(self):
#     return True

# gAnalysis.selection = dummy_selection

# class CustomRun(G4Run):        
#     def RecordEvent(self, ev):
#         if ev.GetEventID() % 10000 == 0: print(ev.GetEventID())

#         # if (gAnalysis.selection(gAnalysis)):
#             # gAnalysis.tuple.fill_int("evt", ev.GetEventID())
#             # gAnalysis.tuple.save_row()

#         # gAnalysis.reset()
        
#         return

# global g4run
# g4run = None

# class analysis_runaction(G4UserRunAction):
#     def BeginOfRunAction(self, run):
#         print("BEGINNING NEW RUN")
#         # if (not gAnalysis.committed):
#             # gAnalysis.tuple.add_int("evt")
#             # gAnalysis.tuple.commit()
#             # gAnalysis.committed = True
            
#         print("Opening new run")
#         # gAnalysis.tuple.open_run()
#         print("Calling RESET")
#         # gAnalysis.reset()
        

#     def EndOfRunAction(self, run):
#         print("Closing RUN RESET")
#         # gAnalysis.tuple.close_run()

#     def GenerateRun(self):
#         # print("CREATING A RUN")
#         self.g4run = CustomRun()
#         return self.g4run

# gAnalysis.action = analysis_runaction


# import pandas as pd
# import re
# def csv_to_dataframe(csv_string):
#     # Split the CSV string into lines
#     #lines = csv_string.strip().split('\n')
    
#     # Extract column names from header information
#     columns = []
#     for line in open(csv_string):
#         if line.startswith('#column'):
#             match = re.search(r'#column\s+(.*)', line)
#             if match:
#                 columns.append(match.group(1).split()[1])
    
#     # Read the data from CSV (skipping header lines)
#     df = pd.read_csv(csv_string, header=None, comment='#')
    
#     # Set column names
#     if len(columns) == len(df.columns):
#         df.columns = columns
    
#     return df

# from .core import *
# from .generator import *
# from . import materials 
