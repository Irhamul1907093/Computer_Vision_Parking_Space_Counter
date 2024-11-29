import cv2
import numpy as np
import math

def my_count_nonzero(img):
    count = 0
    for row in img:
        for pixel in row:
            if pixel != 0:
                count += 1
    return count

def draw_rectangle(img, pt1, pt2, color, thickness):
   
    x1, y1 = pt1
    x2, y2 = pt2
    
    # If thickness is -1, we fill the rectangle
    if thickness == -1:
        img[y1:y2, x1:x2] = color
    else:
        # Draw the top and bottom lines
        img[y1:y1+thickness, x1:x2] = color
        img[y2-thickness:y2, x1:x2] = color
        # Draw the left and right lines
        img[y1:y2, x1:x1+thickness] = color
        img[y1:y2, x2-thickness:x2] = color

def get_gaussian_kernel(k_size, sigma):
    gas_kernel = np.zeros((k_size, k_size))
    norm = 0
    gas_padding = (gas_kernel.shape[0] - 1) // 2
    for x in range(-gas_padding, gas_padding+1):
        for y in range(-gas_padding, gas_padding+1):
            c = 1 / (2 * 3.1416 * (sigma ** 2))
            gas_kernel[x + gas_padding, y + gas_padding] = c * math.exp(-(x ** 2 + y ** 2) / (2 * sigma ** 2))
            norm += gas_kernel[x + gas_padding, y + gas_padding]
    return gas_kernel / norm

def my_gaussian_blur(img, kernel_size, sigma):
    image_h, image_w = img.shape
    gaussian_kernel = get_gaussian_kernel(kernel_size, sigma)
    padding_x = (kernel_size - 1) // 2 
    padding_y = (kernel_size - 1) // 2 

    img_padded = cv2.copyMakeBorder(img, padding_y, padding_y, padding_x, padding_x, cv2.BORDER_REFLECT)
    
    output_image_h = image_h + kernel_size - 1
    output_image_w = image_w + kernel_size - 1

    gaussian_output = np.zeros((output_image_h, output_image_w))
    for x in range(padding_x, output_image_h - padding_x):
        for y in range(padding_y, output_image_w - padding_y):
            temp = 0
            for i in range(-padding_x, padding_x + 1):
                for j in range(-padding_y, padding_y + 1):
                    temp += img_padded[x - i, y - j] * gaussian_kernel[i + padding_x, j + padding_y]
            gaussian_output[x, y] = temp
    
    gaussian_output = gaussian_output[padding_y:padding_y + image_h, padding_x:padding_x + image_w]
    gaussian_output = cv2.normalize(gaussian_output, None, 0, 255, cv2.NORM_MINMAX)
    return gaussian_output.astype(np.uint8) 

def my_adaptive_threshold(img, max_value, adaptive_method, threshold_type, block_size, C):
    # Ensure block_size is odd
    if block_size % 2 == 0:
        raise ValueError("block_size must be an odd number.")

    image_h, image_w = img.shape

    output_img = np.zeros_like(img, dtype=np.uint8)

    # Define the padding based on block size
    padding = block_size // 2


    padded_img = cv2.copyMakeBorder(img, padding, padding, padding, padding, cv2.BORDER_REFLECT)


    for y in range(image_h):
        for x in range(image_w):
            # neighborhood around the current pixel
            neighborhood = padded_img[y:y+block_size, x:x+block_size]

            #adaptive threshold for the current pixel
            if adaptive_method == 'mean':
                threshold = np.mean(neighborhood) - C
            elif adaptive_method == 'gaussian':
                gaussian_kernel = cv2.getGaussianKernel(block_size, -1)
                gaussian_kernel = gaussian_kernel * gaussian_kernel.T
                threshold = np.sum(neighborhood * gaussian_kernel) - C
            else:
                raise ValueError("adaptive_method must be either 'mean' or 'gaussian'.")

            # threshold
            if threshold_type == 'binary':
                output_img[y, x] = max_value if img[y, x] > threshold else 0
            elif threshold_type == 'binary_inv':
                output_img[y, x] = 0 if img[y, x] > threshold else max_value
            else:
                raise ValueError("threshold_type must be either 'binary' or 'binary_inv'.")

    return output_img

#theory
def my_median_filter(img, kernel_size):
    image_h, image_w = img.shape
    padding_x = (kernel_size - 1) // 2 
    padding_y = (kernel_size - 1) // 2 

    # Pad the image
    img_padded = cv2.copyMakeBorder(img, padding_y, padding_y, padding_x, padding_x, cv2.BORDER_REFLECT)

    # Create an empty output image
    median_output = np.zeros_like(img, dtype=np.uint8)
    median_index = (kernel_size * kernel_size) // 2

    # Apply the median filter
    for x in range(padding_x, image_h + padding_x):
        for y in range(padding_y, image_w + padding_y):
            neighborhood = []
            for i in range(-padding_x, padding_x + 1):
                for j in range(-padding_y, padding_y + 1):
                    neighborhood.append(img_padded[x + i, y + j])
            neighborhood.sort()
            median_output[x - padding_x, y - padding_y] = neighborhood[median_index]

    return median_output
#theory
def my_dilate(img, kernel, iterations=1):
    image_h, image_w = img.shape
    kernel_h, kernel_w = kernel.shape
    padding_x = (kernel_w - 1) // 2
    padding_y = (kernel_h - 1) // 2

    # Pad the image
    img_padded = cv2.copyMakeBorder(img, padding_y, padding_y, padding_x, padding_x, cv2.BORDER_CONSTANT, value=0)

    dilated_img = np.zeros_like(img)

    # Apply dilation operation
    for _ in range(iterations):
        for x in range(padding_x, image_h + padding_x):
            for y in range(padding_y, image_w + padding_y):
                # Extract the neighborhood
                neighborhood = img_padded[x-padding_x:x+padding_x+1, y-padding_y:y+padding_y+1]
                
                # Apply the kernel (maximum value in the neighborhood)
                dilated_img[x-padding_x, y-padding_y] = np.max(neighborhood * kernel)

        # Update the padded image for next iteration if needed
        img_padded = cv2.copyMakeBorder(dilated_img, padding_y, padding_y, padding_x, padding_x, cv2.BORDER_CONSTANT, value=0)

    return dilated_img
 