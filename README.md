# AI Image Object Detection Web Tool

This repository contains a web-based tool for AI image object detection built upon the **DEtection TRansformer (DETR)** model. Our approach views object detection as a direct set prediction problem, effectively streamlining the detection pipeline. This tool leverages the power of DETR to perform object detection on images provided by users.

## Table of Contents
- [Introduction](#introduction)
- [Keep in view](#Keep-in-view)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [DETR model](#detr-model)
- [Web Interface](#web-interface)



## Introduction
Our web-based AI image object detection tool is designed to simplify the process of detecting objects in images. It utilizes the DETR model, which treats object detection as a set prediction problem, eliminating the need for many hand-designed components. This tool provides an intuitive and user-friendly interface for users to upload images and receive object detection results.

## Features
- **Object Detection**: The tool uses the DETR model to detect objects within images, providing bounding box predictions and class labels for each object.
- **Web Interface**: A user-friendly web interface allows users to upload images for object detection and view the results directly on the webpage.
- **DETR Model**: The DETR model, as described in the research paper, is used as the underlying AI model for object detection. It provides accurate and efficient results.
- **Real-time Inference**: The tool performs real-time inference, making it suitable for a wide range of applications, including image analysis, content moderation, and more.

## Keep in view
Please note that this tool is still in development. Expect errors here and there when navigating and using the Flask framework. 

## Getting Started

### Prerequisites
Before running the web tool, ensure you have the following prerequisites installed:
- Any version of Python >= 3.8
- `pip` package manager
- Virtual environment (optional but recommended)
- NVIDIA GPU with CUDA support (highly recommended for inference)
- PyTorch >= 2.0.1 (if I remember correctly)

### Installation
1. Navigate to `main.py`.
2. Create a virtual environment in that directory and install the dependencies required in `requirements.txt`.

## DETR Model
Our tool utilizes the DEtection TRansformer (DETR) model, as described in the research paper. DETR represents a breakthrough in object detection by treating it as a set prediction problem, eliminating the need for many hand-designed components. The model can be easily generalized for various object detection tasks and provides state-of-the-art performance.

For more details on the DETR model and its implementation, refer to the official [DETR GitHub repository](https://github.com/facebookresearch/detr).

## Web Interface
The web interface of our tool allows users to interact with the DETR model seamlessly. Here are the main components of the web interface:

- **Upload Image**: Users can upload an image directly from their local device.
- **Object Detection**: Once the image is uploaded, the tool performs object detection using DETR and displays the results, including bounding boxes around detected objects and their corresponding class labels.
- ~~**Customization**: Users can adjust detection parameters, such as confidence threshold, to fine-tune the detection results.~~
- **Real-time inference**: The tool provides real-time inference, allowing users to see the detection results instantly.
- **Beautifully-styled rainbow effect**: No explanation needed





