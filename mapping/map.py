import rasterio
import matplotlib.pyplot as plt
import earthpy.plot as ep

src = rasterio.open('manor-nwc4.tif')
src.mode

plt.imshow(src.read(1, masked=True))
plt.show()

ep.plot_bands(src.read(1, masked=True))

ep.plot_rgb(src.read(), rgb=[2,1,0], stretch=True)
