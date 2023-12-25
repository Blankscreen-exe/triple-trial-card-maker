from os import path
import json
from datetime import datetime as dt
import numpy as np
import cv2
 
class TTCardMaker:
    
    def __init__(self):
        self.config = None
        self.output_dir = path.join(".", "")
        
        # Poker game card size
        self.card_width = 822 # pixel
        self.card_height = 1122 # pixel
        
        self.POSITION_CONFIG = {
            "arrow_heads": {
                "up": (0, 0),
                "down": (0, 0),
                "left": (0, 0),
                "right": (0, 0)
            },
            "avatar": (0, 0),
            "char_title": (0, 0),
            "bg": {
                "red": (0, 0),
                "blue": (0, 0)
            },
            "border": (0, 0),
            "rarity": (0, 0),
            "stats": {
                "top": (0, 0),
                "bottom": (0, 0),
                "left": (0, 0),
                "right": (0, 0),
            },
            "logo": (0, 0)
        }
        
        self.SIZE_CONFIG = {
            "arrow_heads": 000,
            "char_title": 000,
            "rarity": 000,
            "stats": 000,
            "logo": 000
        }
        
        self._card_elements = {
            "arrow_heads": {
                "up": None,
                "down": None,
                "left": None,
                "right": None
            },
            "avatar": None,
            "char_title": None,
            "bg": {
                "red": None,
                "blue": None
            },
            "border": None,
            "rarity": None,
            "stats": {
                "top": None,
                "bottom": None,
                "left": None,
                "right": None,
            },
            "logo": None
        }
        
    def read_config(self, config):
        """Used to read the config dictionary for cards"""
        if not self.validate_config(self._card_elements, config):
            raise KeyError("dictionary keys do not match")
        
        self._card_elements['arrow_heads']['up'] = self.read_image(config['arrow_heads']['up'])
        
        self._card_elements = config
        
        return self
        
    def validate_config(self, dict1, dict2):
        """Recursively check if two dictionaries and their nested dictionaries have the same keys"""
        if isinstance(dict1, dict) and isinstance(dict2, dict):
            keys1 = set(dict1.keys())
            keys2 = set(dict2.keys())

            if keys1 != keys2:
                return False

            for key in keys1:
                if not validate_config(dict1[key], dict2[key]):
                    return False

        return True
    
    def validate_key(self, dic:str, find_key:str) -> bool:
        """Recursively validates given key w.r.t category"""
        
        if find_key in dic:
            return True
        
        for key in dic.keys():
            if not self.validate_key(dic[key], find_key):
                return False
        return True
    
    def validate_val(self) -> bool:
        """Recursilvely validates that all values are not None"""
        for key, value in dictionary.items():
            if value is not None:
                return True
            if isinstance(value, dict) and has_non_none_value(value):
                return True
        return False
        
    def read_image(self, img_key: str) -> object:
        """Reads images using opencv"""
        try:
            return cv2.imread(img_key)
        except:
            return 
        
    def img_path_gen(self, type, img_name) -> str:
        """Generates image string path based on the type provided"""
        asset_folder = "Assets"
        if type=="bg":
            return path.join(asset_folder, "bg", img_name)
        elif type=="avatar":
            return path.join(asset_folder, "avatar", img_name)
        elif type=="arrowhead":
            return path.join(asset_folder, "arrowhead", img_name)
        elif type=="logo":
            return path.join(asset_folder, "logo", img_name)
        elif type=="stats":
            return path.join(asset_folder, "stats", img_name)
        elif type=="border":
            return path.join(asset_folder, "border", img_name)
    
    def base_card_generator(self, height=None, width=None):
        """Generates base card to draw upon"""
        if height is None:
            height = self.card_height
        
        if width is None:
            width = self.card_width
            
        return np.zeros((height, width, 3), dtype=np.uint8)
    
    def output_name_generator(self, char_name, team, star_count):
        """Generates output names for the finalized cards"""
        char_name = char_name.strip().replace(" ","_")
        team = team.strip().replace(" ","_")
        star_count = star_count.strip().replace(" ","_")
        timestamp = dt.now().strftime("%d_%m_%Y_%H:%M")
        return f"{char_name}-{team}-{star_count}-{timestamp}"
    
    def avatar_extractor(self):
        """Extracts the avatar from a picture by trimming the white spaces of transparent surrounding areas and returns the rectangular shape with the character inside. the returned image has a padding of 4% on all borders"""
        
        # Load the image with an avatar
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

        # Check if the image has an alpha channel
        if image.shape[2] == 4:
            # Extract the alpha channel
            alpha_channel = image[:, :, 3]

            # Find the coordinates of the non-zero (non-transparent) pixels
            non_zero_coords = np.column_stack(np.where(alpha_channel > 0))

            # Calculate the bounding box of non-zero pixels
            x, y, w, h = cv2.boundingRect(non_zero_coords)

            # Add a 4% padding to the bounding box
            padding_percent = 0.04
            padding_x = int(w * padding_percent)
            padding_y = int(h * padding_percent)
            x -= padding_x
            y -= padding_y
            w += 2 * padding_x
            h += 2 * padding_y

            # Crop the image to the bounding box with padding
            avatar = image[y:y + h, x:x + w]

            return avatar

        else:
            raise ValueError("The input image does not have an alpha channel (transparency).")
    
    def resize_element(self, image:cv2, height:int, width:int = None, keep_aspect_ratio=True) -> cv2:
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
        result_image = base_image.copy()

        # Overlay the element onto the result image at the specified position
        result_image[pos_y:pos_y + image.shape[0], pos_x:pos_x + image.shape[1]] = image

        return result_image
    
    def convert_to_png(input_image_path, output_image_path):
        """Converts an image to PNG format."""
        
        # Read the input image
        image = cv2.imread(input_image_path)

        # Ensure that the image was successfully loaded
        if image is not None:
            # Convert the image to PNG format and return it as a NumPy array
            _, buffer = cv2.imencode(".png", image)
            png_image = np.array(buffer).tobytes()
            return png_image
        else:
            raise ValueError("Failed to read the input image.")
            
    def get_rarity(self, rarity):
        """Extracts the star combination based on the rarity number"""
        
        if rarity < 1 or rarity > 5:
            raise ValueError("rarity must be between 1 and 5.")

        # Load the filled and empty star images
        filled_star = Image.open(os.path.join(self.stars_directory, 'star_fill.png'))
        empty_star = Image.open(os.path.join(self.stars_directory, 'star_empty.png'))

        # Ensure the images have the same dimensions
        if filled_star.shape != empty_star.shape:
            raise ValueError("The filled and empty star images should have the same dimensions.")

        # Create an array of images
        images = [filled_star] * rarity + [empty_star] * (5 - rarity)

        # Concatenate the images horizontally to create the sequence
        star_sequence = np.hstack(images)

        return star_sequence
    
    def get_dimensions(self, image:cv2) -> tuple:
        """Returns dimensions of a cv2 image as tuple"""
        return image.shape
        
    def compile(self):
        """Compiles the layers into one single card image"""
        
    
    def dump_card(self):
        """Dumps the final card in the output directory"""
        pass
    
    
if __name__=="__main__":
    from pprint import pprint as pp
    makyr = TTCardMaker()
    
    # pp(makyr.read_config())
    
    img_path = makyr.img_path_gen("logo", "feh.png")
    cv2.imshow("image", cv2.imread(img_path))
    # star_sequence = makyr.get_rarity(4)
    # print("DIMENSION ", star_sequence.shape)
    # cv2.imshow("Star Sequence", star_sequence)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    resized = makyr.resize_element(star_sequence, 50, keep_aspect_ratio=True)
    # print("DIMENSION ", resized.shape)
    # cv2.imshow("Star Sequence", resized)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()