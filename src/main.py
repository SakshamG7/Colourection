"""
This is the main file of the project. The purpose is to use Saksham's Colour Balance Square within the image, and correct the colours of the image accordingly.
@author: Saksham Goel
@date: May 18, 2024
@version: 1.0
"""

# Imports
from PIL import Image
import os
import time


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


def variance_square_adjusted_colour(currentColour, suroundedPixels, currentColourBalanceSquareColours) -> list[int, int, int]:
    # Find the Corrected Colour
    CorrectColourBalanceSquareColours = [[[255,   0,   0], [255, 255,   0], [ 84,  84,  84]],
                                          [[255, 255, 255], [  0, 255,   0], [  0,   0,   0]],
                                          [[  0,   0, 255], [  0, 255, 255], [255,   0, 255]]]
    minVariance = 100000000
    colourBalanceX = 0
    colourBalanceY = 0
    averageColour = list(currentColour)
    correct_colour = averageColour.copy()
    for pixel in suroundedPixels:
        for i in range(3):
            averageColour[i] += pixel[i]
            averageColour[i] /= 2
    for i in range(3):
        for j in range(3):
            variance = 0
            for k in range(3):
                variance += abs(averageColour[k] - currentColourBalanceSquareColours[i][j][k]) / 3
            if abs(variance) < minVariance:
                colourBalanceX = j
                colourBalanceY = i
                minVariance = abs(variance)
    for i in range(3):
        correct_colour[i] += averageColour[i]
        correct_colour[i] /= 2
        correct_colour[i] += CorrectColourBalanceSquareColours[colourBalanceY][colourBalanceX][i]
        correct_colour[i] /= 2
    for i in range(3):
        if correct_colour[i] < 0:
            correct_colour[i] = 0
        if correct_colour[i] > 255:
            correct_colour[i] = 255
        correct_colour[i] = round(correct_colour[i])
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
    VARIANCE_LIMIT = 70
    CORRECTION_LIMIT = 5
    SKIP_RATE_X = 1# + (x2 - x1) // 100
    SKIP_RATE_Y = 1# + (y2 - y1) // 100
    # Open the image
    image = Image.open("../Images/" + ImageFileName)
    image = image.convert("RGB")
    imageColourData = list(image.getdata())
    backUpImageColourData = list(imageColourData).copy()

    # Find the Nine Colours of the Square in the Image with Averages of each Colour within each smaller square
    ColourBalanceSquareColours = [[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                                  [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                                  [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]
    # Find the Average Colour of each of the Nine Squares, uses variance from each colour to another to determine if we are on the next colour to track within the general cordinates given
    # Also keeps correcting the colour balance square colours to the correct colours
    oldV1 = 0
    ins = 0
    minIns = 100
    minVar = 100
    while True:
        current_colour_index_x = 0
        current_colour_index_y = 0
        nextY = False
        for y in range(y1 + SKIP_RATE_Y, y2 - SKIP_RATE_Y, SKIP_RATE_Y):
            for x in range(x1 + SKIP_RATE_Y, x2 - SKIP_RATE_X, SKIP_RATE_X):
                current_colour = imageColourData[y * image.width + x]
                next_colour_x = imageColourData[y * image.width + x + SKIP_RATE_X]
                next_colour_y = imageColourData[(y + SKIP_RATE_Y) * image.width + x]

                # Update the Colour Variance
                colour_variance_x = 0
                colour_variance_y = 0
                for i in range(3):
                    colour_variance_x += abs(current_colour[i] - next_colour_x[i])
                    colour_variance_y += abs(current_colour[i] - next_colour_y[i])
                colour_variance_x /= 3
                colour_variance_y /= 3

                # Update the Colour Index
                if colour_variance_x > VARIANCE_LIMIT and nextY == False:
                    current_colour_index_x += 1
                    print('X', colour_variance_x, colour_variance_y, current_colour, next_colour_x, next_colour_y)
                    time.sleep(0.1)
                if colour_variance_y > VARIANCE_LIMIT and current_colour_index_x == 2:
                    nextY = True

                # Update the Colour Balance Square Colours
                for i in range(3):
                    if ColourBalanceSquareColours[current_colour_index_y][current_colour_index_x] == [0, 0, 0]:
                        ColourBalanceSquareColours[current_colour_index_y][current_colour_index_x] = list(current_colour)
                        break
                    ColourBalanceSquareColours[current_colour_index_y][current_colour_index_x][i] += current_colour[i]
                    ColourBalanceSquareColours[current_colour_index_y][current_colour_index_x][i] //= 2

            current_colour_index_x = 0
            if nextY:
                current_colour_index_y += 1
                # print('Y', colour_variance_x, colour_variance_y, current_colour, next_colour_x, next_colour_y)
                # time.sleep(1)
                nextY = False

        for i in range(3):
            print(ColourBalanceSquareColours[i])
        print()
        v1 = variance_square(ColourBalanceSquareColours)
        if v1 != oldV1:
            print('# ' + str(ins + 1) + ':', "Variance Level:", str(v1) + '%,', "Difference:", round(abs(v1 - oldV1), 2))
            oldV1 = v1
            if v1 < minVar:
                minVar = v1
                minIns = ins
        if abs(v1) < CORRECTION_LIMIT or ins > 25:
            imageColourData = backUpImageColourData.copy()
            for i in range(minIns):
                for y in range(1, image.height - 1, 1):
                    for x in range(1, image.width - 1, 1):
                        current_colour = imageColourData[y * image.width + x]
                        suroundedPixels = [imageColourData[y * image.width + x + 1], imageColourData[y * image.width + x - 1], imageColourData[(y + 1) * image.width + x], imageColourData[(y - 1) * image.width + x], imageColourData[(y + 1) * image.width + x + 1], imageColourData[(y - 1) * image.width + x - 1], imageColourData[(y + 1) * image.width + x - 1], imageColourData[(y - 1) * image.width + x + 1]]
                        corrected_colour = variance_square_adjusted_colour(current_colour, suroundedPixels, ColourBalanceSquareColours)
                        imageColourData[y * image.width + x] = tuple(corrected_colour)
            image.putdata(imageColourData)
            image.save("../Output/Corrected_" + ImageFileName.replace("/", "_"))
            break
        # Correct the Colour Balance Square Colours
        for y in range(y1 + SKIP_RATE_Y, y2 - SKIP_RATE_Y, SKIP_RATE_Y):
            for x in range(x1 + SKIP_RATE_X, x2 - SKIP_RATE_X, SKIP_RATE_X):
                current_colour = imageColourData[y * image.width + x]
                suroundedPixels = [imageColourData[y * image.width + x + 1], imageColourData[y * image.width + x - 1], imageColourData[(y + 1) * image.width + x], imageColourData[(y - 1) * image.width + x], imageColourData[(y + 1) * image.width + x + 1], imageColourData[(y - 1) * image.width + x - 1], imageColourData[(y + 1) * image.width + x - 1], imageColourData[(y - 1) * image.width + x + 1]]
                corrected_colour = variance_square_adjusted_colour(current_colour, suroundedPixels, ColourBalanceSquareColours)
                imageColourData[y * image.width + x] = tuple(corrected_colour)
        ins += 1


# Images = os.listdir("../Images")
# for image in Images:
#     if not (image.endswith(".jpg") or image.endswith(".jpeg") or image.endswith(".png")):
#         continue
#     squareData = list(map(int, image.split("-")[0:4]))
#     print(image, squareData)
#     colourection(image, squareData)

print("Saksham's Colour Balance Square Small.png")
colourection("../Saksham's Colour Balance Square Small.png", [0, 0, 750, 750])
