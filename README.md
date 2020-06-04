# Simple-Land-Use-Change-Model

Calibration and Simulation of a Model of Land Use Change used for predicting urbanization in the next decades

## Calibration

### Basics

In the Calibration phase, the model tries to learn from past trends the main drivers of growth in cities. 
We consider here 4 types of growth:

1- Edge Growth: Growth happening around already dense areas \\*

2- Road Related Growth: Growth happening around roads and/or public transport

3- Spontaneous Growth: Occurs when a new cell is urbanized in the middle of nowhere

4- Spread Growth: Occurs when a new cell is urbanized around an isolated small urban areas

### Inputs

urban_path_ini = 'Inputs/urban2012_roads.gif' # Path to Initial Urban Raster
urban_path_fin = 'Inputs/urban2017_roads.gif' # Path to Final Urban Raster
path_roads = 'Inputs/roads_12_mod.tif' # Path to Road Raster at the Initial Period

## Simulation 
