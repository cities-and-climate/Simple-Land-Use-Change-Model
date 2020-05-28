import rasterio
import numpy as np
import random
import time
from numba import njit

@njit
def simulation_numba(urb_fin_new,ini_urb,order_urbanization,dist,index_exclu_1d_arr,index_uni,index_double):
    new_urb = np.zeros(len(order_urbanization),dtype=np.int64)
    lig,col = urb_fin_new.shape
    for rand in order_urbanization:
        urb_fin_new_1d = urb_fin_new.reshape(lig*col).copy()
        growth_cells = np.where(urb_fin_new_1d==rand)[0]
        rand_index = np.random.choice(growth_cells)
        x,y = index_double[rand_index]
        new_urb[i] = rand_index
#         new_urb.extend([rand_index])
        ini_urb[len(ini_urb)] = rand_index
#         ini_urb = np.append(ini_urb,rand_index)
        urb_fin_new[x,y] = 255
        adj_cells = urb_fin_new[x-dist:x+dist+1,y-dist:y+dist+1].copy().reshape((2*dist+1)**2)
        
        if rand==1:
            new_val =  np.array(list(map(lambda x: 1 if x not in [0,255] else x , adj_cells))).reshape(2*dist+1,2*dist+1)
            urb_fin_new[x-dist:x+dist+1,y-dist:y+dist+1] = new_val

        elif rand==2:
            new_val =  np.array(list(map(lambda x: 1 if x not in [0,255] else x , adj_cells))).reshape(2*dist+1,2*dist+1)
            urb_fin_new[x-dist:x+dist+1,y-dist:y+dist+1] = new_val

            possib = [col*a + b  for a in range(x-dist,x+dist+1) for b in range(y-dist,y+dist+1) if (a,b)!=(x,y)]
            for val in possib:
                if len(np.where(ini_urb==possib[0]))>0:
                    x,y = index_double[val]
                    adj_cells_old = urb_fin_new[x-dist:x+dist+1,y-dist:y+dist+1].copy().reshape((2*dist+1)**2)          
                    new_val =  np.array(list(map(lambda x: 1 if x not in [0,255] else x , adj_cells_old))).reshape(2*dist+1,2*dist+1)
                    urb_fin_new[x-dist:x+dist+1,y-dist:y+dist+1] = new_val

        elif rand==3:
            if np.sum(adj_cells)==255:
                adj_cells = urb_fin_new[x-1:x+2,y-1:y+2].copy().reshape(9)
                new_val =  np.array(list(map(lambda x: 2 if x not in [0,3,255] else x , adj_cells))).reshape(3,3)
                urb_fin_new[x-1:x+2,y-1:y+2] = new_val

        else:
            adj_cells = urb_fin_new[x-1:x+2,y-1:y+2].copy().reshape(9)
            new_val =  np.array(list(map(lambda x: 2 if x not in [0,3,255] else x , adj_cells))).reshape(3,3)
            urb_fin_new[x-1:x+2,y-1:y+2] = new_val 

        urb_fin_new_bis = urb_fin_new.copy().reshape(lig*col)
        urb_fin_new_bis[index_exclu_1d_arr] = 0
        urb_fin_new = urb_fin_new_bis.reshape((lig,col)).copy()
        
    return new_urb