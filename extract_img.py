import cv2
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
import torch
import numpy as np
from torch.utils.data import TensorDataset, DataLoader
from read_data import get_compressed_object
from torchvision import transforms
import time
import io
import PIL
from PIL import Image
import random

def make_dataset(root):
    INCH_TO_CM = 2.54
    LBS_TO_G = 453.592

    files = os.listdir(root)
    # print(type(files), len(files))

    print(len(files))
    # obj = get_compressed_object(os.path.join(root,"42080_Beverages wide.pklz"))
    # print(obj)
    # print(obj['dimensions'])
    # print(obj['weight'])
    # # print volume of obj
    # print(float(obj['dimensions'][0])*INCH_TO_CM*float(obj['dimensions'][1])*INCH_TO_CM*float(obj['dimensions'][2])*INCH_TO_CM)
    # print(float(obj['weight'])*LBS_TO_G)
    # print(float(obj['weight'])*LBS_TO_G/(float(obj['dimensions'][0])*INCH_TO_CM*float(obj['dimensions'][1])*INCH_TO_CM*float(obj['dimensions'][2])*INCH_TO_CM))
    # # save the image
    # img_dat = cv2.resize(cv2.cvtColor(cv2.imdecode(np.frombuffer(obj['image_data'],np.uint8),-1),cv2.COLOR_RGB2BGR), (224, 224))
    # cv2.imwrite(os.path.join("train_data_amazon", "42080_Beverages wide.jpg"), img_dat)
    # # exit()
    
    # create csv file to store labels of image
    with open("train_data_amazon.csv", "w") as f:
        f.write("img_name,length,breadth,height,density,weight\n")
        for filename in files:
            cmprsd_obj = get_compressed_object(os.path.join(root,filename))
            img_dat = cv2.resize(cv2.cvtColor(cv2.imdecode(np.frombuffer(cmprsd_obj['image_data'],np.uint8),-1),cv2.COLOR_RGB2BGR), (224, 224))
            cv2.imwrite(os.path.join("train_data_amazon", filename[:6]+'.jpg'), img_dat)
            f.write(filename[:6]+'.jpg,'+str(float(cmprsd_obj['dimensions'][0])*INCH_TO_CM)+','+str(float(cmprsd_obj['dimensions'][1])*INCH_TO_CM)+','+str(float(cmprsd_obj['dimensions'][2])*INCH_TO_CM)+','+str(float(cmprsd_obj['weight'])*LBS_TO_G/(float(cmprsd_obj['dimensions'][0])*INCH_TO_CM*float(cmprsd_obj['dimensions'][1])*INCH_TO_CM*float(cmprsd_obj['dimensions'][2])*INCH_TO_CM))+','+str(float(cmprsd_obj['weight'])*LBS_TO_G)+'\n')
    
if __name__ == "__main__":
    make_dataset("train_data")