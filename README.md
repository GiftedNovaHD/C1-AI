# AI Image Object Detection Web Tool

This repository contains a web-based tool for AI image object detection built upon the **DEtection TRansformer (DETR)** model. Our approach views object detection as a direct set prediction problem, effectively streamlining the detection pipeline. This tool leverages the power of DETR to perform object detection on images provided by users.

## Table of Contents
- [Introduction](#introduction)
- [Keep in view](#keep-in-view)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [DETR model](#detr-model)
- [Web Interface](#web-interface)
- [Additional Notes](#additional-notes)
  - [User Documentation](#user-documentation)
  - [Administrator Documentation](#administrator-documentation)



## Introduction
Our web-based AI image object detection tool is designed to simplify the process of detecting objects in images. It utilizes the DETR model, which treats object detection as a set prediction problem, eliminating the need for many hand-designed components. This tool provides an intuitive and user-friendly interface for users to upload images and receive object detection results.

## Features
- **Object Detection**: The tool uses the DETR model to detect objects within images, providing class labels for each object.
- **Web Interface**: A user-friendly web interface allows users to upload images for object detection and view the results directly on the webpage.
- **DETR Model**: The DETR model, as described in the research paper, is used as the underlying AI model for object detection. It provides relatively accurate and efficient results.
- **Real-time Inference**: The tool performs real-time inference, making it suitable for a wide range of applications, including image analysis, content moderation, and more.

## Keep in view
- Please note that this tool is still in development. Expect errors here and there when navigating and using the micro-web-app. 
- To my knowledge, inference can be performed on the CPU, if a CUDA-enabled GPU is not available.

## Getting Started

### Prerequisites
Before running the web tool, ensure you have the following prerequisites installed:
- Any version of Python >= 3.8
- `pip` package manager
- Virtual environment (optional but recommended)
- NVIDIA GPU with CUDA support (highly recommended for inference)
- PyTorch >= 2.0.1 (if I remember correctly)

### Installation and Running
1. Create a virtual environment in that directory and install the dependencies required in `requirements.txt`.
2. Navigate to `main.py`.
3. Run `main.py`, and naviagte to the address `localhost:5000` or `127.0.0.1` on any browser. 

## DETR Model
Our tool utilizes the DEtection TRansformer (DETR) model, as described in the research paper. DETR represents a breakthrough in object detection by treating it as a set prediction problem, eliminating the need for many hand-designed components. The model can be easily generalized for various object detection tasks and provides state-of-the-art performance.

For more details on the DETR model and its implementation, refer to the official [DETR GitHub repository](https://github.com/facebookresearch/detr).

## Web Interface
The web interface of our tool allows users to interact with the DETR model seamlessly. Here are the main components of the web interface:

- **Upload Image**: Users can upload an image directly from their local device.
- **Object Detection**: Once the image is uploaded, the tool performs object detection using DETR and displays the results, including bounding boxes around detected objects and their corresponding class labels.
- **Real-time inference**: The tool provides real-time inference, allowing users to see the detection results instantly.
- **Beautifully-styled rainbow effect**: No explanation needed. 
- **Images classified by objects present**: Our tool not only detects objects in uploaded images but also provides detailed classifications of objects present within the image. After uploading an image and clicking the "Classify" button, users will be presented with a tabulated view of the detected objects. This feature makes it easy for users to quickly identify and categorize objects in their images.


## Additional Notes 

#### Problem Statement
Do you want your images to be sorted by objects in the photo? This tool is the ideal tool for sorting images based on objects present in the photo. 

The objective of the project is to allow users to view and classify their images based on objects present within the image. 

#### User Documentation 
1. Navigate to `localhost:5000` on _any_ modern web browser of your choice (e.g. Chrome, Edge, Safari, Firefox, Brave).
2. You should be able to view the rainbow-styled header of the website. 
3. On the main page, click on "Browse", and select your image to be uploaded to the web-server.
4. Click on "Classify", and you should be redirected to the results of your classified image in a tabulated form.
5. You may exit to the home-page by clicking on "Back to Home" on the site that displays the classified image.
6. If you want to view more about the architecture, please click on "Read More" at the top of the home-page. 

#### Administrator Documentation
1. Navigate to `localhost:5000/admin_panel` on _any_ modern web browser of your choice (e.g. Chrome, Edge, Safari, Firefox, Brave). 
2. Given that the features of this image classifier AI does not need any sort of updating, the only relevant use case for a web-administrator would be to perform `DELETE` operations.
3. Click on "delete" to delete an image from the web-server. 

#### Database Tables
`Images(ImageID, ImageName, ImageFile, UploadDate)`

`Detections(DetectionID, ImageID, ClassID, Confidence, Location)`

`Classes(ClassID, ClassName)`

#### Normalization (3NF)
The database schema provided in the SQL statements is already in the 3rd Normal Form (3NF) as it satisfies the following conditions:
- Atomic Values: Each attribute (column) contains atomic values, and there are no multi-valued attributes.
- No Partial Dependencies: There are no partial dependencies. All non-key attributes depend on the entire primary key.
- No Transitive Dependencies: There are no transitive dependencies. Non-key attributes do not depend on other non-key attributes.

