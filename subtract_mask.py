import os
import numpy as np
from PIL import Image
import Watermark_misc as Wmisc
from scipy.ndimage import gaussian_filter
import scipy.ndimage 
import scipy.signal
import random

def matrix_substraction(content, mask, alpha, save):
    untouched_content = content * (1 - mask)
    watermarked_content = mask * (content - 120)
    print("watermarked_content < 0: " + str(np.sum(watermarked_content < 0) ) )
    watermarked_content = np.where(watermarked_content > 0, watermarked_content, 0)

    scaled_wtm_content = watermarked_content * alpha
    print("scaled_wtm_content > 255: " + str(np.sum(scaled_wtm_content > 255) ) )
    scaled_wtm_content = np.where(scaled_wtm_content < 255, scaled_wtm_content , 255)

    interim_content = untouched_content + scaled_wtm_content
    print("interim_content > 255: " + str(np.sum(interim_content > 255) ) )
    interim_content= np.where(interim_content < 255, interim_content, 255)
    #print("untouched_content: ")
    #Wmisc.print_statistics(untouched_content)
    #print("watermarked_content: ")
    #Wmisc.print_statistics(watermarked_content)
    #print("scaled_wtm_content: ")
    #Wmisc.print_statistics(scaled_wtm_content)
    #print("interim_content: ")
    #Wmisc.print_statistics(interim_content)
    #if save:
    #    interim_min = np.amin(interim_content, axis = 2)
    #    stacked_interim_min = np.stack((interim_min, interim_min, interim_min), axis = 2)
    #    new_content = np.where(stacked_interim_min > 0, interim_content, content) 
    #    return new_content
    #else:
    return interim_content

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

    #TODO: This creats colorful artefacts, due to the averageing in colors.
    #Problem: The average can be a color that never appeared in the previouse picture.
def smooth_thin_conture(content, wide_conture, thin_conture):
    two_layer_conture = wide_conture - thin_conture
    Wmisc.plot_array_as_file( two_layer_conture * 255, "two_layer_conture.png")
    two_layer_content = content * two_layer_conture
    two_layer_content = two_layer_content - thin_conture
    while ( np.amin( two_layer_content) < 0 ):
        print("Sum < 0: " + str(np.sum (two_layer_content < 0) ) )
        array_averaging(two_layer_content)

    new_content = content * (1 - wide_conture) + two_layer_content
    Wmisc.print_statistics(new_content)
    return new_content

def apply_to_pic(content_array, mask, conture2, conture3, conture4, directory, pic_name):
    con_wo_mask = matrix_substraction(content_array, mask, 2.0, True)
    #con_wo_mask = np.where(con_wo_mask[:,:,] > 0, con_wo_mask, 0) 
    #new_content = smooth_thin_conture(con_wo_mask, conture4, conture3)
    #content_final1 = Wmisc.blurring(new_content, conture2, 2.0 )
    #content_final1 = Wmisc.blurring(content_final1, conture3, 2.0 )
    #content_final1 = Wmisc.blurring(content_final1, conture4, 2.0 )
    #content_final1 = Wmisc.blurring(content_final1, mask, 2.0 )

    #Wmisc.plot_array_as_file(content_final1, str(directory) + "2/" + str(pic_name) )
    #Wmisc.plot_array_as_file(new_content, str(directory) + "2/" + str(pic_name) )
    Wmisc.plot_array_as_file(con_wo_mask, str(directory) + "2/" + str(pic_name) )

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

    mask_array = np.array(Image.open(path2), dtype = np.int32)[:,:,0:3]/255
    mask_array = np.where(mask_array < 1, mask_array, 1)

    interim_conture = Wmisc.get_conture_mask(mask_array, True)
    conture_mask = Wmisc.enlarge_mask( interim_conture, 1 ) - interim_conture
    conture_mask2 = Wmisc.enlarge_mask(conture_mask, 3) * mask_array
    conture_mask3 = Wmisc.enlarge_mask(conture_mask2, 3)
    conture_mask4 = Wmisc.enlarge_mask(conture_mask3, 3)

    mask_array -= interim_conture
    mask_array = np.where(mask_array > 0, mask_array, 0)
    #mask_array = Wmisc.blurring(mask_array, 1, 1.0)

    apply_to_folder(dir1, mask_array, conture_mask2, conture_mask3, conture_mask4)
    apply_to_folder(dir2, mask_array, conture_mask2, conture_mask3, conture_mask4)

if __name__ == '__main__':
    main()
