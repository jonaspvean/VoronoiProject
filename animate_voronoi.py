
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.spatial import voronoi_plot_2d

from compute_voronoi import *
from setup import image_setup


# need to update the points using the lerp_points function and use these points to recalculate the Voronoi diagram

def animate(image, showVorPlot = True):
    # Initialize the plot elements
    fig, ax = plt.subplots()
    sharedProps = {"xticks": [], "yticks": [], "xlim": (0, image.size[0]), "ylim": (0, image.size[1])}

    def update(frame):
        '''
        For each frame, update the data stored on each artist accordingly. 
        '''
        print(frame)
        if frame==0:
            points = image_setup(image, resolution = 10000)
        ax.clear()
        
        def calculatePoints(points: np.ndarray):
            vor, filtered_points, residual_points, centroids = voronoiScheme(points)
            new_points = lerp_points(residual_points, filtered_points, centroids, 0.1)
            return vor, new_points
        
        vor, new_points = calculatePoints(points)
        if (showVorPlot):
            voronoi_plot_2d(vor, ax, point_size = 1, show_vertices = False)
        ax.plot(new_points[:,0], new_points[:,1], 'o', color='black', markersize=2)
        ax.update(sharedProps)


    ani = animation.FuncAnimation(fig, update, frames = 40, interval = 200, fargs=[])
    ani.save('output/voronoi_animation.mp4', writer="imagemagick", fps=5, bitrate=-1)




