from concurrent.futures import ThreadPoolExecutor
import requests
from PIL import Image
from io import BytesIO
import time
import asyncio
import httpx
from threading import Lock

# Run asynchronous function using asyncio
def run_async(func):
    return asyncio.run(func)

# Asynchronous function to fetch content from a URL
async def getContent(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.content

# Start measuring time
start_time = time.time()

# URL to fetch Mars rover photos
nasaUrl = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key=DEMO_KEY"  
response = requests.get(nasaUrl)
raw = response.text

# Normalize image format strings in the raw text
raw = raw.replace("JPG", "jpg")
raw = raw.replace("PNG", "png")

# Initialize list to store image URLs
urlList = []

# Extract image URLs from the raw text
while raw.find("http") != -1:
    beg = raw.index(":\"http")  # Find the start of the URL
    end = raw.index(".jpg")    # Find the end of the URL

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
    
    urlList.append(imgUrl)

# Split the URL list into chunks for parallel processing
bigList = []
for i in range(0, 8):
    subList = urlList[i * 107 : i * 107 + 107]
    bigList.append(subList)

# Initialize a lock and a result list for thread-safe operations
resultList = []
lock = Lock()

# Function to safely add results to the result list
def safeAdd(item):
    with lock:
        resultList.append(item)

# Asynchronous function to analyze a list of URLs
async def analyseList(submittedList):
    finalLink = ""
    width, height, size, maxSize = 0, 0, 0, 0

    for url in submittedList:
        content = await getContent(url)
        im = Image.open(BytesIO(content))
        
        width, height = im.size
        size = width + height
        if size >= maxSize:
            maxSize = size
            finalLink = url
    
    safeAdd(finalLink)

# Use ThreadPoolExecutor to run tasks in parallel
with ThreadPoolExecutor(max_workers = 8) as executor:
    for i in range(0, 8):
        executor.submit(run_async, analyseList(bigList[i]))

# Print the URL of the image with the largest size and the time elapsed
print(resultList[-1])
print("Time elapsed", (time.time() - start_time) * 1000)

