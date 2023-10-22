import cv2
import numpy as np

def trim_and_resize_character(character_image, card_width, card_height):
    # Convert the character image to grayscale
    character_gray = cv2.cvtColor(character_image, cv2.COLOR_BGR2GRAY)

    # Find the contours of the character in the image
    contours, _ = cv2.findContours(character_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour (the character) in the image
    if contours:
        max_contour = max(contours, key=cv2.contourArea)

        # Get the bounding rectangle of the character
        x, y, w, h = cv2.boundingRect(max_contour)

        # Crop the character
        character_cropped = character_image[y:y+h, x:x+w]

        # Calculate the scaling factor to fit the character within the card
        scale = min(card_width / w, card_height / h)

        # Resize the character while maintaining aspect ratio
        character_resized = cv2.resize(character_cropped, (int(w * scale), int(h * scale)))

        # Create a blank canvas with the card dimensions
        card = np.zeros((card_height, card_width, 3), dtype=np.uint8)

        # Calculate the position to center the character on the card
        x_offset = (card_width - character_resized.shape[1]) // 2
        y_offset = (card_height - character_resized.shape[0]) // 2

        # Place the character on the card
        card[y_offset:y_offset + character_resized.shape[0], x_offset:x_offset + character_resized.shape[1]] = character_resized

        return card

    else:
        print("No character found in the image.")
        return None

# Example usage:
# Load the character image and specify card dimensions
character_image = cv2.imread('character_image.png')
card_width, card_height = 200, 300

# Trim, resize, and reposition the character image
final_card = trim_and_resize_character(character_image, card_width, card_height)

if final_card is not None:
    # Display the final card
    cv2.imshow('Final Card', final_card)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Or save it to a file
    cv2.imwrite('final_card.png', final_card)
