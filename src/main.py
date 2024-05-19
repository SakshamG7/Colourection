"""
This is the main file of the project. The purpose is to use Saksham's Colour Balance Square within the image, and correct the colours of the image accordingly.
@author: Saksham Goel
@date: May 18, 2024
@version: 1.0
"""

# Imports
from PIL import Image
import os


def variance_square(ColourBalanceSquareColours) -> float:
    """
    This function takes the Colour Balance Square Colours and returns the variance of each colour to the next colour.
    """
    # Find the Variance of each Colour to the Next Colour
    CorrectColourBalanceSquareColours = [[[255,   0,   0], [255, 255,   0], [ 84,  84,  84]],
                                          [[255, 255, 255], [  0, 255,   0], [  0,   0,   0]],
                                          [[  0,   0, 255], [  0, 255, 255], [255,   0, 255]]]
    variance = 0
    for i in range(3):
        for j in range(3):
            for k in range(3):
                variance += abs(ColourBalanceSquareColours[i][j][k] - CorrectColourBalanceSquareColours[i][j][k]) / (3 * 255 * 9)
    return round(variance * 100, 2)


def variance_square_adjusted_colour(currentColour, currentColourBalanceSquareColours) -> list[int, int, int]:
    # Find the Corrected Colour
    CorrectColourBalanceSquareColours = [[[255,   0,   0], [255, 255,   0], [ 84,  84,  84]],
                                          [[255, 255, 255], [  0, 255,   0], [  0,   0,   0]],
                                          [[  0,   0, 255], [  0, 255, 255], [255,   0, 255]]]
    minVariance = 100000000
    colourBalanceX = 0
    colourBalanceY = 0
    for i in range(3):
        for j in range(3):
            variance = 0
            for k in range(3):
                variance += abs((currentColour[k] - currentColourBalanceSquareColours[i][j][k]))
            if abs(variance) < minVariance:
                colourBalanceX = j
                colourBalanceY = i
                minVariance = abs(variance)
    correct_colour = list(currentColour)
    for i in range(3):
        correct_colour[i] += correct_colour[i] + abs(CorrectColourBalanceSquareColours[colourBalanceY][colourBalanceX][i] + currentColourBalanceSquareColours[colourBalanceY][colourBalanceX][i])
        correct_colour[i] //= 4
    return correct_colour


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
    CORRECTION_LIMIT = 32
    SKIP_RATE_X = 1 + (x2 - x1) // 75
    SKIP_RATE_Y = 1 + (y2 - y1) // 75
    # Open the image
    image = Image.open("../Images/" + ImageFileName)
    image = image.convert("RGB")
    imageColourData = list(image.getdata())

    # Find the Nine Colours of the Square in the Image with Averages of each Colour within each smaller square
    ColourBalanceSquareColours = [[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                                  [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                                  [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]
    # Find the Average Colour of each of the Nine Squares, uses variance from each colour to another to determine if we are on the next colour to track within the general cordinates given
    # Also keeps correcting the colour balance square colours to the correct colours
    while True:
        current_colour_index_x = 0
        current_colour_index_y = 0
        nextY = False
        for y in range(y1, y2 - SKIP_RATE_Y, SKIP_RATE_Y):
            for x in range(x1, x2 - SKIP_RATE_X, SKIP_RATE_X):
                current_colour = imageColourData[y * image.width + x]
                next_colour_x = imageColourData[y * image.width + x + SKIP_RATE_X]
                next_colour_y = imageColourData[(y + SKIP_RATE_Y) * image.width + x]

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

        # for i in range(3):
        #     print(ColourBalanceSquareColours[i])
        # print()
        v1 = variance_square(ColourBalanceSquareColours)
        print(v1)
        if abs(v1) < CORRECTION_LIMIT:
            image.save("../Output/Corrected_" + ImageFileName.replace("/", "_"))
            break
        # Correct the Colour Balance Square Colours
        for y in range(0, image.height, 1):
            for x in range(0, image.width, 1):
                current_colour = imageColourData[y * image.width + x]
                corrected_colour = variance_square_adjusted_colour(current_colour, ColourBalanceSquareColours)
                imageColourData[y * image.width + x] = tuple(corrected_colour)
    image.putdata(imageColourData)


Images = os.listdir("../Images")
for image in Images:
    if not (image.endswith(".jpg") or image.endswith(".jpeg") or image.endswith(".png")):
        continue
    squareData = list(map(int, image.split("-")[0:4]))
    print(image, squareData)
    colourection(image, squareData)

print("Saksham's Colour Balance Square Small.png")
colourection("../Saksham's Colour Balance Square Small.png", [0, 0, 750, 750])
