import numpy as np

from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image

from keras.layers import Dropout, Flatten, Dense

from keras.applications import ResNet50
from keras.models import Model, Sequential
import os
import sys
import glob
import argparse
import matplotlib.pyplot as plt
from keras import __version__
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import SGD, Nadam
from keras.utils import plot_model

# Global Variables
PATH = 'data/birds/'
sz = 224
bs = 64

train_data_dir = f'{PATH}train'
val_data_dir = f'{PATH}valid'
