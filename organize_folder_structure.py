
import os
import shutil
from time import time
import re
import argparse
import numpy as np
import SimpleITK as sitk
import scipy.ndimage as ndimage

def numericalSort(value):
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


def lstFiles(Path):

    images_list = []  # create an empty list, the raw image data files is stored here
    for dirName, subdirList, fileList in os.walk(Path):
        for filename in fileList:
            if ".nii.gz" in filename.lower():
                images_list.append(os.path.join(dirName, filename))
            elif ".nii" in filename.lower():
                images_list.append(os.path.join(dirName, filename))
            elif ".mhd" in filename.lower():
                images_list.append(os.path.join(dirName, filename))

    images_list = sorted(images_list, key=numericalSort)
    return images_list


parser = argparse.ArgumentParser()
parser.add_argument('--images', default='./Data_folder/mocorrected/volumes', help='path to the images a (early frames)')
parser.add_argument('--labels', default='./Data_folder/mocorrected/labels', help='path to the images b (late frames)')
parser.add_argument('--split', default=2, help='number of images for testing')
args = parser.parse_args()

if __name__ == "__main__":

#     list_images = lstFiles(args.images)
#     list_labels = lstFiles(args.labels)
    list_labels = sorted(["../pet_dataset_7_13/"+file for file in os.listdir("../pet_dataset_7_13") if file[0] != "."])
    numbers = set([file.split("/")[-1].split("_")[0] for file in list_labels])
    list_images = sorted(["../dataset_5_29/"+file for file in os.listdir("../dataset_5_29") \
                   if (file[0] != "." and file.split("_")[0] in numbers)])
    # test files
    list_labels += ["../test-dataset-8-8/pet/i103910_img_pet_0.nii.gz", "../test-dataset-8-8/pet/i103910_img_pet_1.nii.gz"]
    list_images += ["../test-dataset-8-8/ct/i103910_img_ct_0.nii.gz", "../test-dataset-8-8/ct/i103910_img_ct_1.nii.gz"]
    
    print(list_labels, list_images)
        
    assert len(list_labels) == len(list_images)
    
    if not os.path.isdir('./Data_folder/train'):
        os.mkdir('./Data_folder/train')

    if not os.path.isdir('./Data_folder/test'):
        os.mkdir('./Data_folder/test')

    for i in range(len(list_images)-int(args.split)):

        a = list_images[i]
        b = list_labels[i]

        print(a)

        save_directory = os.path.join(str('./Data_folder/train/patient_' + str(i)))

        if not os.path.isdir(save_directory):
            os.mkdir(save_directory)

        label = sitk.ReadImage(b)
        image = sitk.ReadImage(a)

        label_directory = os.path.join(str(save_directory), 'label.nii')
        image_directory = os.path.join(str(save_directory), 'image.nii')

        sitk.WriteImage(image, image_directory)
        sitk.WriteImage(label, label_directory)


    for i in range(int(args.split)):

        a = list_images[len(list_images)-int(args.split)+i]
        b = list_labels[len(list_images)-int(args.split)+i]

        print(a)

        save_directory = os.path.join(str('./Data_folder/test/patient_' + str(i)))

        if not os.path.isdir(save_directory):
            os.mkdir(save_directory)

        label = sitk.ReadImage(b)
        image = sitk.ReadImage(a)

        label_directory = os.path.join(str(save_directory), 'label.nii')
        image_directory = os.path.join(str(save_directory), 'image.nii')

        sitk.WriteImage(image, image_directory)
        sitk.WriteImage(label, label_directory)