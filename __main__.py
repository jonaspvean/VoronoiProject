import numpy as np 
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay, voronoi_plot_2d
from PIL import Image

from setup import *
from compute_voronoi import *
from animate_voronoi import *

image = Image.open(r'src/dog_test_image.jpg')


def plot(points, showDelaunay = False, showCentroids = False, showLerp = False):
    vor, filtered_points, residual_points, centroids = voronoiScheme(points)
    new_points = lerp_points(residual_points, filtered_points, centroids, 0.1)
    voronoi_plot_2d(vor, point_size = 1, show_vertices = False)
    plt.plot(points[:,0], points[:,1], 'o', color = 'black', markersize = 1)
    if (showLerp):
        plt.plot(new_points[:,0], new_points[:,1], 'o', color = 'red', markersize = 2)
    if (showDelaunay):
        tri = Delaunay(points[:,0])
        plt.triplot(points[:,0,0], points[:,0,1], tri.simplices)
    if (showCentroids):
        plt.plot(centroids[:,0], centroids[:,1], 'x', color = 'green', markersize = 2)
    plt.xlim(0, image.size[0])
    plt.ylim(0, image.size[1])
    plt.xticks([])
    plt.yticks([])
    plt.show()    


def main(setup_mode = 'rand_setup', *args, **kwargs):
    #points = rand_setup(width, height, resolution)
    np.random.seed(40)
    iterations = 30
    match setup_mode:
        case "image_setup":
            resolution = 10000
            points = image_setup(image, resolution)
        case "rand_setup":
            resolution = 100
            width = kwargs.get('width', 250)
            height = kwargs.get('height', 250)
            points = rand_setup(width, height, resolution)
    points = interpolateScheme(points, iterations)
    animate(image, showVorPlot = False)


if __name__ == "__main__":
    main('image_setup')

