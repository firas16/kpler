# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import matplotlib.pyplot as plt
import pandas as pd

#read positions
df = pd.read_csv("data/input/Galveston_2017_11_25-26.csv", header=0, sep=';')
#filter vessels
vessel_list = (5030, 4721)
filter = df["vessel_id"].isin(vessel_list)

df_filtered = df.where(filter).dropna(how="all")

min_longitude = df["longitude"].min()
max_longitude = df["longitude"].max()
min_latitude = df["latitude"].min()
max_latitude = df["latitude"].max()

BBox = ((df.longitude.min(),   df.longitude.max(),
         df.latitude.min(), df.latitude.max()))


ruh_m = plt.imread('./data/input/map.png')
fig, ax = plt.subplots(figsize = (8,7))
ax.scatter(df_filtered.longitude, df_filtered.latitude, zorder=1, alpha= 0.2, c=df_filtered.vessel_id, s=10)
ax.set_title('Plotting Spatial Data STS')
ax.set_xlim(BBox[0],BBox[1])
ax.set_ylim(BBox[2],BBox[3])
ax.imshow(ruh_m, zorder=0, extent = BBox, aspect= 'equal')
plt.show()