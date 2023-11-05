from os import path
import json
from datetime import datetime as dt
import numpy as np
import cv2
 
 
# REF: https://stackoverflow.com/questions/36921496/how-to-join-png-with-alpha-transparency-in-a-frame-in-realtime/37198079#37198079
 
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
        self.output_dir = path.join(".", "")
        
        # default vars
        
        # Poker game card size
        self.card_width = 822 # pixel
        self.card_height = 1122 # pixel
        
        self.card_elements = {}
        self._base = None
        
    def generate_card_base(self, height=None, width=None):
        """Generates base card to draw upon"""
        if height is None:
            height = self.card_height
        
        if width is None:
            width = self.card_width
            
        # white card base
        self._base = np.zeros((height, width, 4),  dtype=np.uint8)
        self._base[:, :, 0:3] = 255  # Set RGB channels to white (255, 255, 255)
        self._base[:, :, 3] = 255  # Set the alpha channel to fully opaque (255)
        
        return self
    
    @base_exists
    def get_base_image(self):
        return self._base
    
    @base_exists
    def load_asset(self, key_path, img):
        keys = key_path.split('.')

        for key in keys[:-1]:
            if key not in self.card_elements:
                self.card_elements[key] = {}
            self.card_elements = self.card_elements[key]

        last_key = keys[-1]
        
        if isinstance(img, str):
            loaded_img = cv2.imread(img, cv2.IMREAD_UNCHANGED)
            print(loaded_img)
            # loaded_img = loaded_img[:, :, 0:3] = 0
            # loaded_img = loaded_img[:, :, 3] = 0
            print("CONVERTED TO PNG")
        else:
            loaded_img = img
            
        self.card_elements[last_key] = loaded_img
        
        return self
    
    # @asset_exists
    def get_asset(self, key_path):
        found_image = self.card_elements
        
        for key in key_path.split("."):
            found_image = found_image[key]
            
        return found_image
    
    # @asset_exists
    def resize(self, key_path, height=None, width=None, keep_aspect_ratio=True):
        
        image = self.get_asset(key_path)
        
        if keep_aspect_ratio:
            # Calculate the aspect ratio of the original image
            original_height, original_width = image.shape[:2]
            aspect_ratio = original_width / original_height

            if width is None:
                # Calculate the width based on the desired height and aspect ratio
                new_width = int(height * aspect_ratio)
            else:
                # Calculate the height based on the desired width and aspect ratio
                new_height = int(width / aspect_ratio)

            if height is None:
                height = new_height
                
            if width is None:
                width = new_width
                
        # Resize the image using the calculated height and width
        resized_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)
        
        self.load_asset(key_path, resized_image)
        
        return self
    
    def position(self, x, y):
        return self
    
    # @asset_exists
    @base_exists
    def overlay(self, key_path, pos_x=0, pos_y=0):
        base_image = self._base
        
        overlay_image = self.get_asset(key_path)
        # print(overlay_image)
        # # Ensure that the position coordinates are within the bounds of the base_image
        # if pos_x + image.shape[1] > base_image.shape[1] or pos_y + image.shape[0] > base_image.shape[0]:
        #     raise ValueError("Position coordinates exceed the dimensions of the base image.")

        # # Copy the base image to prevent modifying the original
        # result_image = base_image.copy()

        # # Overlay the element onto the result image at the specified position
        # result_image[pos_y:pos_y + image.shape[0], pos_x:pos_x + image.shape[1]] = image
        # return self
    
        # Ensure that the images have the same number of channels (e.g., 3 for RGB)
        print(overlay_image.shape[-1])
        print(base_image.shape[-1])
        if base_image.shape[-1] != overlay_image.shape[-1]:
            raise ValueError("Image channels do not match.")

        # Create a copy of the base image to avoid modifying the original
        combined_image = base_image.copy()

        # Get the height and width of the overlay image
        overlay_height, overlay_width = overlay_image.shape[:2]

        # Calculate the region of interest (ROI) for overlay
        roi = combined_image[pos_y:pos_y + overlay_height, pos_x:pos_x + overlay_width]

        # Overlay the image on the ROI
        combined_image[pos_y:pos_y + overlay_height, pos_x:pos_x + overlay_width] = overlay_image
        self._base = combined_image
        return self
    
    def output(self):
        pass
    
    
if __name__=="__main__":
    cmk = CardMaker().generate_card_base()
    
    asset = cmk.load_asset(key_path="border", img="./Assets/border/gold_small.png") 
            
    asset = asset.load_asset(key_path="logo", img="./Assets/logo/feh.png")
    asset = asset.resize(key_path="logo", width=400)
    asset_to_show = asset.get_asset(key_path="logo")
    
    cv2.imshow("card", asset.get_asset(key_path="border"))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(asset_to_show.shape)
    asset = asset.overlay("border")
    asset = asset.overlay("logo",
                        pos_x=250-(asset_to_show.shape[1]//2), 
                          pos_y=250-(asset_to_show.shape[0]//2)
                        )
    cv2.imshow("card", asset.get_base_image())
    cv2.waitKey(0)
    cv2.destroyAllWindows()