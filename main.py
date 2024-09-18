import os
import numpy as np 
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay, Voronoi, voronoi_plot_2d
import matplotlib.animation as animation
from PIL import Image
import pathlib

# changes the working directory to the correct folder
# the 'r' converts the string to a raw string 
os.chdir(r'C:\Users\jonas\Python Projects in VSCode')


#width = 200
#height = 200
resolution = 10000


t = np.linspace(0,3,40)

# the random.seed() method ensures reproducibility of one particular example

np.random.seed(40)


image = Image.open(pathlib.Path('dog_test_image.jpg'))

def image_setup(image, resolution):
    # uses an image to choose the points that will later be used in the Voronoi diagram
    # the naive way here is to go by pixel brightness
    width, height = image.size 
    points = []
    for i in range(0, resolution):
        x = np.random.randint(1, width)
        y = np.random.randint(1, height)
        pixel = image.getpixel((x,y))
        R, G, B = pixel
        brightness = ((0.2126*R) + (0.7152*G) + (0.0722*B))/255
        if brightness < 0.5:
            points.append([x,y])
    # we add distant points that are outside of the canvas
    points.append([-width*3, -height*3])
    points.append([-width*3, height*4])
    points.append([width*4, -height*3])
    points.append([width*4, height*4])
    return np.asarray(points)

def rand_setup(width, height, resolution): 
    # randomizes points with integer values on a (width x height) bounding box
    points = []
    for i in range(0, resolution):
        points.append([np.random.randint(1, width), np.random.randint(1, height)])
    # we add distant points that are outside of the canvas
    points.append([-width*3, -height*3])
    points.append([-width*3, height*4])
    points.append([width*4, -height*3])
    points.append([width*4, height*4])
    return np.asarray(points)

def centroid(vertices):
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

def voronoiScheme(points):
    # compute the Voronoi tesselation
    vor = Voronoi(points[:])
    
    # compute the applicable regions associated with the above Voronoi diagram
    # indices -1 in the region need to be discarded as they are outside the bounding box
    # additionally, we need to keep track of which points are being removed from the regions we do not discard

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
        region_centroid = centroid(vertices)
        centroids.append(region_centroid)
    centroids = np.asarray(centroids)
    return vor, filtered_points, residual_points, centroids

def lerp_points(residual_points, filtered_points, centroids, t):
    # lerp the filtered initial points towards the centroids
    # we make our own function for this as numpy and scipy decided not to cooperate
    new_points = []
    for filtered_point, centroid in zip(filtered_points, centroids):
        interp = np.multiply((1-t), filtered_point) + np.multiply(t, centroid)
        new_points.append(interp)
    for point in residual_points:
        new_points.append(point)
    return np.asarray(new_points)


#points = rand_setup(width, height, resolution)
points = image_setup(image, resolution)




# for each frame, update the data stored on each artist
# need to update the points using the lerp_points function and use these points to recalculate the Voronoi diagram

#fig, ax = plt.subplots()

"""
def update(points):
    ax.set_xlim([0, width])
    ax.set_ylim([0, height])
    vor, filtered_points, residual_points, centroids = voronoiScheme(points)
    new_points = lerp_points(residual_points, filtered_points, centroids, 0.1)
    ax.plot(points[:,0], points[:,1], 'o', color = 'black', markersize = 1)
    ax.plot(new_points[:,0], new_points[:,1], 'o', color = 'red', markersize = 2)
    points = new_points 
"""    

"""
ims = []
for i in range(10):
    vor, filtered_points, residual_points, centroids = voronoiScheme(points)
    new_points = lerp_points(residual_points, filtered_points, centroids, 0.1)
    im = voronoi_plot_2d(vor, point_size = 1, show_vertices = False)
    ax.plot(points[:,0], points[:,1], 'o', color = 'black', markersize = 1)
    ax.plot(new_points[:,0], new_points[:,1], 'o', color = 'red', markersize = 2)
    points = new_points 
    ims.append([im])
"""

for i in range(0,30):
    vor, filtered_points, residual_points, centroids = voronoiScheme(points)
    new_points = lerp_points(residual_points, filtered_points, centroids, 0.1)
    points = new_points


vor, filtered_points, residual_points, centroids = voronoiScheme(points)
new_points = lerp_points(residual_points, filtered_points, centroids, 0.1)
fig = voronoi_plot_2d(vor, point_size = 1, show_vertices = False)
plt.plot(points[:,0], points[:,1], 'o', color = 'black', markersize = 1)
plt.plot(new_points[:,0], new_points[:,1], 'o', color = 'red', markersize = 2)
#tri = Delaunay(points[:,0])
#plt.triplot(points[:,0,0], points[:,0,1], tri.simplices)
#plt.plot(centroids[:,0], centroids[:,1], 'x', color = 'green', markersize = 2)
plt.xlim(0, image.size[0])
print(image.size[0])
plt.ylim(0, image.size[1])
plt.xticks([])
plt.yticks([])
plt.show()
points = new_points


# the animation part of the code:

