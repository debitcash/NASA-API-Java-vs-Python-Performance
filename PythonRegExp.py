import requests
from PIL import Image
from io import BytesIO
import time
import re

# Start measuring the time
start_time = time.time()

# URL to fetch Mars rover photos
nasaUrl = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key=DEMO_KEY"  

# Make a GET request to the NASA API
response = requests.get(nasaUrl)
jsonString = response.text

# Initialize variables to track image size and URL
size = 0
maxSize = 0
finalLink = ""

# Replace uppercase JPG with lowercase jpg and PNG with png
jsonString = jsonString.replace("JPG", "jpg")
jsonString = jsonString.replace("PNG", "png")

# Regular expression pattern to find image URLs
pattern = r'http(.*?)(png|jpg)'
pattern = re.compile(pattern, re.IGNORECASE)
matches = pattern.finditer(jsonString)

# Iterate through each match found in the JSON string
for link in matches:
    # Format the URL to use https and remove ".jpl"
    imgUrl = link.group().replace("http", "https").replace(".jpl", "")
    
    # Fetch the image content from the URL
    content = requests.get(imgUrl).content
    # Open the image and retrieve its size
    im = Image.open(BytesIO(content))
    
    width, height = im.size
    size = width + height
    # Update the largest image size and corresponding URL
    if size >= maxSize:
        maxSize = size
        finalLink = imgUrl

# Print the URL of the image with the largest size
print(finalLink)
print("Time elapsed", (time.time() - start_time)*1000)

