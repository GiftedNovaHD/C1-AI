import torch
import sqlite3
import os
import datetime
import json

from transformers import DetrImageProcessor, DetrForObjectDetection
from PIL import Image
from flask import Flask, render_template, request, redirect


app = Flask(__name__)

@app.route("/classify", methods=["POST"])
def infer() -> str | None:
  try:
    image_file = request.files.get("image", "")
    image_path = os.path.join(".\\static\\images", image_file.filename)

    if os.path.exists(image_path):
      return render_template("index.html")

    # so that there's no duplicate image 
    image_file.save(image_path)
    image_path = f"images/{image_file.filename}"
    upload_date = datetime.datetime.now()

    image = Image.open(image_file)
  except Exception as e:
    return render_template("error.html", error=e)

  inputs = processor(images=image, return_tensors="pt")
  inputs = inputs.to(device) 
  outputs = model(**inputs)

  target_sizes = torch.tensor([image.size[::-1]]).to(device) # 
  results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

  detection_info = []
  for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    box = [round(i, 2) for i in box.tolist()]
    class_name = model.config.id2label[label.item()]
    detection_info.append({
      "class_name": class_name,
      "confidence": round(score.item(), 3),
      "location": box
      })

  try:
    conn = sqlite3.connect("image_classification.db", isolation_level=None)
    cursor = conn.cursor()

    cursor.execute("""
                   INSERT INTO Images (ImageName, ImageFile, UploadDate) 
                   VALUES (?,?,?)
    """, (image_file.filename, image_path, upload_date))

    image_id = cursor.lastrowid

    for info in detection_info:
      class_name = info["class_name"]
      confidence = info["confidence"]
      location = json.dumps(info["location"])

      # Retrieve the ClassID for the class name or insert it if it doesn't exist
      cursor.execute("SELECT ClassID FROM Classes WHERE ClassName = ?", (class_name,))
      class_id = cursor.fetchone()
      if class_id is None:
        cursor.execute("INSERT INTO Classes (ClassName) VALUES (?)", (class_name,))
        class_id = cursor.lastrowid
      else:
        class_id = class_id[0]

        # Insert detection data
      cursor.execute(
        """
        INSERT INTO Detections (ImageID, ClassID, Confidence, Location) 
        VALUES (?,?,?,?)
        """, (image_id, class_id, confidence, location))

  except sqlite3.Error as e:
    conn.close()
    return render_template('error.html', error=e)
  finally:
    conn.close()
  
  return render_template('index.html', result=detection_info, image_url=f"images/{image_file.filename}", redirect=True) 

@app.route("/")
def homepage():
  return render_template("index.html")

@app.route("/images")
def view_images():
  try: 
    conn = sqlite3.connect('image_classification.db')
    cursor = conn.cursor()
  
    cursor.execute("SELECT ImageID, ImageName, ImageFile, UploadDate FROM Images")

    image_data = []
    for row in cursor.fetchall():
      image_data.append({
      "ImageID": row[0],
      "ImageName": row[1],
      "ImageFile": row[2],
      "UploadDate": row[3]
      })
  
    conn.close()
    return render_template('images.html', image_data=image_data)  
  except sqlite3.Error as e: 
    print(f"Database error: {e}")
    conn.close()
    return render_template('error.html', error=e)

@app.route("/image")
def show_image():
  image_id = request.args.get("id")

  if image_id is None:
    return render_template("error.html", error="No id parameter supplied you bozo")
  
  try:
    conn = sqlite3.connect('image_classification.db')
    cursor = conn.cursor()
  
    cursor.execute(f"SELECT * FROM Images WHERE ImageID = ? ", (image_id))
    image = cursor.fetchall()[0]

    image_data = {
      "ImageID": image[0],
      "ImageName": image[1],
      "ImageFile": image[2],
      "UploadDate": image[3]
    }
  
  except Exception as e:
    conn.close()
    return render_template("error.html", error=e)

  finally:
    conn.close()

  return render_template("image.html", image=image_data)

@app.route("/classes")
def classes():
  try:
    conn = sqlite3.connect('image_classification.db')
    cursor = conn.cursor()

    cursor.execute("""
      SELECT
        C.ClassName,
        I.ImageName,
        I.ImageFile,
        I.UploadDate,
        I.ImageID
      FROM Classes AS C
      LEFT JOIN
        Detections AS D ON C.ClassID = D.ClassID
      LEFT JOIN
        Images AS I ON D.ImageID = I.ImageID
      """)
    data = cursor.fetchall() # tuple 

    classes_data = {}
    for d in data:
      if d[2] is None:
        continue
      if d[0] in classes_data.keys():
        classes_data[d[0]].append({
          "ImageName": d[1],
          "ImageFile": d[2],
          "UploadDate": d[3],
          "ImageID": d[4]
        })
      else:
        classes_data[d[0]] = [
        {
          "ImageName": d[1],
          "ImageFile": d[2],
          "UploadDate": d[3],
          "ImageID": d[4]
        }
      ]

      
    return render_template("classes.html", data=classes_data)
    
  except Exception as e:
    conn.close()
    return render_template("error.html", error=e)

@app.route("/about")
def about_the_architecture(): 
  return render_template("about.html")

@app.route("/admin_panel")
def administrator():

  try:
    conn = sqlite3.connect('image_classification.db')
    cursor = conn.cursor()

    cursor.execute("SELECT ImageID, ImageName, ImageFile, UploadDate FROM Images")

    image_data = []
    for row in cursor.fetchall():
      image_data.append({
      "ImageID": row[0],
      "ImageName": row[1],
      "ImageFile": row[2],
      "UploadDate": row[3]
      })
  
    conn.close()

  except Exception as e:
    conn.close()
    return render_template("error.html", error=e)

  return render_template("admin_panel.html", image_data=image_data)


@app.route("/delete")
def delete_image(): 
  image_id = request.args.get("id")
  
  if image_id is None: 
    return render_template("error.html", error="No image ID provided for deletion")
  
  try: 
    conn = sqlite3.connect('image_classification.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT ImageFile FROM Images WHERE ImageID = ?", (image_id))
    image_path = cursor.fetchone()[0]

    cursor.execute("DELETE FROM Images WHERE ImageID = ?", (image_id))
    cursor.execute("DELETE FROM Detections WHERE ImageID = ?", (image_id))
    conn.commit()

    os.remove("./static/" + image_path)

  except Exception as e: 
    return render_template("error.html", error=e)
  
  finally: 
    conn.close()
  
  return redirect("admin_panel")

if __name__ == "__main__": 
  device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
  print("Currently using: ", device, "for inference.")

  processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-101")
  model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-101")
  model = model.to(device)

  app.run(debug=False)