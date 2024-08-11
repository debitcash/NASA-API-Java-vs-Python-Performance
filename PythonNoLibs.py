import requests
from PIL import Image
from io import BytesIO
import time

# Start measuring the time
start_time = time.time()

# URL to fetch Mars rover photos
nasaUrl = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key=DEMO_KEY"  

# Make a GET request to the NASA API and get the raw response text
response = requests.get(nasaUrl)
raw = response.text

# Initialize variables to track image size and URL
size = 0
maxSize = 0
finalLink = ""

# Normalize image format strings in the raw text
raw = raw.replace("JPG", "jpg")
raw = raw.replace("PNG", "png")

# Extract image URLs from the raw text
while raw.find("http") != -1:
    beg = raw.index(":\"http")  # Find the start of the URL
    end = raw.index(".jpg")  # Find the end of the URL

    # Check for ".png" URLs and adjust end position if found
    try:
        if end > raw.index(".png") and raw.index(".png") != -1:
            end = raw.index(".png")
    except ValueError:
        print("Reached bottom")  # Handle case where ".png" is not found

    # Extract and clean the image URL
    rawLink = raw[beg + 2 : end + 4]
    raw = raw[end + 4:]

    imgUrl = rawLink.replace("http", "https").replace(".jpl", "")
    
    # Download the image and open it
    content = requests.get(imgUrl).content
    im = Image.open(BytesIO(content))
    
    # Get image dimensions and calculate the size
    width, height = im.size
    size = width + height
    # Update the largest image size and corresponding URL
    if size >= maxSize:
        maxSize = size
        finalLink = imgUrl

# Print the URL of the image with the largest size
print(finalLink)
# Print the time elapsed for the script execution in milliseconds
print("Time elapsed", (time.time() - start_time) * 1000)
