import requests
import json
from io import BytesIO
from PIL import Image
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# API endpoint for random images from Unsplash
UNSPLASH_API_URL = "https://api.unsplash.com/photos/random"
UNSPLASH_API_KEY = "YOUR_UNSPLASH_API_KEY_HERE"

@app.route("/")
def index():
    # Fetch a list of random images from Unsplash
    response = requests.get(UNSPLASH_API_URL, headers={"Authorization": f"Client-ID {UNSPLASH_API_KEY}"})
    if response.status_code != 200:
        return "Error fetching images from Unsplash"

    # Parse the JSON response and extract the image URLs
    images_data = json.loads(response.text)
    image_urls = [data["urls"]["regular"] for data in images_data]

    # Load the images from the URLs and return them to the template
    images = []
    for url in image_urls:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        images.append(image)

    return render_template("index.html", images=images)

if __name__ == "__main__":
    app.run(debug=True)