from fastai.vision import *
import random
import numpy as np
import matplotlib.pyplot as plt
#from pyts.image import GramianAngularField
#from pyts.image import GASF, GADF
from pyts.image import gaf
import pandas as pd
# Math
import math
import numpy as np
from datetime import datetime, timedelta
import scipy

bs = 64
n_classes = 3
n_samples = 28

def tabulate(x, y, f):
    """Return a table of f(x, y). Useful for the Gram-like operations."""
    return np.vectorize(f)(*np.meshgrid(x, y, sparse=True))
def cos_sum(a, b):
    """To work with tabulate."""
    return(math.cos(a+b))

class GAF:

    def __init__(self):
        pass
    def __call__(self, serie):
        """Compute the Gramian Angular Field of an image"""
        # Min-Max scaling
        min_ = np.amin(serie)
        max_ = np.amax(serie)
        scaled_serie = (2*serie - max_ - min_)/(max_ - min_)

        # Floating point inaccuracy!
        scaled_serie = np.where(scaled_serie >= 1., 1., scaled_serie)
        scaled_serie = np.where(scaled_serie <= -1., -1., scaled_serie)

        # Polar encoding
        phi = np.arccos(scaled_serie)
        # Note! The computation of r is not necessary
        r = np.linspace(0, 1, len(scaled_serie))

        # GAF Computation (every term of the matrix)
        gaf = tabulate(phi, phi, cos_sum)

        return(gaf, phi, r, scaled_serie)





def begin():
        while 1:
            points = []
            for i in range(20):
                points.append(random.uniform(-1, 1))


            X = np.linspace(0, 1, num=n_samples) ** 2
            Y = [-1.0, -0.5169489478597231, -0.27118697931651753, -0.39830567724816807, -0.21186576773973353, -0.11016996193642421, 0.06779536770990188, 0.025423315857337772, -0.4915269031893659, -0.5762710068944942, -0.279662406636613, -0.07627248994597155, 0.5593209997122872, 0.8389821351619227, 1.0, 1.0, 0.8728813020683495, 0.8559321423441296, 0.864406722206238, 0.593220166618717]

            gaf = GAF()
            print(Y)
            g, _, _, _ = gaf(Y)
            plt.figure(figsize=(16, 8))
            plt.subplot(121)
            plt.plot(Y)
            plt.title("Original", fontsize=16)
            plt.subplot(122)
            plt.axis('off')
            plt.imshow(g, cmap='rainbow', origin='lower')
            plt.title("GAF", fontsize=16)
            plt.show()
            points.clear()
            plt.close()

begin()