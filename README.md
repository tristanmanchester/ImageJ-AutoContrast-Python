# ImageJ-AutoContrast-Python

This repository contains a Python implementation of automatic histogram stretching based on a specific region of a greyscale image. The algorithm is inspired by the auto-contrast feature in ImageJ. Colour images will be converted to greyscale prior to adjustment.

## Overview

The `AutoHistStretch.py` script provides an easy way to apply histogram scaling to grayscale images (or colour images to be converted to greyscale). This script is particularly useful for enhancing the contrast of images based on a specific region, similar to the way ImageJ does it.

The algorithm is based on the ImageJ implementation, which can be found [here](https://imagej.nih.gov/ij/source/ij/plugin/frame/ContrastAdjuster.java).

## Features

- Automatic histogram stretching based on a specified region of an image.
- Option to specify the region as either pixel values or proportions of image dimensions.
- Supports various image types via the PIL library.

## Usage

To use the `AutoHistStretch.py` script, you can call the `histogram_scaling` function like this:

```python
from AutoHistStretch import histogram_scaling

# Example usage
image_path = "/path/to/original/image.jpg"
output_path = "/path/to/scaled/image.jpg"
x_coord = 0.4  # Replace with actual x-coordinate or proportion of the x-dimension 
y_coord = 0.5  # Replace with actual y-coordinate or proportion of the y-dimension
diameter = 0.2  # Replace with actual diameter or proportion of the x-dimension

histogram_scaling(image_path, output_path, centre_x_coord=x_coord, centre_y_coord=y_coord, hist_region_diameter=diameter, proportional=True)
```

## Parameters

- `image_path (str)`: The file path of the input image.
- `output_path (str)`: The file path to save the output image.
- `centre_x_coord (float or int)`: X-coordinate of the center of the region.
- `centre_y_coord (float or int)`: Y-coordinate of the center of the region.
- `hist_region_diameter (float or int)`: Diameter of the region for histogram calculation (as a proportion of the x-dimension when `proportional=True`).
- `proportional (bool)`: If True, coordinates and diameter are specified as proportions.
