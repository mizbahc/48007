from flask_cors import CORS
from flask import Flask, render_template, request, send_from_directory, send_file, redirect, url_for
import torch 
import numpy as np
from PIL import Image
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
import os.path
import json
from pprint import pprint

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
  print("homepage")
  return "Hello from server..."


@app.route('/video_stream', methods=['POST'], strict_slashes=False)
def stream():
    file = request.files['image']
    data = Image.open(file.stream)

    result = model(data)
    result.show()
    return redirect(url_for("stream", image=result))


@app.route('/get_people', methods=['POST'], strict_slashes=False)
def postPeople():
    file = request.files['image']
    data = Image.open(file.stream)

    result = model(data)
    predictions = result.pred[0]

    personCounter = 0
    predictionKeys = []

    for i in range(len(predictions)):
      arraySize = len(predictions[i]) - 1
      predictionKeys.append(predictions[i][arraySize])
    
    for i in range(len(predictionKeys)):
      if predictionKeys[i] == 0:
        personCounter += 1
    
    print("There are", personCounter, "person(s).")

    return redirect(url_for("getPeople", numberOfPeople=personCounter))



@app.route('/video_stream', methods=['GET'], strict_slashes=False)
def stream():
    if request.args:
      image = request.args['image']
      return render_template("index.html", image=image)
    return render_template("index.html")


@app.route('/get_people', methods=['GET'], strict_slashes=False)
def getPeople():
  if request.args:
    numberOfPeople = request.args['numberOfPeople']
    return render_template("people.html", numberOfPeople=numberOfPeople)
  return render_template("people.html")


@app.route('/tiny_stream', methods=['POST'], strict_slashes=False)
def tiny():
    print(request.json)
    res = request.json
    pprint(res)
    number_of_person = res['number_of_person']
    detected_objects = res['detected_objects']

    print("-------INCOMING FRAME---------\n")
    print("(TinyYOLO) There are", number_of_person, "person(s).\n")
    print("All detected objects:")
    for key, value in detected_objects.items():
      print(int(key)+1, "Object type:" ,"\"", value["object_type"] , "\"", "Bounding box:", value["bounding_box"])
    print("--------FRAME END--------")
    return render_template("people.html", numberOfPeople=number_of_person)

    
    



if __name__ == '__main__':
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

    app.run(debug=True , host="0.0.0.0", port="80")

