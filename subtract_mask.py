import os
import numpy as np
from PIL import Image
import Watermark_misc as Wmisc
from scipy.ndimage import gaussian_filter
import scipy.ndimage 
import scipy.signal
import random

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

def enlarge_mask(array, iter):
    for i in range(iter):
        larger_mask1 = get_conture_mask(array, True)
        larger_mask2 = get_conture_mask(larger_mask1, False)
        array = larger_mask1 + larger_mask2 + array 
        array = np.where(array < 1, array, 1) 
    return array

def colorwise_gauß_filer(full_array, sig):
    new_array = np.zeros((full_array.shape))
    new_array[:,:,0] = gaussian_filter(full_array[:,:,0], sigma = sig)
    new_array[:,:,1] = gaussian_filter(full_array[:,:,1], sigma = sig)
    new_array[:,:,2] = gaussian_filter(full_array[:,:,2], sigma = sig)
    return new_array

def blurring(content, mask, sig):
    content_blurry = colorwise_gauß_filer(content, sig)
    new_content = content_blurry*mask + content*(1-mask) 
    return new_content

def matrix_substraction(content, mask, alpha, save):
    interim = content -  mask * (255 - content) * alpha
    if save:
    	interim_min = np.amin(interim, axis = 2)
    	stacked_interim_min = np.stack((interim_min, interim_min, interim_min), axis = 2)
    	new_content = np.where(stacked_interim_min > 0, interim, content) 
    	return new_content
    else:
    	return interim

def get_matrix_argument(array, lx, ly):
    if np.any( array > 0 ):
        array[lx, ly] = np.median( array[array > 0] )

def array_averaging(array):
    arg_array = np.argwhere(array < 0)
    arg_list = []
    for i in range(arg_array.shape[0]):
        arg_list.append(arg_array[i])
    random.shuffle(arg_list)

    x_max = array.shape[0]
    y_max = array.shape[1]
    for idx, idy, idz in arg_list:
        if idx == 0:
            lx = 0
            rx = 1
        elif idx == (x_max - 1):
            lx = 1
            rx = 0
        else:
            lx = 1
            rx = 1
        if idy == 0:
            ly = 0
            ry = 1
        elif idy == (y_max - 1):
            ly = 1
            ry = 0
        else:
            ly = 1
            ry = 1
        get_matrix_argument(array[idx-lx:idx+rx+1, idy-ly:idy+ry+1, idz], lx, ly)

def smooth_thin_conture(content, wide_conture, thin_conture):
    two_layer_conture = wide_conture - thin_conture
    Wmisc.plot_array_as_file( two_layer_conture * 255, "two_layer_conture.png")
    two_layer_content = content * two_layer_conture
    two_layer_content = two_layer_content - thin_conture
    while ( np.amin( two_layer_content) < 0 ):
        print("Sum < 0: " + str(np.sum (two_layer_content < 0) ) )
        array_averaging(two_layer_content)

    new_content = content * (1 - wide_conture) + two_layer_content
    return new_content

def apply_to_pic(content_array, mask, conture2, conture3, conture4, directory, pic_name):
    q = 2.2
    con_wo_mask = content_array -  mask * (255 - content_array) * (1 - content_array/255) * q
    con_wo_mask = np.where(con_wo_mask > 0, con_wo_mask, 0) 
    new_content = smooth_thin_conture(con_wo_mask, conture4, conture3)
    content_final1 = blurring(new_content, conture2, 1.5 )
    content_final1 = blurring(content_final1, conture3, 1.5 )
    content_final1 = blurring(content_final1, conture4, 1.5 )
    content_final1 = blurring(content_final1, mask, 2.0 )
    Wmisc.plot_array_as_file(content_final1, str(directory) + "2/" + str(pic_name) )
    #Wmisc.plot_array_as_file(con_wo_mask, str(directory) + "2/" + str(pic_name) )

def apply_to_folder(directory, mask, conture2, conture3, conture4):
    for filename in os.listdir(directory):
        full_filename = directory + "/" + filename
        if full_filename.endswith(".jpg") or full_filename.endswith(".png"):
            content = np.array(Image.open(full_filename), dtype = np.int32)
            apply_to_pic(content, mask, conture2, conture3, conture4, directory, filename)

def main():
    #path1 = "ESRGAN/results/new_artefact_removal/Martin/5071_MP_01709_rlt.png"
    dir1 = "Martin_sr"
    dir2 = "Mario_sr"
    path2 = "mask.png"

    #content_array = np.array(Image.open(path1), dtype = np.int32)
    mask_array = np.array(Image.open(path2), dtype = np.int32)[:,:,0:3]/255
    mask_array = np.where(mask_array < 1, mask_array, 1)

    interim_conture = get_conture_mask(mask_array, True)
    conture_mask = enlarge_mask( interim_conture, 1 ) - interim_conture
    conture_mask2 = enlarge_mask(conture_mask, 3) * mask_array
    conture_mask3 = enlarge_mask(conture_mask2, 3)
    conture_mask4 = enlarge_mask(conture_mask3, 3)

    mask_array -= interim_conture
    mask_array = blurring(mask_array, 1, 1.0)

    apply_to_folder(dir1, mask_array, conture_mask2, conture_mask3, conture_mask4)
    apply_to_folder(dir2, mask_array, conture_mask2, conture_mask3, conture_mask4)

if __name__ == '__main__':
    main()
