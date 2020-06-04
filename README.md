# Simple-Land-Use-Change-Model

Calibration and Simulation of a Model of Land Use Change used for predicting urbanization in the next decades

## Calibration

### Basics

In the Calibration phase, the model tries to learn from past trends the main drivers of growth in cities. 
We consider here 4 types of growth:

1- Edge Growth: Growth happening around already dense areas \
2- Road Related Growth: Growth happening around roads and/or public transport\
3- Spontaneous Growth: Occurs when a new cell is urbanized in the middle of nowhere\
4- Spread Growth: Occurs when a new cell is urbanized around an isolated small urban areas

### Inputs

urban_path_ini = 'Inputs/urban2012_roads.gif' _# Path to Initial Urban Raster_\
urban_path_fin = 'Inputs/urban2017_roads.gif' _# Path to Final Urban Raster_\
path_roads = 'Inputs/roads_12_mod.tif' _# Path to Road Raster at the Initial Period_

### Output

The Calibration phase gives 4 parameters of growth representing the share of past urban growth associated to each of them

## Simulation 

### Basics
Based on the estimated parameters for each type of growth and a number of cells to urbanize, we simulate future trends of urbanization. This is done based on an iterative procedure. At the beginning of the process, we identify candidate cells that are suited for each type of urbanization. Then, after each new urbanization, we need to upload the poll of candidate cells related to the different growth strategies.

We present here 2 methods of Simulation:

1- Simulation: At each step of the urbanization and for each type of growth, we randomly select a new cell of urbanization \
2- Simulation_prio : For the edge related growth, the cells are chosen based on the number of urban cells next to them.

### Inputs

date_ini = '2017' _# Initial date of the Simulation_\
date_fin = '2050' _# End date of the Simulation_

urban_path_ini = 'Inputs/urban2017_roads.gif' _# Initial Raster of Urban Areas_\
path_roads = 'Inputs/roads_17_mod.tif' _# Initial Raster of Roads_\
excluded_areas_path = 'Inputs/excluded.gif' _# Areas excluded from Urbanization_\
outside_boundaries_path = 'Inputs/outside_boundaries.tif' _# If the area of study is not square, a Raster File for outside boundaries_

objectif_urba =  24004 _# Number of cells to urbanize_\
edge_growth,spread_growth,road_growth,spont_growth = 93,4,1,2 _# Coefficients of the different types of growth (they have to sum to 100)_

### Outputs

A new Map of Urbanization with the new urbanized cells

