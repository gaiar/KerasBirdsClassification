import os, sys
import shutil
import random
from shutil import copyfile


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
