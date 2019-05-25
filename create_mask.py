import os
import numpy as np
from PIL import Image
import Watermark_misc as Wmisc

def main():
    #directory1 = "Martin_sr2"
    #directory2 = "Mario_sr2"
    directory3 = "D:/Bilder/Watermark/Superres/Random3"
    #directory3 = "sub"

    w, h = 768*4, 512*4

    averaged_array = np.zeros(shape = (h, w, 3), dtype = np.int32)
    num_pic = 0

    #num_pic = Wmisc.search_in_folder(directory1, num_pic, averaged_array)
    #num_pic = Wmisc.search_in_folder(directory2, num_pic, averaged_array)
    num_pic = Wmisc.search_in_folder(directory3, num_pic, averaged_array)

    print("Number of pics read: " + str(num_pic))
    averaged_array = averaged_array/num_pic

    Wmisc.print_statistics(averaged_array)
    Wmisc.remove_array_offset(averaged_array)
    Wmisc.print_statistics(averaged_array)
    Wmisc.stretch_array(averaged_array)
    Wmisc.print_statistics(averaged_array)

    Wmisc.plot_array_as_file(averaged_array, "substructure_mask.png")

    alternative_mask = np.array(averaged_array, copy = True)

    bound2 = 160
    if True:
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

    Wmisc.print_statistics(averaged_array)
    Wmisc.plot_array_as_file(averaged_array, "classical_mask.png")

    res = np.sum(alternative_mask, axis=2)/3
    new_res = np.stack((res, res, res), axis = 2)

    new_res = np.where(new_res < bound2, new_res, 255)
    new_res = np.where(new_res > bound2, new_res, 0)

    Wmisc.print_statistics(new_res)
    Wmisc.plot_array_as_file(new_res, "new_mask.png")


if __name__ == '__main__':
    main()
