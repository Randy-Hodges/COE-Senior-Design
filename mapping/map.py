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

# Find bounds
x_gcs_left = 97.6063196 #the longitude is made positive
y_gcs_top = 30.3267942
length_gcs = 0.0058647 #length of both sides of raster in gcs

x_length = rst.bounds.right-rst.bounds.left #length of raster in x in matplotlib
y_length = rst.bounds.top-rst.bounds.bottom #length of raster in y in matplotlib

# Convert gcs coordinates to matplotlib coordinates
x_gcs = 97.602743
y_gcs = 30.324161

x_points = ((x_gcs_left - x_gcs)/length_gcs)*x_length
y_points = ((y_gcs_top - y_gcs)/length_gcs)*y_length

# Convert gcs coordinates to matplotlib coordinates
x_gcs2 = 97.60284224192607
y_gcs2 = 30.324767588927372

x_points2 = ((x_gcs_left - x_gcs2)/length_gcs)*x_length
y_points2 = ((y_gcs_top - y_gcs2)/length_gcs)*y_length

# Overlay points on top of raster
x = [rst.bounds.left + x_points, rst.bounds.left + x_points2]
y = [rst.bounds.top - y_points, rst.bounds.top - y_points2]
ax.scatter(x, y, color='red', marker='x', label = 'Critical Target')

# Convert gcs coordinates to matplotlib coordinates
x_gcs3 = 97.60230311795735
y_gcs3 = 30.3236423845285

x_points3 = ((x_gcs_left - x_gcs3)/length_gcs)*x_length
y_points3 = ((y_gcs_top - y_gcs3)/length_gcs)*y_length

x = [rst.bounds.left + x_points3]
y = [rst.bounds.top - y_points3]
ax.scatter(x, y, color='blue', marker='o', label = 'Non-Critical Target')

# Show the plot
plt.legend()
plt.show()
