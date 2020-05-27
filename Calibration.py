import rasterio
import numpy as np
import random
import time
from numba import njit
from numba.typed import Dict
from utils import *

### INPUTS 

date_ini = '1982'
data_fin = '1994'

urban_path_ini = 'Inputs/urban1982_roads.gif'
urban_path_fin = 'Inputs/urban1994_roads.gif'
path_roads = 'Inputs/roads_82_mod.tif'
excluded_areas_path = 'Inputs/excluded.gif'

### Reading Inputs and estimating new urbanisation

# Urban Areas
urban_ini = rasterio.open(urban_path_ini).read(1)
urban_fin = rasterio.open(urban_path_fin).read(1)

diff_urb = urban_fin - urban_ini
new_urb_index = np.where(diff_urb==255)
new_urb_index = [(a,b) for a,b in zip(new_urb_index[0],new_urb_index[1])]
new_urbanisation = len(new_urb_index)

# Roads
roads = rasterio.open(path_roads).read(1)

# Raster Profile
raster_profile = rasterio.open(urban_path_ini).profile

### Candidate Cells for Growth

edge_growth_cells,spread_growth_cells = create_edge_spread_poll(urban_ini,255,5)
road_growth_cells = create_road_poll(roads,urban_ini,255,[],edge_growth_cells,spread_growth_cells)
spont_growth_cells = create_spont_poll(urban_ini,0,edge_growth_cells,road_growth_cells,spread_growth_cells,[])

### Computing coeffs of growth

new_edge = len(edge_growth_cells) - len(list(set(edge_growth_cells) - set(new_urb_index)))
new_road = len(road_growth_cells) - len(list(set(road_growth_cells) - set(new_urb_index)))
new_spread = len(spread_growth_cells) - len(list(set(spread_growth_cells) - set(new_urb_index)))
new_spont = len(spont_growth_cells) - len(list(set(spont_growth_cells) - set(new_urb_index)))

edge_coef = new_edge/new_urbanisation
road_coef = new_road/new_urbanisation
spread_coef = new_spread/new_urbanisation
spont_coef = new_spont/new_urbanisation

print('Edge_Growth:', np.round(new_edge/new_urbanisation,2),', ','Road_Growth:',np.round(new_road/new_urbanisation,2),', ',
      'Spread_Growth:',np.round(new_spread/new_urbanisation,2),', ','Spont_Growth:', np.round(new_spont/new_urbanisation,2))