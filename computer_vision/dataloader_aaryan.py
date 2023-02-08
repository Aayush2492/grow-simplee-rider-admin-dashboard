from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
from torchvision import transforms
import numpy as np
import pandas as pd


def load_imgs(path_to_imgDir, path_to_csv):
    """
    a tuple with first element as name of class and second element is
    """
    df = pd.read_csv(path_to_csv)
    df = df.drop(['True Weight Ibs','Length','Width','Height','Volume','Weight(kg)'],axis=1)
    a = open("real.txt","r")
    real = a.read()
    a.close()
    real_li = real.split('\n')
    li = []
    for i in range(df.shape[0]):
        if df['Class'][i] not in real_li:
            li.append(i)
    df = df.drop(li)
    df.set_index("Class", inplace = True)
    resize = transforms.Resize(size=(255,255))
    transform = transforms.Compose([resize,
                                transforms.CenterCrop(224),
                                transforms.ToTensor()])
    dataset = ImageFolder(root=path_to_imgDir,transform=transform)
    for i in range(0,len(dataset.classes)):
        if dataset.classes[i] in list(df.index):
            temp = df.loc[dataset.classes[i]]
            # dataset.classes[i] = (dataset.classes[i],np.array([temp[0],temp[1]]))
            dataset.classes[i] = np.array([temp[0],temp[1],temp[2],temp[3]])
            # print(dataset.classes[i])
    for i in range(0,len(dataset.targets)):
        dataset.targets[i] = dataset.classes[dataset.targets[i]]
    return dataset