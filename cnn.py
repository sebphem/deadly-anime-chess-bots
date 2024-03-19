
import numpy as np
from PIL import Image
import os.path
import torch
import torch.nn as nn
from torchvision import transforms
from matplotlib import pyplot

class ImageCompressor(nn.Module):
    def __init__(self):
        super(ImageCompressor, self).__init__()

        #input [3,1920,1080]
        self.pool1 = nn.AvgPool2d(kernel_size=128, stride=128) #default stride is equivalent to the kernel_size
        # output should be [3, 8, 15]

    def forward(self, x):
        # print("pre layer 1 x shape: ", x.shape)
        x = self.pool1(x)
        # print("pre x reshape shape: ", x.shape)
        #set n to whatever it needs to be to be dragged down to a 1 x n vector
        x = x.view(-1)
        # x = torch.tensor([x for i, x in enumerate(x) if i%6 !=5])
        x = [x.item() for i, x in enumerate(x) if i%6 !=5]
        return x

def compress_image():
    imgToTensor = transforms.ToTensor()
    device ='cpu'
    compressor = ImageCompressor().to(device)
    imageData = imgToTensor(Image.open("%s/video_processing/jjk_images/S1_(2)/frame1248.png" % os.path.dirname(__file__)))
    new_image = compressor(imageData)
    print('image data: ', len(new_image))
    # tensorToimg(new_image).show()
    print(new_image)


if __name__ == "__main__":
    print("Example ")
    compress_image()