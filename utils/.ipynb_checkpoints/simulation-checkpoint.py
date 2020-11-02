import rasterio
import numpy as np
import random
import time
from numba import njit

@njit
def simulation_numba(candidate_cells,ini_urb,order_urbanization,distance,index_exclu_1d_arr,index_double):
    """
    Given a raster of urbanisation data and a list of coordinates
    return all coordinates of non urban areas in a square of size "dist" around the list of coordinates
    
    Args:
        *candidate_cells* : A numpy array of cells corresponding to each type of growth
            
        *ini_urb* : A numpy array of urbanization data
        
        *order_urbanization* : A numpy array giving the order of urbanization among the 4 types of growth

        *dist* : Distance around list_coord where we look for non urban areas. Dist=1 means we are looking for non urban cells within a buffer of 1 cell (total of 8 cells checked)

        *index_exclu_1d_arr* : Index of cells excluded from Urbanization

        *index_double* : Array of tuples for the area
        
    Return:
        *new_urb*: list of indexes of new urban cells.
    """
    new_urb = np.zeros(len(order_urbanization),dtype=np.int64)
    lig,col = candidate_cells.shape
    i = 0
    for rand in order_urbanization:
        candidate_cells_1d = candidate_cells.reshape(lig*col).copy()
        growth_cells = np.where(candidate_cells_1d==rand)[0]
        rand_index = np.random.choice(growth_cells)
        x,y = index_double[rand_index]
        new_urb[i] = rand_index
        ini_urb[len(ini_urb)] = rand_index
        candidate_cells[x,y] = 255
        adj_cells = candidate_cells[x-distance:x+distance+1,y-distance:y+distance+1].copy().reshape((2*distance+1)**2)
        
        if rand==1:
            new_val =  np.array(list(map(lambda x: 1 if x not in [0,255] else x , adj_cells))).reshape(2*distance+1,2*distance+1)
            candidate_cells[x-distance:x+distance+1,y-distance:y+distance+1] = new_val

        elif rand==2:
            new_val =  np.array(list(map(lambda x: 1 if x not in [0,255] else x , adj_cells))).reshape(2*distance+1,2*distance+1)
            candidate_cells[x-distance:x+distance+1,y-distance:y+distance+1] = new_val

            possib = [col*a + b  for a in range(x-distance,x+distance+1) for b in range(y-distance,y+distance+1) if (a,b)!=(x,y)]
            for val in possib:
                if len(np.where(ini_urb==val))>0:
                    x,y = index_double[val]
                    adj_cells_old = candidate_cells[x-distance:x+distance+1,y-distance:y+distance+1].copy().reshape((2*distance+1)**2)          
                    new_val =  np.array(list(map(lambda x: 1 if x not in [0,255] else x , adj_cells_old))).reshape(2*distance+1,2*distance+1)
                    candidate_cells[x-distance:x+distance+1,y-distance:y+distance+1] = new_val

        elif rand==3:
            if np.sum(adj_cells)==255:
                adj_cells = candidate_cells[x-1:x+2,y-1:y+2].copy().reshape(9)
                new_val =  np.array(list(map(lambda x: 2 if x not in [0,3,255] else x , adj_cells))).reshape(3,3)
                candidate_cells[x-1:x+2,y-1:y+2] = new_val

        else:
            adj_cells = candidate_cells[x-1:x+2,y-1:y+2].copy().reshape(9)
            new_val =  np.array(list(map(lambda x: 2 if x not in [0,3,255] else x , adj_cells))).reshape(3,3)
            candidate_cells[x-1:x+2,y-1:y+2] = new_val 

        candidate_cells_bis = candidate_cells.copy().reshape(lig*col)
        candidate_cells_bis[index_exclu_1d_arr] = 0
        candidate_cells = candidate_cells_bis.reshape((lig,col)).copy()
        i = i + 1
    output = new_urb.copy()
    return output


@njit
def simulation_numba_prio(candidate_cells,ini_urb,order_urbanization,distance,index_exclu_1d_arr,index_double,number_urban_cells):
    """
    Given a raster of urbanisation data and a list of coordinates
    return all coordinates of non urban areas in a square of size "dist" around the list of coordinates
    
    Args:
        *candidate_cells* : A numpy array of cells corresponding to each type of growth
            
        *ini_urb* : A numpy array of urbanization data
        
        *order_urbanization* : A numpy array giving the order of urbanization among the 4 types of growth

        *dist* : Distance around list_coord where we look for non urban areas. Dist=1 means we are looking for non urban cells within a buffer of 1 cell (total of 8 cells checked)

        *index_exclu_1d_arr* : Index of cells excluded from Urbanization

        *index_double* : Array of tuples for the area

        *number_urban_cells* : Numpy Array counting the number of urban areas around each edge growth cells
        
    Return:
        *new_urb*: list of indexes of new urban cells.
    """
    new_urb = np.zeros(len(order_urbanization),dtype=np.int64)
    lig,col = candidate_cells.shape
    i = 0
    for rand in order_urbanization:
        number_urban_cells[index_exclu_1d_arr] = 0
        if rand==1:
            max_index_uni = np.random.choice(np.flatnonzero(number_urban_cells == number_urban_cells.max()))
            number_urban_cells[max_index_uni] = 0
            x,y = index_double[max_index_uni]
            candidate_cells[x,y] = 255
            new_urb[i] = max_index_uni
#             ini_urb[len(ini_urb)] = max_index_uni
            ini_urb = np.append(ini_urb,max_index_uni)
            
            adj_cells = candidate_cells[x-distance:x+distance+1,y-distance:y+distance+1].copy().reshape((2*distance+1)**2)

            new_val =  np.array(list(map(lambda x: 1 if x not in [0,255] else x , adj_cells))).reshape(2*distance+1,2*distance+1)
            candidate_cells[x-distance:x+distance+1,y-distance:y+distance+1] = new_val
            
            possib = np.array([col * a + b for a in range(x-distance,x+distance+1) for b in range(y-distance,y+distance+1) if ((candidate_cells[(a,b)]!=0)&(candidate_cells[(a,b)]!=255))])
            number_urban_cells[possib] = number_urban_cells[possib] + 1         

        else:
                
            candidate_cells_1d = candidate_cells.reshape(lig*col).copy()
            growth_cells = np.where(candidate_cells_1d==rand)[0]
            rand_index = np.random.choice(growth_cells)
            x,y = index_double[rand_index]

            new_urb[i] = rand_index
#             ini_urb[len(ini_urb)] = rand_index
            ini_urb = np.append(ini_urb,rand_index)
            number_urban_cells[rand_index] = 0
            candidate_cells[x,y] = 255
            adj_cells = candidate_cells[x-distance:x+distance+1,y-distance:y+distance+1].copy().reshape((2*distance+1)**2)

            if rand==2:
                new_val =  np.array(list(map(lambda x: 1 if x not in [0,255] else x , adj_cells))).reshape(2*distance+1,2*distance+1)
                candidate_cells[x-distance:x+distance+1,y-distance:y+distance+1] = new_val
            
                urban_cells_index = np.array([col * a + b   for a in range(x-distance,x+distance+1) for b in range(y-distance,y+distance+1)  if ((candidate_cells[(a,b)]!=0)&(candidate_cells[(a,b)]!=255))])
                number_urban_cells[urban_cells_index] = number_urban_cells[urban_cells_index] + 1

                possib = np.array([col * a + b  for a in range(x-distance,x+distance+1) for b in range(y-distance,y+distance+1) if (a,b)!=(x,y)])
                for val in possib:
                    if len(np.where(ini_urb==val))>0:
                        x,y = index_double[val]
                        adj_cells_old = candidate_cells[x-distance:x+distance+1,y-distance:y+distance+1].copy().reshape((2*distance+1)**2)          
                        new_val =  np.array(list(map(lambda x: 1 if x not in [0,255] else x , adj_cells_old))).reshape(2*distance+1,2*distance+1)
                        candidate_cells[x-distance:x+distance+1,y-distance:y+distance+1] = new_val
                        
            elif rand==3:
    #             new_road.extend([(x,y)])
                if np.sum(adj_cells)==255:
                    adj_cells = candidate_cells[x-1:x+2,y-1:y+2].copy().reshape(9)
                    new_val =  np.array(list(map(lambda x: 2 if x not in [0,3,255] else x , adj_cells))).reshape(3,3)
                    candidate_cells[x-1:x+2,y-1:y+2] = new_val

            else:
    #             new_spont.extend([(x,y)])
                adj_cells = candidate_cells[x-1:x+2,y-1:y+2].copy().reshape(9)
                new_val =  np.array(list(map(lambda x: 2 if x not in [0,3,255] else x , adj_cells))).reshape(3,3)
                candidate_cells[x-1:x+2,y-1:y+2] = new_val 

        candidate_cells_bis = candidate_cells.copy().reshape(lig*col)
        candidate_cells_bis[index_exclu_1d_arr]=0
        candidate_cells = candidate_cells_bis.reshape((lig,col)).copy()
        i = i + 1
        
    output = new_urb.copy()
    return output