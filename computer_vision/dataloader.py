import torch
import torchvision
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from torch.utils.data import random_split, DataLoader
import PIL
# print(torchvision.__version__)
# print(torch.__version__)
# print(torch.cuda.is_available())
# print("hello")
# df = pd.read_csv('Data.csv')

# print(df.head())


class CustomDataset(torch.utils.data.Dataset):
    def __init__(self, csv_path, image_dir, transform=None):
        """
        Args:
            csv_path (string): path to csv file
            image_dir (string): directory with all the images
            transform (callable, optional): optional transform to be applied
                on a sample
        """
        self.image_label = pd.read_csv(csv_path)
        self.image_dir = image_dir
        self.transform = transform

    def __len__(self):
        return len(self.image_label)

    def __getitem__(self, idx):
        img_name = os.path.join(self.image_dir,
                                self.image_label.iloc[idx, 0])
        image = plt.imread(img_name)
        label = self.image_label.iloc[idx, 1]
        sample = {'image': image, 'label': label}

        if self.transform:
            sample = self.transform(sample)

        return sample

class ObjectDataset(torch.utils.data.Dataset):
    def __init__(self, object_dir, csv_file, transform=None):
        print("ObjectDataset")
        print(csv_file)
        
        self.data = pd.read_csv(csv_file)
        self.data['labels'] = self.data['length'].astype(str) +','+ self.data['breadth'].astype(str) +','+ self.data['height'].astype(str) +','+ self.data['density'].astype(str) +','+ self.data['weight'].astype(str)
        self.data = self.data.drop(['length', 'breadth', 'height', 'density', 'weight'], axis=1)
        self.object_dir = object_dir

        self.transform = transform

        

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        # object_class = self.data.iloc[idx]['object_class']
        object_path = self.object_dir + self.data.iloc[idx]['img_name']
        # object_tensor = object_path
        object = PIL.Image.open(object_path)
        if self.transform:
            object = self.transform(object)
        labels = self.data.iloc[idx]['labels'].split(',')
        labels = [float(label) for label in labels]
        labels_tensor = torch.tensor(labels)
        
        return object, labels_tensor
    
def object_dataloader(object_dir, csv_file, transform=None, batch_size=16, sampler=False):
    dataset = ObjectDataset(object_dir, csv_file, transform)
    print("Size of {} = {}".format(csv_file, len(dataset)))
    if sampler:
        # choose only 25% of the dataset
        dataset = torch.utils.data.Subset(dataset, range(0, len(dataset), 4))
    print("Size of {} = {}".format(csv_file, len(dataset)))
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    return dataloader

if __name__ == "__main__":

    val_dat = object_dataloader('val_data_amazon/', 'val_data_amazon.csv', batch_size=16)
    print(len(val_dat.dataset))