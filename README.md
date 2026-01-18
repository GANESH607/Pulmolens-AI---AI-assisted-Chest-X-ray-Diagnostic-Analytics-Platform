# PulmoLens AI  
## AI-Assisted Chest X-ray Diagnostic & Clinical Analytics Platform

---

## Overview

PulmoLens AI is an end-to-end medical imaging platform designed to assist in the
early detection of pneumonia from chest X-ray images using deep learning.
The system integrates a Convolutional Neural Network (CNN) for image inference,
a Flask-based backend API for prediction and data persistence, and an
interactive Streamlit dashboard for visualization, reporting, and analytics.

The platform emphasizes clinical realism by generating structured,
radiology-style medical reports and maintaining longitudinal patient history
with analytical insights.

---

## Objectives

- Detect pneumonia from chest X-ray images using a CNN
- Generate clinically structured radiology-style reports
- Store patient diagnostic records securely in MongoDB
- Provide compact and meaningful medical analytics dashboards
- Enable PDF-based medical report export

---

## Key Features

- CNN-based pneumonia classification (NORMAL / PNEUMONIA)
- Radiology-style structured medical report generation
- Downloadable A4-format medical reports (PDF)
- Persistent patient history using MongoDB Atlas
- Clinical analytics including:
  - Diagnosis distribution
  - Confidence score distribution
  - Diagnosis trends over time
  - Age group vs diagnosis analysis
- Modular and scalable architecture

---

## System Architecture

Streamlit Dashboard
|
v
Flask REST API
|
v
CNN Model (TensorFlow / Keras)
|
v
MongoDB Atlas

## Model Details

- Model Type: Convolutional Neural Network (CNN)
- Input Size: 224 × 224 RGB images
- Framework: TensorFlow / Keras
- Task: Binary Classification (NORMAL vs PNEUMONIA)

---

## Database Schema

`json
{
  "patient_id": "P102",
  "age": 65,
  "gender": "Male",
  "diagnosis": "PNEUMONIA",
  "confidence": 92.4,
  "report_text": "Structured radiology-style report",
  "created_at": "2026-01-18T11:55:10Z"
}

Technology Stack

Frontend: Streamlit

Backend: Flask (Python)

Deep Learning: TensorFlow / Keras

Database: MongoDB Atlas

Visualization: Matplotlib

Report Generation: ReportLab

Disclaimer

This project is intended strictly for educational and research purposes.
It does not replace professional medical diagnosis or clinical decision-making.

Author

Ganesh Ilango
Project: PulmoLens AI

License

This project is released for academic and research use only.


