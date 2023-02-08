#!/usr/bin/env python3
import os
import random
from PIL import Image
import time
import matplotlib.pyplot as plt
import pickle
import io
try:
    # try using the new lz4 API
    import lz4.block
    lz4_compress = lz4.block.compress
    lz4_decompress = lz4.block.decompress
except ImportError:
    # fall back to old one
    lz4_compress = lz4.LZ4_compress
    lz4_decompress = lz4.LZ4_uncompress

def get_compressed_object(filename):
    with open(filename, 'rb') as fp:
        compressed_bytes = fp.read()
    decompressed = lz4_decompress(compressed_bytes)
    pickled_object = pickle.loads(decompressed)

    return pickled_object

def getImageFromString(encoded_image):
    buff = io.BytesIO() #buffer where image is stored
    buff.write(encoded_image)
    buff.seek(0)
    img = Image.open(buff)
    return img

def read_data(root):
    files = os.listdir(root)
    random.shuffle(files)
    print(len(files))
    for filename in files:
        f = os.path.join(root,filename)
        record = get_compressed_object(f)
        im = getImageFromString(record['image_data'])
        thickness_mask = record['thickness_mask']
        sp = plt.subplot(121)
        plt.imshow(im)
        sp.set_xlabel(str(record['weight'])+' lbs')
        sp=plt.subplot(122)
        plt.imshow(thickness_mask)
        dims = record['dimensions']
        dimstr = ' inches by '.join(dims)+' inches'
        sp.set_xlabel(dimstr)
        plt.show()
        


if __name__=='__main__':
    read_data('train_data')

