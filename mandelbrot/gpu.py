import numpy as np
from numba import jit, cuda, uint32, f8, uint8
from pylab import imshow, show
from timeit import default_timer as timer

@jit
def mandel(x, y, max_iters):
    c = complex(x, y)
    z = 0.0j
    for i in range(max_iters):
        z = z*z + c 
        if (x.real*x.real + z.imag*z.imag) >= 4:
            return i

    return max_iters

# Gpu compatible mandel function created using cuda.jit
mandel_gpu = cuda.jit((f8, f8, uint32), device=True)(mandel)

@cuda.jit((f8, f8, f8, f8, uint8[:,:], uint32))
def mandel_kernel(min_x, max_x, min_y, max_y, image, iters):
    height = image.shape[0]
    width = image.shape[1]

    pixel_size_x = (max_x - min_x) / width
    pixel_size_y = (max_y - min_y) / height

    startX, startY = cuda.grid(2)
    gridX = cuda.gridDim.x * cuda.blockDim.x
    gridY = cuda.gridDim.y * cuda.blockDim.y

    for x in range(startX, width, gridX):
        real = min_x + x * pixel_size_x
        for y in range(startY, height, gridY):
            imag = min_y + y * pixel_size_y
            image[y, x] = mandel_gpu(real, imag, iters)

def create_fractal_gpu(min_x, max_x, min_y, max_y, image, iters):
    # Allocate GPU memory for image
    d_image = cuda.to_device(image)

    # Define number of threads and blocks for GPU parallelization
    threadsperblock = (16, 16)
    blockspergrid_x = int(np.ceil(image.shape[1] / threadsperblock[0]))
    blockspergrid_y = int(np.ceil(image.shape[0] / threadsperblock[1]))
    blockspergrid = (blockspergrid_x, blockspergrid_y)

    start = timer()

    # Launch the gpu kernel (mandel_kernel)
    mandel_kernel[blockspergrid, threadsperblock](min_x, max_x, min_y, max_y, d_image, iters)

    # wait for GPU to finish
    cuda.synchronize()

    # Measure the GPU processing time
    dt = timer() - start

    # GPU to CPU
    d_image.copy_to_host(image)

    # Display mandelbrot set image
    print("Mandelbrot created on GPU in %f s" % dt)
    imshow(image)
    show()

image = np.zeros((1024, 1536), dtype=np.uint8)

create_fractal_gpu(-2.0, 1.0, -1.0, 1.0, image, 20)



