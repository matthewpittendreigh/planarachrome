import numpy
from skimage.filters import threshold_otsu
import cv2
from PIL import Image


def quant_percentile(gimage, mask, percent=15):
    '''Quantify planarian based off of percentile of intesities.
    
    Parameters:
        gimage - Grayscale numpy array image of target for quantification.
        mask - Mask for gimage of same size.
        percent (default = 15) - Percentile at which to extract intensity quantification.'''
    roi = numpy.where((mask) != 0)
    percent_quant = numpy.percentile(gimage[roi], percent)

    return percent_quant


# maybe make it like max_otsu = {red = 130, green = 115, blue = 105}
def quant_area(cimage, mask, min_otsu=[120, 100, 55], max_otsu=[152, 140, 120]):
    '''Quantify planarian based off of area. Utilizes masked-otsu-color thresholding.

    Reference used for masked-otsu thresholding:
    https://stackoverflow.com/questions/56535330/otsu-thresholding-inside-mask
    Parameters:
        cimage - Color numpy array image of target for quantification.
        mask - Mask for cimage of same size.
        max_otsu (default = [152, 140, 120]) - Array length 3 containing maximum 
            red, green, blue otsu threshold values.
        min_otsu (default = [120, 100, 55]) - Array length 3 containing minimum 
            red, green, blue otsu threshold values.'''
    # Unsure why the masked.array method works like this at the moment.
    invert_mask = 1-mask   

    red = cimage[:, :, 0]
    red_masked = numpy.ma.masked_array(red, invert_mask)
    red_otsu_val = threshold_otsu(red_masked.compressed())
    if(red_otsu_val > max_otsu[0]):
        red_otsu_val = max_otsu[0]
    elif(red_otsu_val < min_otsu[0]):
        red_otsu_val = min_otsu[0]
    print(red_otsu_val)
    _, red_thresh = cv2.threshold(
        red, red_otsu_val, 255, cv2.THRESH_BINARY_INV)
    red_pigment = cv2.bitwise_and(red_thresh, red_thresh, mask=mask)

    green = cimage[:, :, 1]
    green_masked = numpy.ma.masked_array(green, invert_mask)
    green_otsu_val = threshold_otsu(green_masked.compressed())
    if(green_otsu_val > max_otsu[1]):
        green_otsu_val = max_otsu[1]
    elif(green_otsu_val < min_otsu[1]):
        green_otsu_val = min_otsu[1]
    print(green_otsu_val)
    _, green_thresh = cv2.threshold(
        green, green_otsu_val, 255, cv2.THRESH_BINARY_INV)
    green_pigment = cv2.bitwise_and(green_thresh, green_thresh, mask=mask)

    blue = cimage[:, :, 2]
    blue_masked = numpy.ma.masked_array(blue, invert_mask)
    blue_otsu_val = threshold_otsu(blue_masked.compressed())
    if(blue_otsu_val > max_otsu[2]):
        blue_otsu_val = max_otsu[2]
    elif(blue_otsu_val < min_otsu[2]):
        blue_otsu_val = min_otsu[2]
    print(blue_otsu_val)
    _, blue_thresh = cv2.threshold(
        blue, blue_otsu_val, 255, cv2.THRESH_BINARY_INV)
    blue_pigment = cv2.bitwise_and(blue_thresh, blue_thresh, mask=mask)

    redgreen = cv2.bitwise_and(red_pigment, green_pigment, mask=None)
    greenblue = cv2.bitwise_and(green_pigment, blue_pigment, mask=None)
    bluered = cv2.bitwise_and(blue_pigment, red_pigment, mask=None)
    rggb = cv2.bitwise_or(redgreen, greenblue, mask=None)
    rggbbr = cv2.bitwise_or(rggb, bluered, mask=mask)

    den = len(numpy.where(mask != 0)[0])
    num = len(numpy.where(rggbbr != 0)[0])
    area_ratio = num/den

    return area_ratio, red_pigment, green_pigment, blue_pigment, rggbbr


def quant_pigment(percent_quant, area_quant):
    '''Combine percentile and area based quanitfication.
    
    Method divides percentile quanitification by colorspace of 255 to fit within range [0,1].
    It is then subtracted from 1 to positively correlate with area quantification.
    Parameters:
        percent_quant - Percentile based quantification of target.
        area_quant - Area based quantification of target.'''
    # Scale percentile quantification and invert via subtraction
    adjusted_percent_quant = 1 - (percent_quant/255)

    # Average values of percentile quantificaiton and area quantification
    pigment_quant = (area_quant + adjusted_percent_quant) / 2
    return pigment_quant

def load_image(filepath):
    '''Load image from png file and return as numpy array.
    
    Designed specifically for processing display images for quantification.
    Parameters:
        filepath - Full path of file to be processed.'''
    
    im = Image.open(filepath)

    ima = numpy.array(im)

    return(ima)

def extract_mask(img_array):
    '''Load array input and return its mask as numpy array.
    
    Designed specifically for processing display images for quantification.
    Parameters:
        img_array - Numpy array of masked image.'''

    '''dim = img_array.shape
    mask = numpy.ones((dim[0], dim[1]))

    masked_region = numpy.where(img_array == 0)

    mask[masked_region] = 0'''

    mask = (img_array != 0)
    mask = mask.astype(numpy.uint8)

    return mask




