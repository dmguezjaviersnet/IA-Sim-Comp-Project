EPSILON = ''
import pickle
from os import path, mkdir
from typing import Any, Tuple
from PIL import Image
import math


BLUE = (44, 176, 218)



def make_pickle_file(file_name, data):
    with open(f"{file_name}.pickle", "wb") as outfile:
        pickle.dump(data, outfile)

def unpick_pickle_file(file_name):
    with open(file_name, 'rb') as f:
        data = pickle.load(f)
    
    return data

def serialize_data(data, file_name: str):
    if not path.exists('./serialized_data'):
        mkdir('./serialized_data')

    make_pickle_file(file_name, data)

def deserialize_data(file_name) -> Tuple[bool, Any]:
    if path.exists(file_name):
        data = unpick_pickle_file(file_name)
        return data
    
    else: return None

def open_image(ori_path: str):
    return Image.open(ori_path)

def generate_images_to_rotation(ori_path, des_path):
    im = open_image(ori_path)
    #rotate image
    angle = 0

    while angle < 360:
        angle += 15
        new_img = im.rotate(angle)
        new_img.save(des_path)



def next_point_moving_in_elipse(point: Tuple[float, float], a, b, degree):
    new_x = point[0] + (a*math.cos(degree * 2 * math.pi / 360))
    new_y = point[1] + (b*math.sin(degree * 2 * math.pi / 360))
    return (new_x, new_y)