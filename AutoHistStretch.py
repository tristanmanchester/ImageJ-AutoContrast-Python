from PIL import Image
import numpy as np

def calculate_bounds(histogram, pixel_count, bin_size, hist_min):
    """
    Calculate the minimum and maximum pixel values for histogram scaling.
    
    Parameters:
    - histogram (array): The histogram of the image.
    - pixel_count (int): Total number of pixels in the region being considered.
    - bin_size (float): The size of each bin in the histogram.
    - hist_min (float): The minimum pixel value in the histogram.
    
    Returns:
    - min_val (float): Minimum pixel value for scaling.
    - max_val (float): Maximum pixel value for scaling.
    """
    limit = pixel_count // 10
    threshold = pixel_count // 5000
    hmin, hmax = -1, -1
    
    # Find the minimum pixel value for scaling
    for i, count in enumerate(histogram):
        if count > limit:
            continue
        if count > threshold:
            hmin = i
            break
            
    # Find the maximum pixel value for scaling
    for i, count in reversed(list(enumerate(histogram))):
        if count > limit:
            continue
        if count > threshold:
            hmax = i
            break

    min_val = hist_min + hmin * bin_size
    max_val = hist_min + hmax * bin_size
    
    return min_val, max_val

def histogram_scaling(image_path, output_path, centre_x_coord, centre_y_coord, hist_region_diameter, proportional=False):
    """
    Apply histogram scaling to an image based on a specified region.
    
    Parameters:
    - image_path (str): The file path of the input image.
    - output_path (str): The file path to save the output image.
    - centre_x_coord (float or int): X-coordinate of the center of the region.
    - centre_y_coord (float or int): Y-coordinate of the center of the region.
    - hist_region_diameter (float or int): Diameter of the region for histogram calculation.
    - proportional (bool): If True, coordinates and diameter are specified as proportions.
    
    Note:
    - When proportional=True, hist_region_diameter is a proportion of the x-dimension of the image.
    """
    with Image.open(image_path) as img:
        # Convert image to grayscale if it's not
        if img.mode not in ('L', 'I;16'):
            img = img.convert('L')
        
        width, height = img.size

        # Convert to pixel values if proportional=True
        if proportional:
            centre_x_coord = int(centre_x_coord * width)
            centre_y_coord = int(centre_y_coord * height)
            hist_region_diameter = int(hist_region_diameter * width)
        
        # Calculate cropping coordinates, ensuring they are within image boundaries
        half_diameter = hist_region_diameter // 2
        left = max(centre_x_coord - half_diameter, 0)
        top = max(centre_y_coord - half_diameter, 0)
        right = min(centre_x_coord + half_diameter, width)
        bottom = min(centre_y_coord + half_diameter, height)

        # Crop the specified region for histogram calculation
        crop_region = img.crop((left, top, right, bottom))

        # Compute histogram and statistics of the cropped region
        crop_array = np.array(crop_region)
        histogram, bin_edges = np.histogram(crop_array, bins=256)
        hist_min = bin_edges[0]
        bin_size = bin_edges[1] - bin_edges[0]
        pixel_count = crop_array.size

        # Calculate min and max pixel values for scaling the whole image
        min_val, max_val = calculate_bounds(histogram, pixel_count, bin_size, hist_min)

        # Apply histogram scaling to the original image
        img_array = np.array(img)
        img_stretched_array = np.clip((img_array - min_val) * (255 / (max_val - min_val)), 0, 255).astype('uint8')
        img_stretched = Image.fromarray(img_stretched_array, 'L')

        # Save the scaled image
        img_stretched.save(output_path)

# Example usage
# Replace these paths with actual file paths
image_path = "/path/to/original/image.jpg"
output_path = "/path/to/scaled/image.jpg"
centre_x_coord = 0.4  # Replace with actual x-coordinate or proportion of the x-dimension 
centre_y_coord = 0.5  # Replace with actual y-coordinate or proportion of the y-dimension
hist_region_diameter = 0.2  # Replace with actual diameter or proportion of the x-dimension

histogram_scaling(image_path, output_path, centre_x_coord, centre_y_coord, hist_region_diameter, proportional=True)
