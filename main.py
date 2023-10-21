import cv2
import numpy as np

def create_game_card(character_name, background_image, character_stats, card_border, character_avatar, character_logo, card_width, card_height):
    # Create a blank canvas with the specified dimensions
    card = np.zeros((card_height, card_width, 3), dtype=np.uint8)

    # Position and overlay each layer on the card
    # card[0:character_name.shape[0], 0:character_name.shape[1]] = character_name
    # card[0:background_image.shape[0], 0:background_image.shape[1]] = background_image
    # card[0:character_stats.shape[0], 0:character_stats.shape[1]] = character_stats
    # card[0:card_border.shape[0], 0:card_border.shape[1]] = card_border
    # card[0:character_avatar.shape[0], 0:character_avatar.shape[1]] = character_avatar
    # card[0:character_logo.shape[0], 0:character_logo.shape[1]] = character_logo

    # Resize each layer to fit the card dimensions
    character_name = cv2.resize(character_name, (card_width, card_height))
    background_image = cv2.resize(background_image, (card_width, card_height))
    character_stats = cv2.resize(character_stats, (card_width, card_height))
    card_border = cv2.resize(card_border, (card_width, card_height))
    character_avatar = cv2.resize(character_avatar, (card_width, card_height))
    character_logo = cv2.resize(character_logo, (card_width, card_height))

    # Position and overlay each layer on the card
    card = cv2.add(card, character_name)
    card = cv2.add(card, background_image)
    card = cv2.add(card, character_stats)
    card = cv2.add(card, card_border)
    card = cv2.add(card, character_avatar)
    card = cv2.add(card, character_logo)
    
    # Display the final game card
    cv2.imshow('Game Card', card)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Or save it to a file
    cv2.imwrite('game_card.png', card)

# Example usage:
# Load images and specify card dimensions
character_name = cv2.imread('./Assets/logo/feh.png') # TODO: need sample
background_image = cv2.imread('./Assets/bg/blue.png') 
character_stats = cv2.imread('./Assets/stats/5.png') 
card_border = cv2.imread('./Assets/stars/stars.png')
character_avatar = cv2.imread('./Assets/logo/feh.png') # TODO: need sample
character_logo = cv2.imread('./Assets/logo/feh.png') 
card_width, card_height = 200, 300

# Create the game card using the function
create_game_card(character_name, background_image, character_stats, card_border, character_avatar, character_logo, card_width, card_height)
