import pydicom as dicom
import numpy as np
from scipy.ndimage import gaussian_filter
from PIL import Image
import sys
import os
from os import listdir
from os.path import isfile, join

#DcmFilter manages dicom library and applies a gaussian filter
class DcmFilter:
    def __init__(self,path,sigma_value = 3):
        dicom_file = dicom.read_file(path)

        self.original = dicom_file.pixel_array
        self.filtered = gaussian_filter(self.original, sigma=sigma_value)
        self.ipp = dicom_file.ImagePositionPatient

#DcmFilter manages dicom library and applies a rotation
class DcmRotate:
    def __init__(self,path,angle = 180):
        dicom_file = dicom.read_file(path)

        self.original = dicom_file.pixel_array
        self.rotated = np.rot90(self.original, ((angle / 90) % 4))
        self.ipp = dicom_file.ImagePositionPatient

#Custom exception classes
class IncorrectNumberOfImages(Exception):
    def __str__(self):
        return 'Incorrect number of images. Aborting.'

class SameImagePositionPatient(Exception):
    def __str__(self):
        return 'The DICOM files appear to be the same. Aborting.'

class IncorrectNumberArguments(Exception):
    def __str__(self):
        return 'The name of the input folder is needed. Example: python3 -m dicomhandling.py input_folder_name'

#Returns true if the ImagePositionPatien is the same
def check_ipp(dcm_1, dcm_2):
    if(dcm_1.ipp == dcm_2.ipp):
        return True
    else:
        return False

#Given an array, save as image in jpeg format 
def save_image(np_image,folder,name):
    image = Image.fromarray(np_image)
    image.mode = 'I'
    image.point(lambda i:i*(1./256)).convert('L').save(folder + "/" + name)

def main():
    sigma = 3

    if(len(sys.argv) != 2):
        raise IncorrectNumberArguments

    folder = sys.argv[1]
    new_path = folder + "/residues"
    
    #Check if the folder 'residues' already exist
    if not os.path.isdir(new_path):
         os.makedirs(new_path)

    #Read .dcm images from input folder
    images = [f for f in listdir(folder) if isfile(join(folder, f)) and ".dcm" in f]

    if(len(images) != 2):
        raise IncorrectNumberOfImages

    image_1 = DcmFilter(join(folder, images[0]), sigma)
    image_2 = DcmFilter(join(folder, images[1]), sigma)

    if(check_ipp(image_1, image_2)):
        raise SameImagePositionPatient
        
    unfiltered_residue = image_1.original - image_2.original
    filtered_residue = image_1.filtered - image_2.filtered
    
    save_image(unfiltered_residue, new_path,"unfiltered.jpeg")
    save_image(filtered_residue, new_path,"filtered.jpeg")

if __name__ == "__main__":
    main()