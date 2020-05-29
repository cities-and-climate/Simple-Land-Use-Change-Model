import numpy as np

def get_index_around_new_urb_prio(data,list_coord,dist=1):
    """Given a raster of urbanisation data and a list of coordinates
    return all coordinates of non urban areas in a square of size 1 around the list of coordinates
    """
    
    adj_cells = [data[x-dist:x+dist+1,y-dist:y+dist+1] for x,y in list_coord]
    val_index_0 = [np.where(adj==0) for adj in adj_cells]
    
    x_index = [val_index_0[i][0] + (x[0]-dist) for i,x in zip(list(range(len(val_index_0))),list_coord)]
    x_index = [item for sublist in x_index for item in sublist]
    
    y_index = [val_index_0[i][1] + (x[1]-dist) for i,x in zip(list(range(len(val_index_0))),list_coord)]
    y_index = [item for sublist in y_index for item in sublist]
    
    full_index = [(x_index[i],y_index[i]) for i in range(len(x_index))]
    return full_index

def create_edge_spread_poll_prio(data_urb,dict_double_uni,val_urb,dist):
    
    urb_index = np.where(data_urb==val_urb)

    urb_index = [(urb_index[0][i],urb_index[1][i]) for i in range(len(urb_index[0]))]
    
    adj_cells = [data_urb[x-1:x+2,y-1:y+2] for x,y in urb_index]
    
    spread_index = [ind for a,ind in zip(adj_cells,urb_index) if np.sum(a)==val_urb]
    edge_index = list(set(urb_index) - set(spread_index))
    
    spread_growth_cells = get_index_around_new_urb_prio(data_urb,spread_index,dist=1)
    spread_growth_cells = list(set(spread_growth_cells))
    
    edge_growth_cells = get_index_around_new_urb_prio(data_urb,edge_index,dist)
    
    full_index_uni = [dict_double_uni[x] for x in edge_growth_cells]

    index_uni = np.unique(full_index_uni,return_counts=True)
    
    number_urban_cells = np.zeros(data_urb.shape[0]*data_urb.shape[1])
    number_urban_cells[index_uni[0]] = index_uni[1]
    
    edge_growth_cells = list(set(edge_growth_cells) - set(spread_growth_cells))
    
    return edge_growth_cells,number_urban_cells,spread_growth_cells

def create_road_poll(data_road,data_urb,road_val,exclu_tuple,edge_growth_cells,spread_growth_cells):
    roads_index = np.where(data_road==road_val)
    roads_index = [(roads_index[0][i],roads_index[1][i]) for i in range(len(roads_index[0]))]
    road_growth_cells = get_index_around_new_urb_prio(data_urb,roads_index,dist=3)
    road_growth_cells = list(set(road_growth_cells))

    urb_index = np.where(data_road==255)
    urb_index = [(urb_index[0][i],urb_index[1][i]) for i in range(len(urb_index[0]))]
    
    road_growth_cells = list(set(road_growth_cells) - set(urb_index))
    road_growth_cells = list(set(road_growth_cells) - set(edge_growth_cells))
    road_growth_cells = list(set(road_growth_cells) - set(exclu_tuple))
    road_growth_cells = list(set(road_growth_cells) - set(spread_growth_cells))
    
    return road_growth_cells

def create_spont_poll(urb_ini,non_urb_val,edge_growth_cells,road_growth_cells,spread_growth_cells,index_outside_boundaries):

    spr_edge_road = edge_growth_cells.copy()
    spr_edge_road.extend(road_growth_cells)
    spr_edge_road.extend(spread_growth_cells)
    spr_edge_road.extend(index_outside_boundaries)

    spont_growth_cells = np.where(urb_ini==non_urb_val)
    spont_growth_cells = [(spont_growth_cells[0][i],spont_growth_cells[1][i]) for i in range(len(spont_growth_cells[0]))]
    spont_growth_cells = list(set(spont_growth_cells) - set(spr_edge_road))

    return spont_growth_cells

def tuple_to_double_arr(array1):
    return [a[0] for a in array1],[a[1] for a in array1]