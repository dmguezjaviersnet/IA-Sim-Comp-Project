from PIL import Image

#read the image
im = Image.open("./images/earth3.png")

#rotate image
angle = 0

while angle < 360:
    angle += 15
    new_img = im.rotate(angle)
    new_img.save(f'./images/img_rotate_{angle}_grades.png')