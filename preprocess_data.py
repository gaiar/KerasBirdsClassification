import os, sys
import shutil
import random
from shutil import copyfile

import numpy as np


# def load_img(path, size = (256, 256)):
#     im = Image.open(path)
#     im = im.resize(size, Image.ANTIALIAS)
#     rgb_im = im.convert('RGB')  # Some imageses are in Grayscale
#     return np.array(rgb_im)

def center_crop(img_mat, size=(224, 224)):
    w, h, c = img_mat.shape
    start_h = h // 2 - (size[1] // 2)  # Size[1] - h of cropped image
    start_w = w // 2 - (size[0] // 2)  # Size[0] - w of cropepd image
    return img_mat[start_w:start_w + size[0], start_h:start_h + size[1], :]


# folder which contains the sub directories
source_dir = 'data/cub/images/'
total = 0


# list sub directories

def split_data():
    total = 0
    for root, dirs, files in os.walk(source_dir):
        # iterate through them
        for i in dirs:
            # create a new folder with the name of the iterated sub dir
            path = source_dir + 'test/' + "%s/" % i
            # os.makedirs(path)
            print(path)
            # take random sample, here 3 files per sub dir
            filenames = random.sample(os.listdir(source_dir + "%s/" % i),
                                      int(len(os.listdir(source_dir + "%s/" % i)) * 0.3))
            # print(filenames)
            # total+= len(os.listdir(source_dir + "%s/" % i ))
            # print (total)
            ## print filenames
            # copy the files to the new destination
            for j in filenames:
                print(source_dir + "%s/" % i + j)
                # shutil.move(source_dir + "%s/" % i + j, path)


def split_datasets(all_data_dir, training_data_dir, testing_data_dir, testing_data_pct, valid_data_dir=None,
                   create_sample=False):
    if testing_data_dir.count('/') > 1:
        shutil.rmtree(testing_data_dir, ignore_errors=False)
        os.makedirs(testing_data_dir)
        print("Successfully cleaned directory " + testing_data_dir)
    else:
        print(
            "Refusing to delete testing data directory " + testing_data_dir + " as we prevent you from doing stupid things!")

    if training_data_dir.count('/') > 1:
        shutil.rmtree(training_data_dir, ignore_errors=False)
        os.makedirs(training_data_dir)
        print("Successfully cleaned directory " + training_data_dir)
    else:
        print(
            "Refusing to delete testing data directory " + training_data_dir + " as we prevent you from doing stupid things!")

    pass


def split_dataset_into_test_and_train_sets(all_data_dir, training_data_dir, testing_data_dir, testing_data_pct):
    # Recreate testing and training directories
    if testing_data_dir.count('/') > 1:
        shutil.rmtree(testing_data_dir, ignore_errors=False)
        os.makedirs(testing_data_dir)
        print("Successfully cleaned directory " + testing_data_dir)
    else:
        print(
            "Refusing to delete testing data directory " + testing_data_dir + " as we prevent you from doing stupid things!")

    if training_data_dir.count('/') > 1:
        shutil.rmtree(training_data_dir, ignore_errors=False)
        os.makedirs(training_data_dir)
        print("Successfully cleaned directory " + training_data_dir)
    else:
        print(
            "Refusing to delete testing data directory " + training_data_dir + " as we prevent you from doing stupid things!")

    num_training_files = 0
    num_testing_files = 0

    for subdir, dirs, files in os.walk(all_data_dir):
        category_name = os.path.basename(subdir)

        # Don't create a subdirectory for the root directory
        print(category_name + " vs " + os.path.basename(all_data_dir))
        if category_name == os.path.basename(all_data_dir):
            continue

        training_data_category_dir = training_data_dir + '/' + category_name
        testing_data_category_dir = testing_data_dir + '/' + category_name

        if not os.path.exists(training_data_category_dir):
            os.mkdir(training_data_category_dir)

        if not os.path.exists(testing_data_category_dir):
            os.mkdir(testing_data_category_dir)

        for file in files:
            input_file = os.path.join(subdir, file)
            if np.random.rand(1) < testing_data_pct:
                shutil.copy(input_file, testing_data_dir + '/' + category_name + '/' + file)
                num_testing_files += 1
            else:
                shutil.copy(input_file, training_data_dir + '/' + category_name + '/' + file)
                num_training_files += 1

    print("Processed " + str(num_training_files) + " training files.")
    print("Processed " + str(num_testing_files) + " testing files.")
