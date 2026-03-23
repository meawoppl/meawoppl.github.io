---
title: "Pycuda Fun!"
date: 2009-06-15 12:00:00 +0000
---

*Originally published on [craneium.net](https://web.archive.org/web/20160315095018/http://craneium.net/)*

I recently built myself a shiny new computer equipped with a NVIDIA 260 at least partly to indulge in the occasional video game, but moreover for its CUDA abilities. Until a couple of weeks ago, I was under the impression that I was going to have to brush up my C/C++ skills, but thanks to a nice fellow named Andreas Klockner, I was able to inline some CUDA code into Python very elegantly.

Though the particular package (called pycuda), is exceptionally well developed, it however does not allow you to escape understanding the GPU architecture and computing strategy underlying everything. Correspondingly, I will talk a little about everything. So without further ado, here is the first program I wrote with Python and CUDA working together:

```python
from scipy import *
from scipy import misc
from pylab import *
import pycuda.autoinit
import pycuda.driver as drv
import time

mod = drv.SourceModule("""
__global__ void julia_iterate(float *a, float *b, float *max_iter)
{
    const int i = blockIdx.x * blockDim.x + threadIdx.x;
    float bounds = 16.0;
    for(int iter = 0; iter < max_iter[i]; iter++)
    {
        float new_a = (a[i] * a[i]) - (b[i] * b[i]) +.6;
        float new_b = (2 * a[i] * b[i])  - .2;
        a[i] = new_a;
        b[i] = new_b;
        if(abs((a[i]*a[i])+(b[i]*b[i])) > bounds)
        {
            max_iter[i] = iter;
            break;
        }
    }
}

__global__ void mandelbrot_iterate(float *a, float *b, float *max_iter)
{
    const int i = blockIdx.x * blockDim.x + threadIdx.x;
    float bounds = 16.0;
    float ai = 0;
    float bi = 0;
    for(int iter = 0; iter < max_iter[i]; iter++)
    {
        float new_a = (ai * ai) - (bi * bi) + a[i];
        float new_b = (2 * ai * bi)  + b[i];
        ai = new_a;
        bi = new_b;
        if(abs((ai*ai)+(bi*bi)) > bounds)
        {
            max_iter[i] = iter;
            break;
        }
    }
}
""")

mb = mod.get_function("mandelbrot_iterate")

shape = (5000, 5000)
pxls = shape[0] * shape[1]

x, y = mgrid[-2:1:shape[0]*1j,-1:1:shape[1]*1j]
x = x.astype(float32)
y = y.astype(float32)
x = x.flatten()
y = y.flatten()

itr = ones_like(x) * 3000

start_time = time.time()
mb(drv.In(x), drv.In(y), drv.InOut(itr), block=(500,1,1), grid=(50000,1))
print "CUDA iteration time:", time.time() - start_time

itr = itr.reshape(shape)
itr = log(itr)
misc.imsave("test.png", itr.T)
```

The names of the CUDA functions are a bit of a giveaway to the final punch-image, but this is code for generating Mandelbrot fractals. (A Julia example is in there too, but is unused for now) What is wonderful about CUDA that thanks to its incredible paralellism, it takes more time to write the image to disk than it does for the actual computation!

On my NVIDIA 260 it took 1.8 seconds to do 3000 iterations on 25,000,000 points! The super computer is personal again.

![Mandelbrot fractal generated with CUDA](/images/craneium/pycuda/cuda-fract.png)

[click for the full size image!]

The code above actually outputs a 5000x5000 ".png" So lets go through this all step by step to give some idea of how this all works.

First we are going to import all the various important libraries.

```python
from scipy import *
from scipy import misc
from pylab import *
import pycuda.autoinit
import pycuda.driver as drv
import time
```

Note that,

```python
import pycuda.autoinit
```

automatically initializes (and checks for the proper setup) of your CUDA device. There is typically code that goes into accomplishing this, so just having things setup on import is very handy. While there are provisions in pycuda to do the initialization with more control over the process, they will not be covered here. If you have more than one CUDA device, or certain SLI configurations using the autoinit import feature may not be the best choice. If you don't know what this means, it likely will not affect you.

Next up we come to the actual CUDA/C code that we are going to run on the GPU. I am assuming a fair bit of knowledge here about the C programming language, particularly pointers, indexing, etc, but if you don't already know about these things, they are worth learning! You can find some catchup links here.

And with that, on to the big block:

```python
mod = drv.SourceModule("""
__global__ void julia_iterate(float *a, float *b, float *max_iter)
{
    const int i = blockIdx.x * blockDim.x + threadIdx.x;
    float bounds = 16.0;
    for(int iter = 0; iter < max_iter[i]; iter++)
    {
        float new_a = (a[i] * a[i]) - (b[i] * b[i]) +.6;
        float new_b = (2 * a[i] * b[i])  - .2;
        a[i] = new_a;
        b[i] = new_b;
        if(abs((a[i]*a[i])+(b[i]*b[i])) > bounds)
        {
            max_iter[i] = iter;
            break;
        }
    }
}

__global__ void mandelbrot_iterate(float *a, float *b, float *max_iter)
{
    const int i = blockIdx.x * blockDim.x + threadIdx.x;
    float bounds = 16.0;
    float ai = 0;
    float bi = 0;
    for(int iter = 0; iter < max_iter[i]; iter++)
    {
        float new_a = (ai * ai) - (bi * bi) + a[i];
        float new_b = (2 * ai * bi)  + b[i];
        ai = new_a;
        bi = new_b;
        if(abs((ai*ai)+(bi*bi)) > bounds)
        {
            max_iter[i] = iter;
            break;
        }
    }
}
""")
```

The above code will compile the entire code string into a module accessible by pycuda. Pycuda ties the lifetime of objects on the GPU the the life of objects in the Python environment.

At the end of execution, all the GPU resident objects are cleaned up and deallocated appropriately. Correspondingly, if you want to remove something from the GPU you can simply delete the associated objects and cleanup will happen automagically. We will see this again in the "drv.In"/"drv.Out" objects.

Now its time to talk about some CUDA features that are worth understanding. There are two in particular that are worth note in this example:

1.) The "\_\_global\_\_" keyword. This is a directive that tells the CUDA compiler that this function is accessible from both the standard CPU and GPU realm of things. We use it for a function that we want to have a handle on from outside the GPU context (like through pycuda).

2.) This line

```c
const int i = blockIdx.x * blockDim.x + threadIdx.x;
```

contains several variables that appear undefined. They are not defined in the normal C sense, but are special CUDA objects defined in context which they are run.

At this point we need to talk a little bit about the CUDA threading structure. Coming from a largely interpreted language background, this was a bit difficult for me. CUDA is ideally suited to the single operation, multiple data paradigm. Thusly it is _very_ good at things like fractals where you need to perform the same operation over and over on a single data set. So, you need to conceptually break down your operation into single action that is performed on any number of data pieces.

There is two levels of threaded-ness in CUDA:

1.) Operations that can occur in any order/concurrently within a single ALU

2.) The chunks which will be slit apart to and sent to different ALU's which also occur in any order/concurrently.

These are referred to in the NVIDIA CUDA documentation (with excellent diagrams) as threads at the lowest level. These threads are grouped into "blocks" of threads. These "blocks" are organized in a Cartesian grouping referred to as a "grid". (Illustrated on pdf page 16 of here) Being a modeling guy, I tend to think of this as an actual Cartesian organization of shapes. This particular example I imagine as as a vector of vectors (some number of vectors glued end to end).

So within your function, there is a way to identify your thread number, the size of your block, and what block number you are in. This is accomplished by the following three internal variables respectively:

threadIdx

blockDim

blockIdx

Each of these is a structure containing variables pertaining to its dimensionality. In our example, we have both mono-dimensional blocks, and and a mono-dimensional grid. Correspondingly, based off of simple geometric calculations

```c
const int i = blockIdx.x * blockDim.x + threadIdx.x;
```

Will store in the variable "i", the correct index that needs to be processed by a particular thread in a particular block. For example, the zeroth thread in the zeroth block will operate on the zeroth array index. Or the zeroth thread in the first block will be offset by the one times the block dimension. This gets a bit more complicated for multidimensional arrays, so we will stick to 1-d for this example. More complex examples are seen in the CUDA documentation mentioned earlier. But really it boils down to a function of:

threadIdx(.x / .y / .z)

blockDim(.x / .y)

blockIdx(.x / .y)

Derived from geometry of the arrays. The remainder of the code within that Python text block is industry standard C to generate either a Mandelbrot or Julia fractal. Alright, back to Python!

Next we get a handle to the actual function on the GPU with: `mb = mod.get_function("mandelbrot_iterate")`

"mb" is now an object which is callable within our Python code to execute the function we have described! Were getting there!! Next we are going to generate a pair of vectors which are the real and imaginary component corresponding to all the points withing the interesting area of the Mandelbrot set.

We want a 5000x5000 grid so:

```python
shape = (5000, 5000)
pxls = shape[0] * shape[1]
x, y = mgrid[-2:1:shape[0]*1j,-1:1:shape[1]*1j]
```

Next, we use the scipy function "mgrid" to generate the indices, convert them to float32 (to match the precision of NVIDIA GPU's), then flatten them into linear vectors. We also define a linear vector of how many iterations we will maximally perform on each point. NB: All of these vectors are the same length!

```python
x, y = mgrid[-2:1:shape[0]*1j,-1:1:shape[1]*1j]
x = x.astype(float32)
y = y.astype(float32)
x = x.flatten()
y = y.flatten()
itr = ones_like(x) * 3000
```

If you want to play with zooming, the other values in the mgrid statement deal with the bounds of interest.

Now we call the actual function that performs the calculations. While doing this, several objects are instantiated by "drv.In" and "drv.InOut". These objects correspond to arrays of data that are resident on the GPU. Notably also, their lifetime on the GPU is tied to their lifetime in the Python interpretor environment. Therefore, instantiating them allocates their memory space on the GPU and copies the ndarray over. Also, when the object is destroyed at the end of the statement, the memory is deallocated, and cleaned up appropriately on the GPU itself.

```python
start_time = time.time()
mb(drv.In(x), drv.In(y), drv.InOut(itr), block=(500,1,1), grid=(50000,1))
print "CUDA iteration time:", time.time() - start_time
```

The difference between "drv.In", "drv.Out", and "drv.InOut" is fairly obvious, but using them appropriately insures that time is not wasted copying back and forth unnecessarily.

In here we specify the geometry of our blocks and the grid. (Note that 500\*50,000 is our pixel count) These are hard coded in this example, but it is easy to imagine juggling these around to fit the size of the problem. Notably, the dimensions of both the grid size and block size are bounded, however allow some _very_ large numbers. There is some dark voojoo in the optimization of these variables to get the best speed out of your operation. Read through the CUDA documentation if you want to know more!

Last up, we reshape the data back into the 2-d ndarray in scipy. I chose to log scale the coloring because it brings out the iteration difference nearest the edges for nice contrast. Then we output a .png of the image! (Using the ".T" orients the axes in those more familiar to us.)

```python
itr = itr.reshape(shape)
itr = log(itr)
misc.imsave("test.png", itr.T)
```

Depending on the versions of python "misc.imsave" may or may not work for you (and will likely take longer than the fractal iterations!). You can also use "imshow()" and "savefig()" from matplotlib, but this has boarders or figure formatting you would have to kill to get a pure image. The matplotlib colormap of 'winter' ("cm.winter") looks very nice with this particular view, but play around! There is a lot of neat visualization fun you can have here! I love playing with the alpha channel that PIL extends you (another part of scipy). One last closing note (to my DoD buddies who have tirelessly gotten numpy cleared for secret lab use) is that pycuda is not dependent on scipy, only numpy (which scipy sits atop), so you should be able to manage all of this without the heady overhead of scipy if you so desire!

Comments, concerns, and critiques all welcome! I am new to this whole thing and wanted to put together a more detailed example than those available with the pycuda documentation! This in particular show you how to attack problems larger than one block size. Next up, I am going to write a SOR solver with pycuda, so check back if that is something you have interest in!
