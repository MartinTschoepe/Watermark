import os
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
import scipy.ndimage 
import scipy.signal
import random

def print_statistics(averaged_array):
    #Statistics
    #Mean values
    mean_r = np.average(averaged_array[:,:,0])
    mean_g = np.average(averaged_array[:,:,1])
    mean_b = np.average(averaged_array[:,:,2])
    print("----- ---- Mean values ----- ----")
    print(mean_r)
    print(mean_g)
    print(mean_b)

    #Minimal values
    print("Minimum values")
    print(np.amin(averaged_array[:,:,0]))
    print(np.amin(averaged_array[:,:,1]))
    print(np.amin(averaged_array[:,:,2]))

    #Maximum values
    print("Maximum values")
    print(np.amax(averaged_array[:,:,0]))
    print(np.amax(averaged_array[:,:,1]))
    print(np.amax(averaged_array[:,:,2]))

def remove_array_offset(array):
    minimum_r = np.amin(array[:,:,0])
    minimum_g = np.amin(array[:,:,1])
    minimum_b = np.amin(array[:,:,2])
    array[:,:,0] = array[:,:,0] - minimum_r
    array[:,:,1] = array[:,:,1] - minimum_g
    array[:,:,2] = array[:,:,2] - minimum_b

def stretch_array(array):
    maximum_r = np.amax(array[:,:,0])
    maximum_g = np.amax(array[:,:,1])
    maximum_b = np.amax(array[:,:,2])
    if (maximum_r >= 255):
        maximum_r ==254
    if (maximum_g >= 255):
        maximum_g ==254
    if (maximum_b >= 255):
        maximum_b ==254
    array[:,:,0] = array[:,:,0] * (255/ maximum_r)
    array[:,:,1] = array[:,:,1] * (255/ maximum_g)
    array[:,:,2] = array[:,:,2] * (255/ maximum_b)

def plot_array_as_file(array, filename):
    array = np.where(array <= 255, array, 255)
    array = np.where(array >= 0, array, 0)
    im = Image.fromarray(np.uint8(array), 'RGB')
    im.save(filename)

def search_in_folder(directory, num_pic, averaged_array):
    for filename in os.listdir(directory):
        filename = directory + "/" + filename
        if num_pic%100 == 0:
            print(num_pic)
        if filename.endswith(".JPG") or filename.endswith(".jpg") or filename.endswith(".png"):
            im = Image.open(filename)
            num_pic+=1
            new_pic = np.array(im, dtype = np.int32)
            averaged_array+= new_pic
        #Commented 25.5.19 1 pm
            #continue
        #else:
            #continue
    return num_pic

def blurring(content, mask, sig):
    content_blurry = colorwise_gauß_filer(content, sig)
    new_content = content_blurry*mask + content*(1-mask) 
    return new_content

def get_conture_mask(mask_array, top_left):
    dx = 1
    mask_array2 = np.diff(mask_array, axis = 0)/dx #derivate in 511-direction
    mask_array3 = np.diff(mask_array, axis = 1)/dx #derivate in 768-direction
    filler_array2 = np.zeros(mask_array2[1:2,:,:].shape) #vector of shape (1, 768, 3)
    filler_array3 = np.zeros(mask_array3[:,1:2,:].shape) #vec of shape (511, 1, 3)
    if top_left:
        mask_array2 = np.concatenate((abs(mask_array2), filler_array2))
        mask_array3 = np.concatenate((abs(mask_array3), filler_array3), axis = 1)
    else:
        mask_array2 = np.concatenate( (filler_array2, abs(mask_array2)) )
        mask_array3 = np.concatenate( (filler_array3, abs(mask_array3)), axis = 1 )
    mask = mask_array2 + mask_array3 #add horizonal and vertical derivatives
    return np.where(mask < 1, mask, 1) 

def colorwise_gauß_filer(full_array, sig):
    new_array = np.zeros((full_array.shape))
    new_array[:,:,0] = gaussian_filter(full_array[:,:,0], sigma = sig)
    new_array[:,:,1] = gaussian_filter(full_array[:,:,1], sigma = sig)
    new_array[:,:,2] = gaussian_filter(full_array[:,:,2], sigma = sig)
    return new_array

def enlarge_mask(array, iter):
    for i in range(iter):
        larger_mask1 = get_conture_mask(array, True)
        larger_mask2 = get_conture_mask(larger_mask1, False)
        array = larger_mask1 + larger_mask2 + array 
        array = np.where(array < 1, array, 1) 
    return array

