import matplotlib
from matplotlib import pyplot as plt
import numpy as np
from pylab import imshow, show
from timeit import default_timer as timer

matplotlib.use('GTK')

def mandel(x, y, max_iters):
    c = complex(x, y)
    z = 0.0j
    # Iterate to check if a point is in the Mandelbrot set
    for i in range(max_iters):
        z = z*z + c
        if (x.real*z.real + z.imag*z.imag) >= 4:
            return i
    return max_iters

def create_fractal(min_x, max_x, min_y, max_y, image, iters):
    height = image.shape[0]
    width = image.shape[1]

    # Calculate pixel sizes based on the specified region
    pixel_size_x = (max_x - min_x) / width
    pixel_size_y = (max_y - min_y) / height

    # Calculate mandelbrot value for each px
    for x in range(width):
        real = min_x + x * pixel_size_x
        for y in range(height):
            imag = min_y + y * pixel_size_y
            color = mandel(real, imag, iters)
            image[y, x] = color

image = np.zeros((1024, 1536), dtype=np.uint8)

start = timer()

create_fractal(-2.0, 1.0, -1.0, 1.0, image, 20)

dt = timer() - start

print("Mandelbrot created in %f s" % dt)

imshow(image)
show()
