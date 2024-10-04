import numpy as np

'''
This script initializes the canvas used for computing the Voronoi scheme.
'''

def rand_setup(width: int, height: int, resolution: int):
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


def image_setup(image, resolution: int):
    # setup based on input image 
    width, height = image.size
    points = []
    for i in range(0, resolution):
        x = np.random.randint(1, width)
        y = np.random.randint(1, height)
        pixel = image.getpixel((x,y))
        R, G, B = pixel
        brightness = ((0.2126*R) + (0.7152*G) + (0.0722*B))/255
        if brightness < 0.3:
            points.append([x,y])
    # we add distant points that are outside of the canvas
    points.append([-width*3, -height*3])
    points.append([-width*3, height*4])
    points.append([width*4, -height*3])
    points.append([width*4, height*4])
    return np.asarray(points)



