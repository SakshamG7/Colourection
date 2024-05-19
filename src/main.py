"""
This is the main file of the project. The purpose is to use Saksham's Colour Balance Square within the image, and correct the colours of the image accordingly.
@author: Saksham Goel
@date: May 18, 2024
@version: 1.0
"""

# Imports
from PIL import Image, ImageDraw
import time
import os

def colourection(ImageFileName: str, ColourBalanceSquare: list[int, int, int, int]):
    """
    This function takes an image file as input, and returns the image with the colours corrected.
    """
    # Constants
    x1 = ColourBalanceSquare[0]
    y1 = ColourBalanceSquare[1]
    x2 = ColourBalanceSquare[2]
    y2 = ColourBalanceSquare[3]
    VARIANCE_LIMIT = 20
    SKIP_RATE_X = 1 + (x2 - x1) // 100
    SKIP_RATE_Y = 1 + (y2 - y1) // 100
    # Open the image
    image = Image.open(ImageFileName)
    image = image.convert("RGB")

    # Find the Nine Colours of the Square in the Image with Averages of each Colour within each smaller square
    ColourBalanceSquareColours = [[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                                  [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                                  [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]
    # Find the Average Colour of each of the Nine Squares, uses variance from each colour to another to determine if we are on the next colour to track within the general cordinates given
    current_colour_index_x = 0
    current_colour_index_y = 0
    nextY = False
    for y in range(y1, y2 - SKIP_RATE_Y, SKIP_RATE_Y):
        for x in range(x1, x2 - SKIP_RATE_X, SKIP_RATE_X):
            current_colour = image.getpixel((x, y))
            next_colour_x = image.getpixel((x + SKIP_RATE_X, y))
            next_colour_y = image.getpixel((x, y + SKIP_RATE_Y))

            # Update the Colour Variance
            colour_variance_x = abs(current_colour[0] - next_colour_x[0]) / (3 * 255) + abs(current_colour[1] - next_colour_x[1]) / (3 * 255) + abs(current_colour[2] - next_colour_x[2]) / (3 * 255)
            colour_variance_y = abs(current_colour[0] - next_colour_y[0]) / (3 * 255) + abs(current_colour[1] - next_colour_y[1]) / (3 * 255) + abs(current_colour[2] - next_colour_y[2]) / (3 * 255)
            colour_variance_x *= 100
            colour_variance_y *= 100

            # Update the Colour Balance Square Colours
            for i in range(3):
                if ColourBalanceSquareColours[current_colour_index_y][current_colour_index_x] == [0, 0, 0]:
                    ColourBalanceSquareColours[current_colour_index_y][current_colour_index_x] = list(current_colour)
                    break
                ColourBalanceSquareColours[current_colour_index_y][current_colour_index_x][i] += current_colour[i]
                ColourBalanceSquareColours[current_colour_index_y][current_colour_index_x][i] //= 2

            # Update the Colour Index
            if colour_variance_x > VARIANCE_LIMIT and nextY == False:
                current_colour_index_x += 1
                if current_colour_index_x == 3:
                    current_colour_index_x = 0
            if colour_variance_y > VARIANCE_LIMIT and current_colour_index_x == 2:
                nextY = True
        current_colour_index_x = 0
        if nextY:
            current_colour_index_y += 1
            if current_colour_index_y == 3:
                break
            nextY = False

    for i in range(3):
        print(ColourBalanceSquareColours[i])


Images = os.listdir("../Images")
for image in Images:
    if not (image.endswith(".jpg") or image.endswith(".jpeg") or image.endswith(".png")):
        continue
    print(image)
    colourection("../Images/" + image, [2648, 2648, 4688, 4688])

print("Saksham's Colour Balance Square Small.png")
colourection("../Saksham's Colour Balance Square Small.png", [0, 0, 750, 750])
