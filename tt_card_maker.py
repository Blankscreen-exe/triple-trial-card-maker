from os import path
import json
from datetime import datetime as dt
import numpy as np
import cv2
 
class TTCardMaker:
    
    def __init__(self):
        self.config = self.read_config()
        self.output_dir = path.join(".", "")
        self.config_file_path = path.join(".", "config.json")
        
        # Poker game card size
        self.card_width = 822 # pixel
        self.card_height = 1122 # pixel
        
        self.POSITION_CONFIG = {
            "char_name": (0, 0),
            "logo": (0, 0),
            "top": (0, 0),
            "left": (0, 0),
            "right": (0, 0),
            "bottom": (0, 0),
            "stars": (0, 0),
        }
        
    def read_config(self):
        """Used to read the json config for cards"""
        with open("./card_config.json", "r") as config:
            return json.load(config)
    
    def read_image(self, img_key: str) -> object:
        """Reads images using opencv"""
        return cv2.imread(img_key)
    
    def base_card_generator(self):
        """Generates base card to draw upon"""
        return np.zeros((self.card_height, self.card_width, 3), dtype=np.uint8)
    
    def output_name_generator(self, char_name, team, star_count):
        """Generates output names for the finalized cards"""
        char_name = char_name.strip().replace(" ","_")
        team = team.strip().replace(" ","_")
        star_count = star_count.strip().replace(" ","_")
        timestamp = dt.now().strftime("%d_%m_%Y_%H:%M")
        return f"{char_name}-{team}-{star_count}-{timestamp}"
    
    def avatar_extractor(self):
        """Extracts the avatar from a picture"""
        pass
    
    def resize_element(self, image:cv2, height:int, width:int, keep_aspect_ratio=True) -> cv2:
        """Resizes elements based on height by keeping the aspect ratio intact"""
        
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
            else:
                width = new_width

        # Resize the image using the calculated height and width
        resized_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)

        return resized_image
    
    def position_element(self, image, pos_x, pos_y):
        """Positions the given element(by its top-left most pixel) relative to the base card image"""
        
        # Generate the base card image
        base_image = self.base_card_generator()

        # Ensure that the position coordinates are within the bounds of the base_image
        if pos_x + image.shape[1] > base_image.shape[1] or pos_y + image.shape[0] > base_image.shape[0]:
            raise ValueError("Position coordinates exceed the dimensions of the base image.")

        # Copy the base image to prevent modifying the original
        # result_image = base_image.copy()

        # Overlay the element onto the result image at the specified position
        result_image[pos_y:pos_y + image.shape[0], pos_x:pos_x + image.shape[1]] = image

        return result_image
    
    def get_rarity(self, rarity):
        """Extracts the star combination based on the rarity number"""
        
        if rarity < 1 or rarity > 5:
            raise ValueError("rarity must be between 1 and 5.")

        # Load the filled and empty star images
        filled_star = cv2.imread('./Assets/stars/star_fill.png')
        empty_star = cv2.imread('./Assets/stars/star_empty.png')

        # Ensure the images have the same dimensions
        if filled_star.shape != empty_star.shape:
            raise ValueError("The filled and empty star images should have the same dimensions.")

        # Create an array of images
        images = [filled_star] * rarity + [empty_star] * (5 - rarity)

        # Concatenate the images horizontally to create the sequence
        star_sequence = np.hstack(images)

        return star_sequence
    
    def compile(self):
        """Compiles the layers into one single card image"""
        pass
    
    def dump_card(self):
        """Dumps the final card in the output directory"""
        pass
    
    
if __name__=="__main__":
    from pprint import pprint as pp
    makyr = TTCardMaker()
    
    pp(makyr.read_config())
    
    star_sequence = makyr.get_rarity(4)
    
    cv2.imshow("Star Sequence", star_sequence)
    cv2.waitKey(0)
    cv2.destroyAllWindows()