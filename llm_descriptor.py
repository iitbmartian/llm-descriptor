
from google import genai 
from PIL import Image
import io 
 
import os
import cv2
 
from dotenv import  load_dotenv
 
import sys
 


load_dotenv()  
api_key = os.getenv("GEMINI_API_KEY")
 

arguments = sys.argv
if len(arguments) !=2:
    print(f'Please povide the image file path as an argument')

 
filepath = arguments[1]

client=genai.Client(api_key=api_key)
if not os.path.isfile(arguments[1]):
    raise ValueError(f"The provided path '{arguments[1]}' is not a valid file.")
if not filepath.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
    raise ValueError(f"The provided file '{arguments[1]}' is not a valid image file. Supported formats are: .jpg, .jpeg, .png, .bmp, .tiff")
image = cv2.imread(filepath)
if image is None:
    raise ValueError(f"Could not read the image file '{arguments[1]}'. Please check if the file is a valid image.")

 
 
 
target_size = (512, 512)
resized = cv2.resize(image, target_size, interpolation=cv2.INTER_CUBIC)
_, buffer = cv2.imencode('.jpg', resized)
img = Image.open(io.BytesIO(buffer.tobytes()))

response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=[
        img,
        "What are the objects in the image? Describe them. Please give the objects and description in this format:\n"
      
        "Object:-\n"
        "Descriptions:-\n"
        "Likelihood of being present on mars:-\n"
        "In object - try to enter the name of the object in 1-3 words"
        "Try to keep the description to 2-3 sentences max\n"
        "For likelihood of being present on mars give me a percentage"
    ]
)

description = response.text.strip()
print(f'{description}')


 
 
