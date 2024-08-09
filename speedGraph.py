import matplotlib

import numpy as np

from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

import matplotlib.pyplot as plt
import pandas

df = pandas.read_excel("/Users/mercedesstringermartin/Documents/Y3/Diss/M2_T4.xlsx")

plt.scatter(df['Corner X Coords'],df['Corner Y Coords'],color = 'black',marker='x')
#
plt.plot(df['X position'], df['Y position'], color = 'black')
# plt.show()

x = df['X position']
y = df['Y position']
s = df['Speed (pxl/sec)']

#cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["green","yellow","red"])
#cmap = plt.cm.coolwarm
# plt.scatter(x, y, c=s,cmap=plt.cm.coolwarm)
plt.axis('off')

#plt.scatter(x, y, c=s,cmap=cmap, s= 30)
plt.show()

