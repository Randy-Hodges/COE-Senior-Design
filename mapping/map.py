import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Patch
import numpy as np
import rasterio 

# Open raster file with rasterio
rst = rasterio.open('ARCAClippedGCS.tif')

# Read raster data into numpy array
data = rst.read(1)

# Define colormap for raster
cmap = LinearSegmentedColormap.from_list('mycmap', [(0, 'black'), (1, 'white')])

# Create figure and axis objects
fig, ax = plt.subplots(figsize=(10, 10))

# Plot raster as image
ax.imshow(data, cmap=cmap, extent=[rst.bounds.left, rst.bounds.right, rst.bounds.bottom, rst.bounds.top])

# set bounds
x_gcs_left = 97.6063196 #the longitude is made positive
y_gcs_top = 30.3267942
length_gcs = 0.0058647 #length of both sides of raster in gcs

x_length = rst.bounds.right-rst.bounds.left #length of raster in x in matplotlib
y_length = rst.bounds.top-rst.bounds.bottom #length of raster in y in matplotlib

# Convert gcs coordinates to matplotlib coordinates
# set coordinates of empty tarps
x_gcs_tarp = [97.602743, 97.60284224192607, 97.60230311795735]
y_gcs_tarp = [30.324161, 30.3236423845285, 30.3236423845285]

#convert from gcs to matplotlib
x_points = [((x_gcs_left - x_gcs_tarp[i])/length_gcs)*x_length for i in range(0, len(x_gcs_tarp))]
y_points = [((y_gcs_top - y_gcs_tarp[i])/length_gcs)*y_length for i in range(0, len(y_gcs_tarp))]   

# Overlay points on top of raster
x = [rst.bounds.left + x_points[i] for i in range(0, len(x_gcs_tarp))]
y = [rst.bounds.top - y_points[i] for i in range(0, len(y_gcs_tarp))]
ax.scatter(x, y, color='blue', marker='s', label = 'Empty Tarp')

# Convert gcs coordinates to matplotlib coordinates
# set coordinates of Non-Critical Targets
x_gcs_non = [97.602394]
y_gcs_non = [30.324453]

#convert from gcs to matplotlib
x_points = [((x_gcs_left - x_gcs_non[i])/length_gcs)*x_length for i in range(0, len(x_gcs_non))]
y_points = [((y_gcs_top - y_gcs_non[i])/length_gcs)*y_length for i in range(0, len(y_gcs_non))]   

# Overlay points on top of raster
x = [rst.bounds.left + x_points[i] for i in range(0, len(x_gcs_non))]
y = [rst.bounds.top - y_points[i] for i in range(0, len(y_gcs_non))]
ax.scatter(x, y, color='Cyan', marker='o', label = 'Non-Critical')

# Convert gcs coordinates to matplotlib coordinates
# set coordinates of Critical Targets
x_gcs_crit = [97.603051]
y_gcs_crit = [30.324997]

#convert from gcs to matplotlib
x_points = [((x_gcs_left - x_gcs_crit[i])/length_gcs)*x_length for i in range(0, len(x_gcs_crit))]
y_points = [((y_gcs_top - y_gcs_crit[i])/length_gcs)*y_length for i in range(0, len(y_gcs_crit))]   

# Overlay points on top of raster
x = [rst.bounds.left + x_points[i] for i in range(0, len(x_gcs_crit))]
y = [rst.bounds.top - y_points[i] for i in range(0, len(y_gcs_crit))]
ax.scatter(x, y, color='Red', marker='x', label = 'Critical')

# Show the plot
plt.legend()
plt.show()
