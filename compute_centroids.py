import numpy as np

def computeCentroids(vertices):
    # calculates the centroid coordinates (C_x, C_y) of a 2-D polygon from its vertices
    # first, we initialize the area and coordinates 
    
    area = 0
    C_x = 0
    C_y = 0
    
    for i in range(0, len(vertices)-1):
        # produces the nested sum required for the total expression
        cross = vertices[i, 0] * vertices[i+1, 1] - vertices[i, 1] * vertices[i+1, 0]
        area = area + cross
        C_x = C_x + (vertices[i, 0] + vertices[i+1, 0]) * cross
        C_y = C_y + (vertices[i, 1] + vertices[i+1, 1]) * cross
    area = 0.5 * area
    C_x = (1.0 /(6.0 * area) ) * C_x 
    C_y = (1.0 /(6.0 * area) ) * C_y
    return np.array([C_x, C_y])

