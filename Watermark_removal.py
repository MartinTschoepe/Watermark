import os
import numpy as np
from PIL import Image

def print_statistics(averaged_array):
    #Statistics
    #Mean values
    mean_r = np.average(averaged_array[:,:,0])
    mean_g = np.average(averaged_array[:,:,1])
    mean_b = np.average(averaged_array[:,:,2])
    print("Mean values")
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

# Only a dummy because the correct method would require k-mean-method
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
        if filename.endswith(".JPG") or filename.endswith(".jpg"):
            im = Image.open(filename)
            num_pic+=1
            new_pic = np.array(im, dtype = np.int32)
            #remove_array_offset(new_pic)
            averaged_array+= new_pic
            #for idx, pixel in enumerate(im.getdata()):
                #averaged_array[idx,0]+= pixel[0]
                #averaged_array[idx,1]+= pixel[1]
                #averaged_array[idx,2]+= pixel[2]
            continue
        else:
            continue
    return num_pic

def main():
    directory1 = "Martin"
    directory2 = "Mario"
    directory3 = "Random3"

    w, h = 768, 511

    path1 = "Martin/5071_MP_01709.JPG"
    im = Image.open(path1)
    content_array = np.array(im, dtype = np.int32)

    im.save("original.jpg")


    averaged_array = np.zeros(shape = (h, w, 3), dtype = np.int32)
    num_pic = 0

    #num_pic = search_in_folder(directory1, num_pic, averaged_array)
    #num_pic = search_in_folder(directory2, num_pic, averaged_array)
    num_pic = search_in_folder(directory3, num_pic, averaged_array)

    print("Number of pics read: " + str(num_pic))

    averaged_array = averaged_array/num_pic

    print_statistics(averaged_array)
    remove_array_offset(averaged_array)
    stretch_array(averaged_array)
    print_statistics(averaged_array)

    if True:
        bound2 = 155
        for idx1 in range(len(averaged_array[:,:,:])):
            for idx2 in range(len(averaged_array[idx1,:,:])):
                if averaged_array[idx1, idx2, 0] <= bound2:
                    if averaged_array[idx1, idx2, 1] <= bound2:
                        if averaged_array[idx1, idx2, 2] <= bound2:
                            averaged_array[idx1, idx2, :] = 0
                        else:
                            averaged_array[idx1, idx2, :] = 0
                    else: 
                        if averaged_array[idx1, idx2, 2] <= bound2:
                            averaged_array[idx1, idx2, :] = 0
                        else:
                            averaged_array[idx1, idx2, :] = 255
                else: 
                    averaged_array[idx1, idx2, :] = 255

    print_statistics(averaged_array)
    plot_array_as_file(averaged_array, "averaged_array_try3.jpg")

    content_array1 = content_array - averaged_array/255*(255 - content_array)
    plot_array_as_file(content_array1, "content_array.jpg")

#averaged_array[:,0] = averaged_array[:,0] - mean_r
#print(averaged_array)

#TODOs
#0) Ausgabe des averaged_array als JPG.

#1) k-mean soll die zwei Klassen in den Daten erkennen und zu jedem Pixel sagen ob er
#in der Watermark Klasse K1 oder in der Non-Watermark Klasse K2 ist.

#2) k-mean soll den Schwerpunkte S1 und S2 der beiden Klassen bestimmen.

#3) bei allen K2 Pixel wird der Farbwert auf Null gesetzt und bei allen 
#K1 Pixel wird er auf "S2-S1" gesetzt

if __name__ == '__main__':
    main()
