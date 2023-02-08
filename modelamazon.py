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


# Regressor Model for the image
class ModelClass(nn.Module):
    def __init__(self, image_size=224, freeze=False):
        super(ModelClass, self).__init__()
        
        # TODO: Complete the model
        self.resnet = torchvision.models.resnet101()
        # freeze the all layers of resnet except the last layer
        if freeze:
            for param in self.resnet.parameters():
                param.requires_grad = False
        # print(self.resnet)

        self.image_size = image_size
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')      
        
        self.loss_function_huber = nn.HuberLoss().to(self.device)
        self.loss_function_l1 = nn.L1Loss().to(self.device)
        self.loss_function_mse = nn.MSELoss().to(self.device)

        self.model = nn.Sequential(
            *(list(self.resnet.children())[:-1]
        ))
        
        # print(self.model)
        
        self.fc1_density = nn.Sequential(
            nn.Linear(2048, 1024),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(32, 1),
            
        )
        
        self.fc2_lbh = nn.Sequential(
            nn.Linear(2304, 1024),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(64, 3),
        )
        
        # number of parameter in the model
        # print(sum(p.numel() for p in self.model.parameters() if p.requires_grad))
        # print(sum(p.numel() for p in self.fc1_density.parameters() if p.requires_grad))
        # print(sum(p.numel() for p in self.fc2_lbh.parameters() if p.requires_grad));exit()
        
        # print(self.model)
        self.optimizer = torch.optim.SGD(self.parameters(), lr=0.0005, momentum=0.9, weight_decay=0.0001)
        
        
        print("Current: ", torch.cuda.current_device())
        if torch.cuda.is_available():
            self.model = self.model.to(self.device)
            self.fc1_density = self.fc1_density.to(self.device)
            self.fc2_lbh = self.fc2_lbh.to(self.device)
            
        self.model = nn.DataParallel(self.model, device_ids=[0,1,2,3], dim=0)
        
        lst = set()
        for param in self.model.parameters():
            # print(param.device)
            lst.add(param.device)
        print(lst)
                    
                    
    # TODO: Complete the forward function
    def forward(self, x, weight=0):

        self.model.to(self.device)
        x = x.float()
        x = x.to(self.device)

        conv_out = self.model(x)
        # print("Conv Shape ",conv_out.shape)
        density_out = self.fc1_density(conv_out.view(conv_out.size(0), -1))
        density_out = density_out.reshape(-1)
        # print("Density out: ",density_out.shape)
        # create vector for density of shape B x 512 from density output
        density = density_out.view(density_out.size(0), 1).repeat(1, 128)
        # print("density: ",density.shape)
        
        # create vector for weight of shape B x 512 from input weight
        # print("weight: ",weight.shape)
        weight = weight.view(weight.size(0), 1).repeat(1, 128)
        # print("weight: ",weight.shape)
        
        
        # concatenate the three vectors
        concat = torch.cat((conv_out.view(conv_out.size(0), -1), density, weight), dim=1)
        # print("concat: ",concat.shape)
        
        # pass through the second fully connected layer
        lbh_out = self.fc2_lbh(concat)
        # print("lbh_out: ",lbh_out.shape)

        return density_out, lbh_out

    # TODO: Complete the training function
    def trainer(self, train_loader, val_loader=None, epochs=10):
        self.model.train()
        best_val_acc = 1000
        loss = []
        length = []
        width = []
        height = []
        CF = []
        start_time = time.time()
        curr_time = start_time
        for epoch in range(epochs):
            self.train_epoch(train_loader, epoch)
        
            if val_loader is not None:
                val_loss, val_acc = self.evaluate(val_loader)
                curr_time2 = time.time()
                print('Epoch: {} \tValidation Loss: {:.6f} \tValidation Accuracy: {} \t Time: {}'.format(epoch, val_loss, val_acc, curr_time2 - curr_time))
                curr_time = curr_time2
                loss.append(val_loss.cpu())
                length.append(val_acc[0].cpu().item())
                width.append(val_acc[1].cpu().item())
                height.append(val_acc[2].cpu().item())
                CF.append(val_acc[3].cpu().item())

                if val_loss < best_val_acc:
                    print("Here")
                    best_val_acc = val_loss
                    torch.save({'model_dict' : self.state_dict(),
                                'optimizer_state': self.optimizer.state_dict()}, 'best_model_amazon_state3.pt')
                    torch.save(self.state_dict(), 'best_model_amazon3.pt')
                    
        print("Total time taken for Training and Validation: {}".format(time.time() - start_time))  
        plt.plot(loss)
        plt.title('Validation Loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.savefig('loss_amazon.png')
        plt.close()
        print('Best Validation Accuracy: {}'.format(best_val_acc))
        
        plt.plot(length)
        plt.title('Length Loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.savefig('length_amazon.png')
        plt.close()
        
        plt.plot(width)
        plt.title('width Loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.savefig('width_amazon.png')
        plt.close()
        
        plt.plot(height)
        plt.title('height Loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.savefig('height_amazon.png')
        plt.close()
        
        plt.plot(CF)
        plt.title('CF Loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.savefig('cf_amazon.png')
        plt.close()
        
        # print(length, width, height, CF)
        print("PLots saved")
        return
    
    def train_epoch(self, train_loader, epoch):
        self.train()
        # print("Epoch Done")
        start_time = time.time()
        for batch_idx, (data, target) in enumerate(train_loader):
            # print(batch)
            # target = np.array([train_loader.dataset.dataset.targets[i] for i in target])
            # target = torch.tensor(target)
            # print(target.shape)
            
            # select last column of target which is the weight
            weights = target[:, -1]
            weights = weights.to(self.device)
            data, target = data.float(), target.float()
            data, target = data.to(self.device), target.to(self.device)
            
            # select first 3 columns of target which is the length, width and height
            label_lbh = target[:, :3]
            # select fourth column of target which is the CF
            label_CF = target[:, 3]
            # print("label_CF: ",label_CF.shape)
            # print("label_lbh: ",label_lbh.shape)
            output_CF, output_lbh = self(data, weights)
            loss_CF = self.loss_function_huber(output_CF, label_CF) + 0.001*self.loss_function_mse(output_CF, label_CF) + 0.001*self.loss_function_l1(output_CF, label_CF)
            loss_lbh = self.loss_function_huber(output_lbh, label_lbh) + 0.001*self.loss_function_mse(output_lbh, label_lbh) + 0.001*self.loss_function_l1(output_lbh, label_lbh)
            loss = loss_CF + loss_lbh
            loss.backward()
            self.optimizer.step()
            self.optimizer.zero_grad()
            
            if batch_idx % 100 == 0:
                print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                    epoch, batch_idx * len(data), len(train_loader.dataset),
                    100. * batch_idx / len(train_loader), loss.item()))
        print("Time taken to train Epoch: {}".format(time.time() - start_time))
        return
               

    # TODO: Complete the evaluation function
    def evaluate(self, test_loader):
        self.model.eval()
        test_loss = 0
        mse_attr = 0
        with torch.no_grad():
            for data, target in test_loader:
                # target = np.array([test_loader.dataset.dataset.targets[i] for i in target])
                # print("--------------------------------",type(target))
                # target = torch.tensor(target)
                weights = target[:, -1]
                weights = weights.to(self.device)
                data, target = data.float(), target.float()
                data, target = data.to(self.device), target.to(self.device)
                
                label_lbh = target[:, :3]
                label_CF = target[:, 3]
                
                output_CF, output_lbh = self(data, weights)
                test_loss += self.loss_function_huber(output_CF, label_CF) + 0.001*self.loss_function_mse(output_CF, label_CF) + 0.001*self.loss_function_l1(output_CF, label_CF)
                test_loss += self.loss_function_huber(output_lbh, label_lbh) + 0.001*self.loss_function_mse(output_lbh, label_lbh) + 0.001*self.loss_function_l1(output_lbh, label_lbh)
                mse_attr_CF = (output_CF - label_CF)**2
                mse_attr_CF = mse_attr_CF.unsqueeze(1)
                mse_attr_lbh = (output_lbh - label_lbh)**2
                # concat mse_attr_CF of shape B and mse_attr_lbh of shape B x 3
                mse = torch.cat((mse_attr_CF, mse_attr_lbh), dim=1)
                mse_attr += mse.sum(dim=0)
                mse_attr = mse_attr / len(test_loader.dataset)
                
                

            test_loss /= len(test_loader.dataset)
            
            # print(mse_attr.shape, mse_attr)

            return test_loss, mse_attr

    # TODO: Complete the prediction function
    def predict(self, data, weight):
        self.eval()
        with torch.no_grad():
            output_cf, output_lbh = self(data, weight)
        return output_cf, output_lbh
    
        


def main():
    # TODO: Complete the main function
    print(torch.cuda.device_count())
    print(torch.cuda.current_device())
    GS_Model = ModelClass()
    # GS_Model2 = nn.DataParallel(GS_Model, device_ids=None).to(GS_Model.device)
    # print(GS_Model)
    # dataset = load_imgs('data/','Data (1).csv')
    # # print(dataset.targets)
    # train_ds, val_ds = random_split(dataset, [0.9, 0.1])
    # # train_ds.dataset.targets = train_ds.dataset.classes
    # train_loader = DataLoader(train_ds, batch_size=16, shuffle=True, num_workers=4, pin_memory=True)
    # val_loader = DataLoader(val_ds, batch_size= 16, num_workers=4, pin_memory=True)

    # object_data = MyData.ObjectDataset('data/', 'modified.csv')
    # import test_amazon as ta
    # train_ds = ta.make_dataset('train_data/', k=10000)
    # val_ds = ta.make_dataset('val_data/', k=5000)
    # test_ds = ta.make_dataset('test_data/', k=1000)
    # trainDataLoader = DataLoader(train_ds, batch_size =16)
    # valDataLoader = DataLoader(val_ds, batch_size =16)
    # testDataLoader = DataLoader(test_ds, batch_size=16)
    # print(torch.cuda.is_available())

    # train_data = MyData.ObjectDataset('train_data_amazon/', 'train_data_amazon.csv')
    # val_data = MyData.ObjectDataset('val_data_amazon/', 'val_data_amazon.csv')
    # test_data = MyData.ObjectDataset('test_data_amazon/', 'test_data_amazon.csv')
    # trainDataLoader = DataLoader(train_data, batch_size =16)
    # valDataLoader = DataLoader(val_data, batch_size =16)
    # testDataLoader = DataLoader(test_data, batch_size=16)
    
    train_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        transforms.RandomRotation(30),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    val_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.RandomHorizontalFlip(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    test_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    trainDataLoader = MyData.object_dataloader('train_data_amazon/', 'train_data_amazon.csv', train_transform, batch_size=64, sampler=True)
    valDataLoader = MyData.object_dataloader('val_data_amazon/', 'val_data_amazon.csv', val_transform, batch_size=16)
    testDataLoader = MyData.object_dataloader('test_data_amazon/', 'test_data_amazon.csv', test_transform, batch_size=16)

    GS_Model.trainer(trainDataLoader, valDataLoader, epochs=5)
    
    GS_Model.eval()
    checkpoint = torch.load('best_model_amazon_state3.pt')
    GS_Model.load_state_dict(checkpoint['model_dict'])
    test_loss, test_acc = GS_Model.evaluate(testDataLoader)
    print("Final Loss: {}\t Final SE: {}".format(test_loss, test_acc))
    
    

if __name__ == '__main__':
    main()