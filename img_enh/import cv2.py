import cv2
import numpy as np

def enhance_image(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(image, (5, 5), 0)

    # Apply sharpening using the unsharp mask technique
    sharpened = cv2.addWeighted(image, 1.7, blurred, -0.5, 0)

    return sharpened

# Path to the input image
input_image_path = 'sigguuu.jpg'

# Enhance the image
enhanced_image = enhance_image(input_image_path)

# Save the enhanced image
output_image_path = 'enhanced_Sheruu.jpeg'
cv2.imwrite(output_image_path, enhanced_image)

# Display the original and enhanced images
cv2.imshow('Original Image', cv2.imread(input_image_path))
cv2.imshow('Enhanced Image', enhanced_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
