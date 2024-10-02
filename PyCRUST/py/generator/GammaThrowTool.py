import pandas as pd
import numpy as np

isotopes = {}
isotopes["isotope"] = []
isotopes["branch"]  = []
isotopes["activity"]  = []
isotopes["ratio"]  = []
isotopes["energy"]  = []
isotopes["weight"]  = []
isotopes["x_low"]  = []
isotopes["x_high"]  = []
isotopes["y_low"]  = []
isotopes["y_high"]  = []
isotopes["z_low"]  = []
isotopes["z_high"]  = []
isotopes["energy_bias"] = []
isotopes["depth_bias"] = []

def retrieve_branch_data(isotope, activity, energy_bias=1):
    if isotope == "Co-60":
        return [{
            "isotope": "Co-60",
            "branch": "low",
            "ratio": 0.999,
            "energy": 1.113,
            "energy_bias": energy_bias
        },{
            "isotope": "Co-60",
            "branch": "high",
            "ratio": 0.981,
            "energy": 1.145,
            "energy_bias": energy_bias
        }]
    elif isotope == "Cs-137":
        return [{
            "isotope": "Cs-137",
            "branch": "low",
            "ratio": 0.999,
            "energy": 1.345,
            "energy_bias": energy_bias
        }]

def add_isotope(data, isotope, activity, voxel):
    for obj in retrieve_branch_data(isotope, activity):
        for key in obj:
            data[key].append(obj[key])
        for key in voxel:
            data[key].append(voxel[key])

        data["activity"].append(activity)
        data["weight"].append(1.0) #data["ratio"] * data["activity"])
    return data
    
def build_voxel( x, y, z, dx, dy, dz):
    data = {}
    data["x_low"] = x-dx/2  
    data["x_high"]= x+dx/2 
    data["y_low"] = y-dy/2  
    data["y_high"]= y+dy/2  
    data["z_low"] = z-dz/2  
    data["z_high"]= z+dz/2  
    data["depth_bias"] = np.exp(-np.abs(z))
    return data

for x in np.linspace(-10,10,21):
    for y in np.linspace(-10,10,21):
        for z in np.linspace(-10,0,10):

            vox = build_voxel(x, y, z, 1, 1, 1)
            add_isotope(isotopes, "Co-60", 5.12, vox) 

            if x > 0:
                vox = build_voxel(x, y, z, 1, 1, 1)
                add_isotope(isotopes, "Cs-137", 5.12, vox) 
        
            

# def add_density(df):
    
            
df = pd.DataFrame(data=isotopes)
# add_density(df)
df["weight"] = df["activity"] * df["ratio"] * df["energy_bias"] * df["depth_bias"]
totalweight = np.sum(df["weight"])
cumweight = []
cumtotal = 0
for v in df["weight"].values:
    cumtotal += v
    cumweight.append(cumtotal)

count = 0
for vox in df:
    count += 1
    box2 = component_build(name=f"test{count}", 
                solid=build_box(f"test{count}", 1, 1, 1), 
                material="G4_AIR", 
                mother=air, pos=[x,y,z])


df["cum_weight"] = cumweight/totalweight

print(df)


import random

def sample(df):

    rand = random.random()
    sub = np.sum((df["cum_weight"] < rand).astype(int))-1
    row = df.iloc[sub]

    pos_x = row["x_low"] + random.random() * (row["x_high"] - row["x_low"])
    pos_y = row["y_low"] + random.random() * (row["y_high"] - row["y_low"])
    pos_z = row["z_low"] + random.random() * (row["z_high"] - row["z_low"])
    iso = row["isotope"]
    branch = row["branch"]
    bias = row["depth_bias"] * row["energy_bias"]

    return {"x":pos_x, "y": pos_y, "z": pos_z, "iso": iso, "branch": branch, "bias":bias}

dataset = []
for i in range(100000):
    dt = sample(df)
    dataset.append(dt)

df2 = pd.DataFrame(data=dataset)

print(df2)

import matplotlib.pyplot as plt

plt.hist2d(x=df2.x, y=df2.y, bins=[20,20])
plt.show()


plt.hist2d(x=df2.x, y=df2.z, bins=[20,20])
plt.show()


