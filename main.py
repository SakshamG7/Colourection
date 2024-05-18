"""
This is the main file of the project. The purpose is to use Saksham's Colour Balance Square within the image, and correct the colours of the image accordingly.
@author: Saksham Goel
@date: May 18, 2024
@version: 1.0
"""

# Imports
from PIL import Image, ImageDraw
import os

def colourection(ImageFileName: str, ColourBalanceSquare: list[int, int, int, int]):
    """
    This function takes an image file as input, and returns the image with the colours corrected.
    """
    # Open the image
    image = Image.open(ImageFileName)

    # Find the Nine Colours of the Square in the Image with Averages of each Colour within each smaller square
    ColourBalanceSquareColours = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(image.size[0] - ColourBalanceSquare[0], image.size[0] - ColourBalanceSquare[2]):
        c = 0
        for j in range(image.size[1] - ColourBalanceSquare[1], image.size[1] - ColourBalanceSquare[3]):
            pixelColour = image.getpixel((i, j))
            print(pixelColour)


Images = os.listdir("Images")
for image in Images:
    colourection("Images/" + image, [100, 100, 200, 200])

