from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import os
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "ml_model", "pneumonia_model.keras")

print("✅ USING MODEL:", MODEL_PATH)
model = load_model(MODEL_PATH, compile=False)

client = MongoClient(
    "mongodb+srv://admin:medicalreportcts@cluster0.xgp7csp.mongodb.net/?appName=Cluster0"
)
db = client.medical_db
reports = db.reports

def generate_medical_report(diagnosis):
    if diagnosis == "PNEUMONIA":
        return (
            "EXAMINATION:\n"
            "Chest Radiograph (Posteroanterior View)\n\n"
            "CLINICAL INDICATION:\n"
            "Evaluation for suspected lower respiratory tract infection.\n\n"
            "TECHNIQUE:\n"
            "Single frontal chest radiograph obtained with adequate inspiration.\n\n"
            "FINDINGS:\n"
            "Patchy air-space opacities are noted predominantly in the lower lung zones, "
            "suggestive of infective etiology. Mild blurring of adjacent bronchovascular "
            "markings is observed. No significant pleural effusion or pneumothorax. "
            "Cardiomediastinal silhouette is within normal limits.\n\n"
            "IMPRESSION:\n"
            "Radiographic findings are suggestive of pneumonia.\n\n"
            "RECOMMENDATION:\n"
            "Correlation with clinical findings and laboratory investigations is advised. "
            "Appropriate medical management and follow-up imaging may be considered to "
            "assess resolution."
        )
    else:
        return (
            "EXAMINATION:\n"
            "Chest Radiograph (Posteroanterior View)\n\n"
            "CLINICAL INDICATION:\n"
            "Evaluation for suspected pulmonary infection.\n\n"
            "TECHNIQUE:\n"
            "Single frontal chest radiograph obtained with adequate inspiration.\n\n"
            "FINDINGS:\n"
            "The lung fields are clear bilaterally with no focal air-space consolidation. "
            "No evidence of interstitial infiltrates, pleural effusion, or pneumothorax. "
            "Cardiomediastinal silhouette appears within normal limits. "
            "Bony thoracic structures are intact.\n\n"
            "IMPRESSION:\n"
            "No radiographic evidence of acute cardiopulmonary abnormality. "
            "No features suggestive of pneumonia are identified.\n\n"
            "RECOMMENDATION:\n"
            "Clinical correlation is advised. Follow-up imaging may be considered if "
            "symptoms persist or worsen."
        )


@app.route("/get-reports", methods=["GET"])
def get_reports():
    data = list(reports.find({}, {"_id": 0}))
    return jsonify(data)


@app.route("/predict", methods=["POST"])
def predict():
    file = request.files["image"]
    patient_id = request.form.get("patient_id") 
    age = request.form.get("age")
    gender = request.form.get("gender")
    img = Image.open(file).convert("RGB").resize((224, 224))

    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    pred = model.predict(img_array)[0][0]
    print(" Raw CNN output:", float(pred))

    diagnosis = "PNEUMONIA" if pred > 0.5 else "NORMAL"
    confidence = float(pred * 100 if pred > 0.5 else (1 - pred) * 100)
    report_text = generate_medical_report(diagnosis)

    
    reports.insert_one({
    "patient_id": patient_id,  
    "age": int(age),
    "gender": gender,         
    "image_name": file.filename,
    "diagnosis": diagnosis,
    "confidence": confidence,
    "report_text": report_text,
    "created_at": datetime.utcnow()
})


    return jsonify({
        "diagnosis": diagnosis,
        "confidence": round(confidence, 2),
        "report": report_text
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
