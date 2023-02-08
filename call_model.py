import os
# os.environ['CUDA_VISIBLE_DEVICES'] = '1,2,3'
import time

import torch
# torch.cuda.set_device(2)
import torchvision
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# import dataloader as MyData
from torch.utils.data import random_split, DataLoader
from dataloader_aaryan import load_imgs
import sklearn
from sklearn.metrics import r2_score
import dataloader as MyData
from torch.utils.data import random_split, DataLoader
from torchvision import transforms
import PIL
from PIL import Image
import modelamazon

# code to predict the values of a random image given as input along with the weight of the object by loading state_dict of model

def predict(model_path, image_path, weight=0):
    GS_Model = modelamazon.ModelClass()
    model_checkpoint = torch.load(model_path)
    GS_Model.load_state_dict(model_checkpoint['model_dict'])
    # print(GS_Model)
    GS_Model.eval()
    
    # image_path = 'test_images/1.jpg'
    # weight = 0
    # image_path = 'test_images/2.jpg'
    img_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                std=[0.229, 0.224, 0.225])
    ])
    
    # load image 
    image = Image.open(image_path)
    image = img_transform(image)
    # convert this into B x 3 x 224 x 224 where B is 1
    image = image.unsqueeze(0)
    # print(image.shape)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    weight = torch.tensor(weight).to(device)
    # weight = weight.repeat(1, 128)
    weight = weight.unsqueeze(0)

    with torch.no_grad():
        image = image.to(device)
        # print(image.shape, weight.shape)
        output_cf, output_lbh = GS_Model(image, weight)
        output_cf = output_cf.cpu().numpy()
        output_lbh = output_lbh.cpu().numpy()
    
    return output_cf, output_lbh

if __name__ == '__main__':
    model_path = 'best_model_amazon_state.pt'
    image_path = 'test_data_amazon/6551_b.jpg'
    weight = 158.0
    output_cf, output_lbh = predict(model_path, image_path, weight)
    print(output_cf, output_lbh)
    
