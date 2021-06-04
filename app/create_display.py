from PIL import Image
import os
import time
import cv2

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def tif_save_png(frompath, filename, topath, addtime = True):
    '''Saves tif image as a lossless png image.
    
    Parameters:
        frompath - Path of folder containing tif image file.
        filename - Filename of tif image file including extension.
        topath - Path of png destination folder.
        addtime (default = True) - Boolean option for appending global time variable to filename.
            Info: Appending time is needed to circumvent browser image caching.'''
    filepath = os.path.join(frompath, filename)
    im = Image.open(filepath)

    filename = os.path.splitext(filename)[0]
    if addtime == True:
        filename = str(time.time()) + filename

    new_filepath = os.path.join(topath, (filename + '.png'))

    im.save(new_filepath, 'PNG', compress_level = 0)

def png_save_png(frompath, filename, topath, addtime = True):
    '''Saves png image as a lossless png image.
    
    Parameters:
        frompath - Path of folder containing tif image file.
        filename - Filename of png image file including extension.
        topath - Path of png destination folder.
        addtime (default = True) - Boolean option for appending global time variable to filename.
            Info: Appending time is needed to circumvent browser image caching.'''
    filepath = os.path.join(frompath, filename)
    im = Image.open(filepath)

    filename = os.path.splitext(filename)[0]
    if addtime == True:
        filename = str(time.time()) + filename

    new_filepath = os.path.join(topath, (filename + '.png'))

    im.save(new_filepath, 'PNG', compress_level = 0)

def save_png(img_array, filename, topath, addtime = False):
    '''Saves numpy array object as a lossless png image.
    
    Parameters:
        img_array - Image array of target to be saved.
        filename - Filename of output png file.
        topath - Path of png destination folder.
        addtime (default = False) - Boolean option for appending global time variable to filename.
            Info: Appending time is needed to circumvent browser image caching.'''
    im = Image.fromarray(img_array)

    if addtime == True:
        filename = filename + str(time.time()) + '.png'

    new_filepath = os.path.join(topath, filename)

    im.save(new_filepath, 'PNG', compress_level = 0)
    #im.close()

def mask_image(img_array, mask):
    '''Masks image.
    
    Parameters:
        img_array - Numpy array image.
        mask - Numpy array mask.'''

    masked_image = cv2.bitwise_and(img_array, img_array, mask=mask)
    return masked_image

# Histogram display creation
def save_histogram(data_array, topath, xrange, bins=None, name=None):
    if bins:
        bins = int(bins)
    else:
        bins = int(10)
    
    if name:
        xlabel = str(name) + ' Pigmentation Score'
        title = 'Distribution of ' + str(name) + ' Pigmentation Score'
    else:
        xlabel = 'Pigmentation Score'
        title = 'Distribution of Pigmentation Score'
    
    plt.figure()
    plt.hist(data_array, bins=bins, range=xrange)
    plt.xlabel(xlabel)
    plt.ylabel('Frequency')
    plt.title(title)

    filename = 'hist' + str(time.time()) + '.png'
    filepath = os.path.join(topath, filename)

    plt.savefig(filepath)

    return(filename)


#def process_image()
