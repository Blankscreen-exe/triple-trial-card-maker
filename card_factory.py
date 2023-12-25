from os import path
import json
from datetime import datetime as dt
import numpy as np
import cv2
from PIL import Image
 
 
# REF: https://stackoverflow.com/questions/36921496/how-to-join-png-with-alpha-transparency-in-a-frame-in-realtime/37198079#37198079
# REF: https://gist.github.com/uchidama/6d51e8d4b740b4cac14855a55b9c65ef
def base_exists(func):
    def wrapper(self, *args, **kwargs):
        if self._base is None:
            message = "Base image does not exist. You need to generate it first."
            raise ValueError(f"\033[1;37;41m{' ' * len(message)}\n{message}\n{' ' * len(message)}\033[0m")
        return func(self, *args, **kwargs)
    return wrapper

# def asset_exists(func):
#     def wrapper(self, *args, **kwargs):
#         found_image = self.card_elements
#         print("ARGS", args)
#         print("KWARGS", kwargs)
#         try:
#             for key in kwargs["key_path"].split("."):
#                 print(key)
#                 found_image = found_image[key]
#             asset = self.get_asset(kwargs["key_path"])
#             print(asset)
#         except:
#             raise ValueError("\033[1;37;41mAsset image does not exist. You need to load it first using load_asset().\033[0m")
#         return func(self, *args, **kwargs)
#     return wrapper
 
class CardMaker:
    
    def __init__(self):
        self.config = None
        
        # default vars
        
        # Poker game card size
        self.card_width = 822 # pixel
        self.card_height = 1122 # pixel
        
        self.card_elements = {}
        self._base = None
        
    def generate_card_base(self, height:float=None, width:float=None)->object:
        """Generates base card to draw upon"""
        if height is None:
            height = self.card_height
        
        if width is None:
            width = self.card_width
            
        # white card base
        self._base = np.zeros((height, width, 4), dtype=np.uint8)
        self._base[:, :, 0:3] = 255  # Set RGB channels to white (255, 255, 255)
        self._base[:, :, 3] = 255  # Set the alpha channel to fully opaque (255)
        
        return self
    
    @base_exists
    def get_base_image(self)->np:
        """getter for base card image
        
        Return Image object of the _base image
        """
        return Image.fromarray(self._base)
    
    @base_exists
    def load_asset(self, key_path:str, img:str)->object:
        """loads an image and stores them within a hashtable(python dictionary)"""
        keys = key_path.split('.')

        for key in keys[:-1]:
            if key not in self.card_elements:
                self.card_elements[key] = {}
            self.card_elements = self.card_elements[key]

        last_key = keys[-1]
        
        if isinstance(img, str):
            # Load the image using Pillow instead of cv2
            loaded_img = Image.open(img)
            loaded_img = np.array(loaded_img)
            # Ensure the image has an alpha channel if needed
            # if loaded_img.shape[2] == 3:  # If image doesn't have an alpha channel
                # alpha = np.full((loaded_img.shape[0], loaded_img.shape[1], 1), 255, dtype=np.uint8)
                # loaded_img = np.concatenate((loaded_img, alpha), axis=2)
            if len(loaded_img.shape) == 3 and loaded_img.shape[2] in (3, 4):
                if loaded_img.shape[2] == 3:  # If image doesn't have an alpha channel
                    alpha = np.full((loaded_img.shape[0], loaded_img.shape[1], 1), 255, dtype=np.uint8)
                    loaded_img = np.concatenate((loaded_img, alpha), axis=2)
        else:
            loaded_img = np.array(img)
            
        self.card_elements[last_key] = loaded_img
        
        return self
    
    def get_asset(self, key_path:str)->object:
        """retrieves stored assets
        
        Returns Image object corresponding to key
        """
        found_image = self.card_elements
        
        for key in key_path.split("."):
            found_image = found_image[key]

        return Image.fromarray(found_image)

    def resize(self, key_path, height:float=None, width:float=None, keep_aspect_ratio:bool=True)->object:
        """resizes loaded assets"""
        image = self.get_asset(key_path)  # Assuming you have a method to retrieve images
        
        # Convert NumPy array to a Pillow Image
        pillow_image = image
        
        if keep_aspect_ratio:
            
            # Get the original width and height
            original_width, original_height = pillow_image.size
            
            # Calculate aspect ratio
            aspect_ratio = original_width / original_height
            
            if width is None and height is not None:
                # Calculate width based on the desired height and aspect ratio
                width = int(height * aspect_ratio)
            elif height is None and width is not None:
                # Calculate height based on the desired width and aspect ratio
                height = int(width / aspect_ratio)
        
            # Resize the image using Pillow
            pillow_image = pillow_image.resize((width, height))
            
            # Convert back to NumPy array
            resized_image = np.array(pillow_image)
        else:
            # Resize without maintaining aspect ratio
            resized_image = pillow_image.resize((width, height))
        
        # Assuming you have a method to load assets using Pillow
        self.load_asset(key_path, resized_image)
        
        return self
    
    def overlay(self, base_image_path:str, overlay_key_path:str, pos_x:float=0, pos_y:float=0):
        """overlay two images and positions them relatively.
        stores the final image as Image object in the base_image_path"""

        # Load the base image
        base_image = self.get_base_image() if base_image_path == "__base__" else self.get_asset(base_image_path)
        
        # Load the overlay image using load_asset method
        overlay_image = self.get_asset(overlay_key_path)
        
        # Paste the overlay image onto the base image at the specified position
        base_image.paste(overlay_image, (pos_x, pos_y), overlay_image)
                
        self.load_asset(base_image_path, base_image)
        
        return self
    
    def save_to_base_image(self, key_path:str):
        """saves asset to base image"""
        self.overlay("__base__", key_path)
    
    def factory_reset(self)->None:
        """factory reset all the loaded assets"""
        self.card_width = 822 # pixel
        self.card_height = 1122 # pixel
        
        self.card_elements = {}
        self._base = None
        
    def show_image(self, key_path:str)->None:
        """displays loaded images"""
        asset = self.get_asset(key_path)
        asset.show()
        
    def get_asset_list(self):
        """gets names of loaded assets and returns a list"""
        return tuple( name for name in self.card_elements.keys())
    
    def show_finalized_card(self):
        self.get_base_image().show()
    
    @base_exists
    def dump_card(self, output_path:str, output_fimename:str)->None:
        """outputs the resulting image to a given directory"""
        base_image = self.card_elements.get('base_image')  # Assuming 'base_image' is stored in card_elements
        
        if base_image is None:
            raise ValueError("Base image not found. Please set the base image first.")
        
        # Construct the complete output path
        output_complete_path = os.path.join(output_path, output_filename)
        
        # Save the base image to the specified directory
        base_image.save(output_complete_path)