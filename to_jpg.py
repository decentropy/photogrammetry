from PIL import Image 
import os 
PATH = "/home/casper/Documents/rendering/DATASET/1"

files = os.listdir(PATH) # list of files in directory

for file in files:  

    if file.endswith('.png'): # check if file is png
        file_path = f"{PATH}/{file}"

        im = Image.open(file_path).convert("RGB") # open file as an image object                
        im.save(f'{PATH}/jpgs/{file[:-4]}.jpg',quality=95, optimize=True)        