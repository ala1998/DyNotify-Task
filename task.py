from fastapi import FastAPI, Body, HTTPException, Header, Request
from PIL import Image
import requests
import cv2
from skimage.metrics import structural_similarity
import numpy as np
import re

app = FastAPI()

@app.post("/compare")
def comparePhotos(request: Request, body = Body(...)):

    url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    apiKey = ''
    if 'apiKey' in body.keys() or request.headers['apiKey']:
        if 'apiKey' in body.keys():
            apiKey = body['apiKey']
        elif request.headers['apiKey']:
            apiKey = request.headers['apiKey']

        if apiKey == 'sRo09WDtPVQJ4IN7NsckfsyQtpo':
            img1, img2 = body['first_photo'], body['second_photo']

            if re.match(url_regex, img1):
                img1 = requests.get(img1, stream=True).raw

            if re.match(url_regex, img2):
                img2 = requests.get(img2, stream=True).raw
        
            img1 = openImage(img1,'first')
            img2 = openImage(img2,'second')
            
            return {"Percentage": str(computeSimilarity(img1, img2))+"%"}
        else:
            raise HTTPException(status_code=404, detail="Invalid API Key!")

    else:
        raise HTTPException(status_code=404, detail="Please include an API Key in the request body!")

def computeSimilarity(img1, img2):
    processed1 = imageProccssing(img1)
    processed2 = imageProccssing(img2)
    # Compute the Structural Similarity Index (SSIM)
    percentage = structural_similarity(processed1, processed2, multichannel= True)
    return percentage * 100

def imageProccssing(img):
    # Convert the image to equivalent type of CV2 type which is (UMat)
    img = np.float32(img)
    # Resize the image since Input images must have the same dimensions
    img = cv2.resize(img, (500, 500))
    # Convert the image to grayscale
    return(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))

def openImage(img,order):
    try:
        return(Image.open(img))
    except Exception as e:
        if 'cannot identify image' in str(e):
            detail_msg = "The " + order + " image in not found at the URL!"
        elif 'Invalid argument' in str(e):
            detail_msg = "Invalid URL for the " + order + " image!"
        elif 'No such file' in str(e):
            detail_msg = "The local " + order + " image is not exist in the path!"
        raise HTTPException(status_code=404, detail=detail_msg)