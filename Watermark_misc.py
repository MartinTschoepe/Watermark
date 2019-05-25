import os
import numpy as np
from PIL import Image

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
            continue
        else:
            continue
    return num_pic

def colorwise_gauß_filer(full_array, sig):
    new_array = np.zeros((full_array.shape))
    new_array[:,:,0] = gaussian_filter(full_array[:,:,0], sigma = sig)
    new_array[:,:,1] = gaussian_filter(full_array[:,:,1], sigma = sig)
    new_array[:,:,2] = gaussian_filter(full_array[:,:,2], sigma = sig)
    return new_array

