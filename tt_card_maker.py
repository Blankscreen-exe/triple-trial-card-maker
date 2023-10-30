from os import path
from datetime import datetime as dt

class TTCardMaker:
    
    def __init__(self):
        self.config = None # replace this with a caller function
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
        pass
    
    def read_image(self, path):
        """Reads images using opencv"""
        pass
    
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
    
    def resize_element(self, image, height, width, keep_aspect_ratio=True):
        """Resizes elements based on height byt keeping the aspect ratio"""
        pass
    
    def position_element(self, image, pos_x, pos_y):
        """Positions the given element(by its top-left most pixel) relative the base card"""
        pass
    
    def get_rarity(self):
        """Extracts the star combination based on the rarity number"""
        pass
    
    def compiler(self):
        """Compiles the images into one single card"""
        pass
    
    def dump_card(self):
        """Dumps the final card in the output directory"""
        pass