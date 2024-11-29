import cv2
import numpy as np

# Load the image
image = cv2.imread('car4.jpg')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray=cv2.GaussianBlur(gray,(3,3),1)
# Apply threshold to get binary image
_, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# Function to find the width of the parking slot
def find_width(start_row, start_col, binary_image):
    cols = binary_image.shape[1]
    for col in range(start_col, cols):
        if binary_image[start_row, col] == 0:
            return col - start_col
    return cols - start_col

# Function to find the height of the parking slot
def find_height(start_row, start_col, binary_image):
    rows = binary_image.shape[0]
    for row in range(start_row, rows):
        if binary_image[row, start_col] == 0:
            return row - start_row
    return rows - start_row

# List to store the detected parking slots
parking_slots = []

# Traverse the image to detect the first white line
rows, cols = binary.shape
slot_width = 0
slot_height = 0
for row in range(rows):
    for col in range(cols):
        if binary[row, col] == 255:  # Detect white line
            slot_width = find_width(row, col, binary)
            slot_height = find_height(row, col, binary)
            slot_width = int(slot_width/4 )
            slot_height = int(slot_height /4)
            if slot_width > 20 and slot_height > 20:  # Threshold to filter out small detections
                parking_slots.append((row, col, slot_width, slot_height))
                break
    if slot_width > 0 and slot_height > 0:
        break

# Print the height and width of a parking slot
print(f"Parking Slot Width: {slot_width}, Parking Slot Height: {slot_height}")

# Now use the determined width and height to find all parking slots
if slot_width > 0 and slot_height > 0:
    for row in range(0, rows, slot_height):
        for col in range(0, cols, slot_width):
            if binary[row, col] == 255:  # Detect white line
                parking_slots.append((row, col, slot_width, slot_height))

# Draw the detected parking slots on the original image
for slot in parking_slots:
    row, col, width, height = slot
    cv2.rectangle(image, (col, row), (col + width, row + height), (0, 255, 0), 2)

# Display the result
cv2.imshow('Detected Parking Slots', image)
cv2.imshow('binary', binary)
cv2.waitKey(0)
cv2.destroyAllWindows()
