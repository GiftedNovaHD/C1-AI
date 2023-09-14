import torch
from transformers import DetrImageProcessor, DetrForObjectDetection
from PIL import Image
from flask import Flask, render_template, request, redirect
import sqlite3
import os
import datetime

app = Flask(__name__)

@app.route("/classify", methods=["POST"])
def infer() -> str | None:
  try:
    image_file = request.files.get("image", "")
    image_path = os.path.join(".\\static\\images", image_file.filename)
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
  
    cursor.execute(f"SELECT * FROM Images WHERE ImageID = {image_id}")
    image = cursor.fetchall()[0]
  
  except Exception as e:
    conn.close()
    return render_template("error.html", error=e)

  finally:
    conn.close()

  return render_template("image.html", image=image)

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

  app.run(debug=True)