import numpy as np
import pygame as pg

listlevel= np.array([np.loadtxt("prototype_Tile Layer 1.csv","int32",delimiter=","),
                     np.loadtxt("prototype_right_ramp.csv","int32",delimiter=","),
                     np.loadtxt("prototype_left_ramp.csv","int32",delimiter=",")])

width,height = 620, 360