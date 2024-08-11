import requests
from PIL import Image
from io import BytesIO
import time

# Start measuring the time
start_time = time.time()

# URL to fetch Mars rover photos
nasaUrl = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key=DEMO_KEY"  

# Make a GET request to the NASA API and get the JSON response
response = requests.get(nasaUrl)
inp = response.json()

# Extract the list of photos from the JSON response
arr = inp["photos"]

# Initialize variables to track image size and URL
size = 0
maxSize = 0
finalLink = ""

# Iterate through each photo in the list
for data in arr:
    # Get the image URL and format it to use https and remove ".jpl"
    imgUrl = data["img_src"].replace("http", "https").replace(".jpl", "")
    
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
# Print the time elapsed for the script execution in milliseconds
print("Time elapsed", (time.time() - start_time) * 1000)
