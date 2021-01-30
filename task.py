from fastapi import FastAPI
from PIL import Image
import requests
import glob

app = FastAPI()

@app.get("/")
def hello():
    return {"Hello":"World"}

# @app.post("/api")
# def comparePhotos():
#     img1 = Image.open(requests.get(request.json['first_photo'], stream=True).raw)    
#     print(img1)
#     img2 = Image.open(request.json['second_photo'])
#     print(img2)
#     return request.json['second_photo']
