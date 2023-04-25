import csv

import cv2
import numpy as np
import os
from collections import Counter

# Set the path to the folder containing the images
folder_path = "./Fotofolder"

# Define the RGB value of the white background to filter out
background_color = (255, 255, 255)

# Initialize a list to store the dominant color of each image
dominant_colors = []


# Define a function to generify the colors
def generify_color(color):
    generified = tuple([int(round(c / 64) * 64) for c in color])
    return generified


color_dict = {(0, 0, 0): "Black", (0, 0, 64): "Navy", (0, 0, 128): "Navy", (0, 0, 192): "Blue", (0, 0, 256): "Blue",
              (0, 64, 0): "Green", (0, 64, 64): "Teal", (0, 64, 128): "Teal", (0, 64, 192): "Light Blue",
              (0, 64, 256): "Light Blue", (0, 128, 0): "Green", (0, 128, 64): "Green", (0, 128, 128): "Teal",
              (0, 128, 192): "Light Blue", (0, 128, 256): "Light Blue", (0, 192, 0): "Green", (0, 192, 64): "Green",
              (0, 192, 128): "Green", (0, 192, 192): "Light Blue", (0, 192, 256): "Light Blue", (0, 256, 0): "Green",
              (0, 256, 64): "Green", (0, 256, 128): "Light Blue", (0, 256, 192): "Light Blue", (0, 256, 256): "Cyan",
              (64, 0, 0): "Maroon", (64, 0, 64): "Purple", (64, 0, 128): "Purple", (64, 0, 192): "Blue",
              (64, 0, 256): "Blue", (64, 64, 0): "Olive", (64, 64, 64): "Gray", (64, 64, 128): "Gray",
              (64, 64, 192): "Blue", (64, 64, 256): "Blue", (64, 128, 0): "Olive", (64, 128, 64): "Gray",
              (64, 128, 128): "Gray", (64, 128, 192): "Blue", (64, 128, 256): "Blue", (64, 192, 0): "Olive",
              (64, 192, 64): "Gray", (64, 192, 128): "Blue", (64, 192, 192): "Blue", (64, 192, 256): "Light Blue",
              (64, 256, 0): "Olive", (64, 256, 64): "Gray", (64, 256, 128): "Light Blue", (64, 256, 192): "Light Blue",
              (64, 256, 256): "Cyan", (128, 0, 0): "Maroon", (128, 0, 64): "Purple", (128, 0, 128): "Purple",
              (128, 0, 192): "Purple", (128, 0, 256): "Purple", (128, 64, 0): "Brown", (128, 64, 64): "Rosy Brown",
              (128, 64, 128): "Purple", (128, 64, 192): "Purple", (128, 64, 256): "Purple", (128, 128, 0): "Olive",
              (128, 128, 64): "Olive", (128, 128, 128): "Gray", (128, 128, 192): "Purple", (128, 128, 256): "Blue",
              (128, 192, 0): "Olive", (128, 192, 64): "Olive", (128, 192, 128): "Gray", (128, 192, 192): "Purple",
              (128, 192, 256): "Blue", (128, 256, 0): "Olive", (128, 256, 64): "Olive", (128, 256, 128): "Purple",
              (128, 256, 192): "Blue", (128, 256, 256): "Light Blue", (192, 0, 0): "Maroon", (192, 0, 64): "Maroon",
              (192, 0, 128): "Purple", (192, 0, 192): "Purple", (192, 0, 256): "Purple", (192, 64, 0): "Brown",
              (192, 64, 64): "Brown", (192, 64, 128): "Purple", (192, 64, 192): "Purple", (192, 64, 256): "Purple",
              (192, 128, 0): "Olive", (192, 128, 64): "Olive", (192, 128, 128): "Gray", (192, 128, 192): "Purple",
              (192, 128, 256): "Blue", (192, 192, 0): "Olive", (192, 192, 64): "Olive", (192, 192, 128): "Gray",
              (192, 192, 192): "Silver", (192, 192, 256): "Blue", (192, 256, 0): "Olive", (192, 256, 64): "Olive",
              (192, 256, 128): "Purple", (192, 256, 192): "Blue", (192, 256, 256): "Light Blue", (256, 0, 0): "Maroon",
              (256, 0, 64): "Maroon", (256, 0, 128): "Purple", (256, 0, 192): "Purple", (256, 0, 256): "Purple",
              (256, 64, 0): "Brown", (256, 64, 64): "Brown", (256, 64, 128): "Purple", (256, 64, 192): "Purple",
              (256, 64, 256): "Purple", (256, 128, 0): "Orange", (256, 128, 64): "Orange", (256, 128, 128): "Purple",
              (256, 128, 192): "Purple", (256, 128, 256): "Purple", (256, 192, 0): "Olive", (256, 192, 64): "Olive",
              (256, 192, 128): "Purple", (256, 192, 192): "Purple", (256, 192, 256): "Purple",
              (256, 256, 0): "Spring Green", (256, 256, 64): "Teal", (256, 256, 128): "Light Sea Green",
              (256, 256, 192): "Silver", (256, 256, 256): "White", }

# Loop through each image in the folder
for filename in os.listdir(folder_path):
    # Load the image
    img_path = os.path.join(folder_path, filename)
    img = cv2.imread(img_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Threshold the image to create a mask of the white background
    _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

    # Invert the mask to create a mask of the foreground
    mask_inv = cv2.bitwise_not(mask)

    # Remove the white background color from the image
    img[mask == 255] = [0, 0, 0]

    # Extract the dominant color of the image and generify it
    pixels = np.float32(img.reshape(-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.1)
    _, labels, centers = cv2.kmeans(pixels, 1, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    dominant_color = generify_color(centers[0].astype(int))
    dominant_colors.append(dominant_color)

# Count the occurrence of each color in the list of generified dominant colors
color_counts = Counter(dominant_colors)

# Get the top 50 most recurring colors and their counts
top_50_colors = color_counts.most_common(40)

color_combined = []

for color, count in top_50_colors:
    if color_dict.get(color) in color_combined:
        color_combined[color_dict.get(color)] += count
    else:
        color_combined.append({'color': color_dict.get(color), 'count': count})


def merge_objects_by_attribute(arr, attribute):
    result = []
    visited_indexes = set()

    for i, obj1 in enumerate(arr):
        if i in visited_indexes:
            continue

        merged_obj = obj1.copy()

        for j, obj2 in enumerate(arr[i + 1:], i + 1):
            if obj1[attribute] == obj2[attribute]:
                merged_obj['count'] += obj2['count']
                # merged_obj.update(obj2)
                visited_indexes.add(j)

        result.append(merged_obj)

    return result


mmm = merge_objects_by_attribute(color_combined, "color")

for color in mmm:
    #print(color.get('color'))
    print("- {} ({} occurrences)".format(color.get('color'), color.get('count')))

# top_10_colors = color_counts.most_common(10)
with open('./colorOutput.csv', 'w', newline='') as file:
    reader = csv.DictReader(file)
    fieldnames = ['color', 'count']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for color in mmm:
        writer.writerow({"color": color.get('color'), "count": color.get('count')})
        # writer.writerows(mmm)