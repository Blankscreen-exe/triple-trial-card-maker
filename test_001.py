from card_factory import CardMaker
from PIL import Image

# Initialize the CardMaker class
card_maker = CardMaker()

card_maker.generate_card_base()
print("TYPE 1", type(card_maker.get_base_image()))

card_maker.load_asset("border", "Assets\\border\\gold.png")

border = card_maker.get_asset("border")
print("TYPE 2", type(card_maker.get_asset("border")))



# card_maker.show_image("border")

# ============================

card_maker.load_asset("bg", "Assets\\bg\\blue.png")
# card_maker.load_asset("logo", "Assets\\logo\\feh.png")
# # card_maker.load_asset("bg", "Assets\\bg\\blue.png")
# # card_maker.load_asset("bg", "Assets\\bg\\blue.png")

asset = card_maker.get_asset("bg")
# print(asset)

# card_maker.show_image("bg")

# ============================

# card_maker.resize("border",1122*2+50,822*2-50,False)
card_maker.overlay("bg", "border")
# # card_maker.overlay("bg", "logo")

card_maker.show_image("bg")

# card_maker.save_to_base_image("bg")

# asset = card_maker.show_finalized_card()
# # asset = Image.fromarray(card_maker.get_asset("bg")).show()
# asset =  Image.fromarray(card_maker.get_base_image()).show()
# print(asset)

# ============================

# # Load necessary images
# card_maker.load_asset("background", "./assets/background.png")
# card_maker.load_asset("avatar", "./assets/avatar.png")
# card_maker.load_asset("frame", "./assets/frame.png")
# card_maker.load_asset("rarity_stars", "./assets/rarity_stars.png")

# # Resize images as needed
# card_maker.resize("background", height=1122, width=822)
# card_maker.resize("avatar", height=200, width=200)
# card_maker.resize("frame", height=300, width=300)
# card_maker.resize("rarity_stars", width=400)  # Maintains aspect ratio

# # Overlay images onto the base image
# card_maker.overlay("./assets/background.png", "avatar", pos_x=100, pos_y=100)
# card_maker.overlay("./assets/background.png", "frame", pos_x=50, pos_y=50)
# card_maker.overlay("./assets/background.png", "rarity_stars", pos_x=50, pos_y=800)

# # Get the final base image
# final_image = card_maker.get_base_image()

# # Output the resulting image
# output_path = "./output/"
# output_filename = "my_custom_card.png"
# card_maker.dump_card(output_path, output_filename)