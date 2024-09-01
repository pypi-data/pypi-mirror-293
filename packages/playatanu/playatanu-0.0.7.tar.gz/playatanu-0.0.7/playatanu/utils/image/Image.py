from PIL import Image

import numpy 

def resize(image,size):
    image=Image.fromarray(image)
    image = image.resize(size)
    return numpy.array(image)


def read(filename:str):
    return numpy.array(Image.open(filename))

def write(path:str,image):
    image=Image.fromarray(image)
    image.save(path)


