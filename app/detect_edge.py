from PIL import Image
import numpy as np
import cv2


def preprocess_image(filepath, outtype='g'):
    '''Read in .tif image and cover scale and magnification labels.
    
    Experimentally found to work with .tif and .png formats, otherwise unknown.
    Parameters:
        filepath - Full path of file to be processed.
        outtype - Option for whether the output should be grayscale or colorized.
            options:
                gray (default) - 'g', 'gray'
                color - 'c', 'color' '''

    im = Image.open(filepath)

    '''#process PNG image 
    #https://www.kite.com/python/answers/how-to-convert-a-rgba-image-to-a-rgb-image-with-pil-in-python
    if filetype == 'PNG' or filetype == 'png':
        im.load()
        background = Image.new("RGB", im.size, (255, 255, 255))
        background.paste(im)
        im = background'''

    # Convert image to numpy array
    ima = np.array(im)
    #im.close()

    if(outtype == 'g' or outtype == 'gray'):
        # Convert image to grayscale
        im_gray = cv2.cvtColor(ima, cv2.COLOR_RGB2GRAY)

        # Cover the scale and magnification regions with zero pixels
        #im_gray[0:40, -175:] = 0  # Scale
        #im_gray[-30:, 0:150] = 0  # Magnitude

        return im_gray
    elif(outtype == 'c' or outtype == 'color'):
        # Cover the scale and magnification regions with zero pixels
        #ima[0:40, -175:, :] = 0  # Scale
        #ima[-30:, 0:150, :] = 0  # Magnitude

        return ima
    else:
        print('Output type not accepted. Accepted arguments: \'g\', \'gray\', \'c\', \'color\'')


def threshflood(image, threshold=113):
    '''Threshold image and use flood fill to get rough mask of planarian.

    Flood filling technique referenced: 
    https://www.learnopencv.com/filling-holes-in-an-image-using-opencv-python-c/ 
    Parameters: 
        image - Numpy array image.
        threshold (default = 113) - Intensity level used for threshold and subsequent floodfill.'''
    # Default threshold value is 113 by experimentation
    ret, im_thresh = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)

    # Flood fill to connect planarian body

    # Copy the thresholded image
    im_floodfill = im_thresh.copy()

    # Mask used to flood filling
    # Notice the size needs to be 2 pixels than the image
    h, w = im_thresh.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)

    # Floodfill from lower left zero region created in preprocessing
    cv2.floodFill(im_floodfill, mask, (h, 0), 255)
    # Floodfill from upper left zero region created in preprocessing
    cv2.floodFill(im_floodfill, mask, (0, 0), 255)

    # Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)

    # Combine the two images to get the foreground
    mask = im_thresh | im_floodfill_inv

    return mask


def undesired_objects(image):
    '''Find the largest connected component.

    Reference used:
    https://stackoverflow.com/questions/47055771/how-to-extract-the-largest-connected-component-using-opencv-and-python
    Parameters:
        image - Numpy array image.'''
    image = image.astype('uint8')
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(
        image, connectivity=4)
    sizes = stats[:, -1]

    max_label = 1
    max_size = sizes[1]
    for i in range(2, nb_components):
        if sizes[i] > max_size:
            max_label = i
            max_size = sizes[i]

    img2 = np.zeros(output.shape)
    img2[output == max_label] = 255

    return img2


def remove_noise(image):
    '''Perform image opening and isolate largest connected component.
    
    Parameters:
        image - Numpy array image.'''
    kernel = np.ones((9, 9), np.uint8)

    # Perform image opening
    im_open = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=1)

    # Isolate largest connected component
    largest = undesired_objects(im_open)
    mask = np.int8(largest)
    mask[mask == -1] = 1

    return mask
