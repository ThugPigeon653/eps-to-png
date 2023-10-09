# check for unused import statements...
import turtle
import math
import random
import re
import numpy as np
from PIL import Image, ImageDraw

class Converter():
    @staticmethod
    def convert_to_png(ps_path, output_path="output_image.png"):
        with open(ps_path, 'r') as ps_file:
            lines = ps_file.readlines()
    
        # Create a list to store the extracted points
        points = []
    
        # Extract the points from the PS content
        for line in lines:
            if "lineto" in line:
                # Extract the coordinates from the line
                coordinates = line.split()[:2]
                if len(coordinates) == 2:
                    try:
                        x, y = map(float, coordinates)
                        points.append((x, y))
                    except ValueError:
                        pass
    
        # Find the minimum and maximum coordinates
        min_x = min(point[0] for point in points)
        max_x = max(point[0] for point in points)
        min_y = min(point[1] for point in points)
        max_y = max(point[1] for point in points)
    
        # Calculate the width and height of the image
        width = int(max_x - min_x) + 1
        height = int(max_y - min_y) + 1
    
        # Create a white NumPy array as the canvas
        canvas = np.zeros((height, width, 3), dtype=np.uint8) + 255  # Initialize with white (255, 255, 255)
    
        # Create a PIL ImageDraw object to draw on the canvas
        draw = ImageDraw.Draw(Image.fromarray(canvas))
    
        # Initialize variables to keep track of the current point
        current_x, current_y = None, None
    
        # Create a list to store the transformed coordinates
        transformed_coordinates = []
    
        for x, y in points:
            # Transform the coordinates to match the canvas
            transformed_x = int(x - min_x)
            transformed_y = int(y - min_y)
            transformed_coordinates.append((transformed_x, transformed_y))
    
        # Create a white image with the same size as the canvas
        line_image = Image.new('RGB', (width, height), (255, 255, 255))
    
        # Create a PIL ImageDraw object to draw on the line image
        draw_lines = ImageDraw.Draw(line_image)
    
        # Loop over all transformed coordinates and add them to the line image
        for i in range(100, len(transformed_coordinates) - 100):  # Skip the first and last points
            x, y = transformed_coordinates[i]
            # If there's a previous point, draw a green line from it to the current point
            if current_x is not None and current_y is not None:
                draw_lines.line(
                    [(current_x, current_y), (x, y)],
                    fill=(0, 255, 0), width=2
                )
    
            # Update the current point
            current_x, current_y = x, y
    
        # Composite the line image onto the canvas
        canvas_image = Image.fromarray(canvas)
        canvas_image.paste(line_image, (0, 0))
    
        # Save the image as PNG
        canvas_image.save(output_path, 'PNG')
