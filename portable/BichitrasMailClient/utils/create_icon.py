import requests
from PIL import Image
import io

def create_icon():
    try:
        # Download logo
        logo_url = "https://utfs.io/f/uCCvk88x4gvM3puo5JI2lfhitzaQJEejZDXdxGvy69UkBMr8"
        response = requests.get(logo_url)
        logo_data = response.content
        
        # Open image and convert to icon
        img = Image.open(io.BytesIO(logo_data))
        
        # Create different sizes for the icon
        sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
        img.save('icon.ico', format='ICO', sizes=sizes)
        
        print("Icon created successfully!")
    except Exception as e:
        print(f"Error creating icon: {e}")

if __name__ == "__main__":
    create_icon()
