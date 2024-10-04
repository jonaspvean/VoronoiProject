import numpy as np 
from scipy.spatial import Voronoi
from compute_centroids import computeCentroids


def voronoiScheme(points):
    '''
    USAGE: Calculate the Voronoi scheme based on the input points.
    
    Compute the applicable regions associated with the above Voronoi diagram
    indices -1 in the region need to be discarded as they are outside the bounding box
    additionally, we need to keep track of which points are being removed from the regions we do not discard
    '''
    vor = Voronoi(points[:])
    regions = []
    points_to_filter = []
    points_to_residue = []
    for i, region in enumerate(vor.regions):
        if not region:
            continue
        if -1 in region:
            points_to_residue.append(vor.points[vor.point_region == i][0,:])

        if -1 not in region:
            regions.append(region)
            points_to_filter.append(vor.points[vor.point_region == i][0,:])
        
    filtered_points = np.array(points_to_filter)
    residual_points = np.array(points_to_residue)
    vor.filtered_regions = regions 

    # compute the centroids
    centroids = []
    for i, region in enumerate(vor.filtered_regions):
        vertices = vor.vertices[region + [region[0]], :]
        region_centroid = computeCentroids(vertices)
        centroids.append(region_centroid)
    centroids = np.asarray(centroids)
    return vor, filtered_points, residual_points, centroids

def lerp_points(residual_points, filtered_points, centroids, t: float):
    '''
    Linearly interpolate the filtered initial points towards the centroids with interp parameter t.
    Made a dedicated function for this as numpy and scipy decided not to cooperate.
    The residual points should not be interpolated, so they are left alone.
    '''
    new_points = []
    for filtered_point, centroid in zip(filtered_points, centroids):
        interp = np.multiply((1-t), filtered_point) + np.multiply(t, centroid)
        new_points.append(interp)
    for point in residual_points:
        new_points.append(point)
    return np.asarray(new_points)


def interpolateScheme(points, iterations: int):
    for i in range(0, iterations):
        _, filtered_points, residual_points, centroids = voronoiScheme(points)
        new_points = lerp_points(residual_points, filtered_points, centroids, 0.1)
        points = new_points
    return points