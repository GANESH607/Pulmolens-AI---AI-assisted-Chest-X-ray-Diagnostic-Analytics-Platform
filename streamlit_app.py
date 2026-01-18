import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime


def generate_medical_report_pdf(
    patient_id, age, gender,
    diagnosis, confidence, report_text
):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height - 50, "PulmoLens AI")

    
    c.setFont("Helvetica", 10)
    c.drawCentredString(
        width / 2, height - 75,
        "AI-Assisted Chest X-ray Diagnostic & Analytics Platform"
    )

    c.line(40, height - 90, width - 40, height - 90)

    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, height - 120, "Patient Information")

    c.setFont("Helvetica", 11)
    c.drawString(40, height - 145, f"Patient ID: {patient_id}")
    c.drawString(40, height - 165, f"Age: {age}")
    c.drawString(40, height - 185, f"Gender: {gender}")
    c.drawString(
        40, height - 205,
        f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )

    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, height - 245, "Diagnosis Result")

    c.setFont("Helvetica", 11)
    c.drawString(40, height - 270, f"Diagnosis: {diagnosis}")
    c.drawString(40, height - 290, f"Confidence: {confidence:.2f}%")

    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, height - 330, "AI-Generated Medical Report")

    text = c.beginText(40, height - 355)
    text.setFont("Helvetica", 11)

    for line in report_text.split("\n"):
        text.textLine(line)

    c.drawText(text)

    
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(
        40, 60,
        "Disclaimer: This AI-generated report is for educational purposes only "
        "and should not replace professional medical diagnosis."
    )

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer


st.set_page_config(
    page_title="PulmoLens AI Dashboard",
    layout="wide",
    page_icon="🩺"
)


st.markdown("""
<h1 style="text-align:center;">🩺 PulmoLens AI</h1>
<p style="text-align:center; color:gray;">
AI-assisted Chest X-ray Diagnostic & Analytics Platform
</p>
<hr>
""", unsafe_allow_html=True)


st.sidebar.title("🧭 Navigation")
menu = st.sidebar.radio(
    "Select Module",
    ["New Diagnosis", "Patient History", "Model Information"]
)


if menu == "New Diagnosis":

    st.subheader("🧑‍⚕️ Patient Information")
    col1, col2, col3 = st.columns(3)

    with col1:
        patient_id = st.text_input("Patient ID")
    with col2:
        age = st.number_input("Age", 1, 120)
    with col3:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    st.markdown("---")

    st.subheader("🩻 Upload Chest X-ray")
    uploaded_file = st.file_uploader(
        "Accepted formats: JPG, PNG, JPEG",
        type=["jpg", "png", "jpeg"]
    )

    if uploaded_file:
        col_img, col_action = st.columns([1, 1])

        with col_img:
            st.image(
                uploaded_file,
                caption="Uploaded Chest X-ray",
                use_column_width=True
            )

        with col_action:
            if st.button("🔍 Generate Medical Report", use_container_width=True):
                with st.spinner("Analyzing X-ray using CNN model..."):
                    response = requests.post(
                        "http://localhost:5000/predict",
                        files={
                            "image": (
                                uploaded_file.name,
                                uploaded_file.getvalue(),
                                uploaded_file.type
                            )
                        },
                        data={
                            "patient_id": patient_id,
                            "age": age,
                            "gender": gender
                        }
                    )

                if response.status_code != 200:
                    st.error("❌ Backend error occurred")
                    st.stop()

                result = response.json()

                st.markdown("---")
                st.subheader("Diagnosis Result")

                if result["diagnosis"] == "NORMAL":
                    st.success(
                        f" **NORMAL**  \nConfidence: {result['confidence']:.2f}%"
                    )
                else:
                    st.error(
                        f" **PNEUMONIA DETECTED**  \nConfidence: {result['confidence']:.2f}%"
                    )

                st.info(" **AI-Generated Medical Report**")
                st.write(result["report"])

                st.success("Report saved securely in database")

                
                pdf_buffer = generate_medical_report_pdf(
                    patient_id=patient_id,
                    age=age,
                    gender=gender,
                    diagnosis=result["diagnosis"],
                    confidence=result["confidence"],
                    report_text=result["report"]
                )

                st.download_button(
                    label=" Download Medical Report (PDF)",
                    data=pdf_buffer,
                    file_name=f"{patient_id}_medical_report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )


elif menu == "Patient History":

    st.subheader("📁 Patient Diagnosis History & Analytics")

    response = requests.get("http://localhost:5000/get-reports")
    data = response.json()

    if not data:
        st.warning("No patient records found.")
        st.stop()

    df = pd.DataFrame(data)
    df["created_at"] = pd.to_datetime(df["created_at"])

    
    st.markdown("### 🔍 Filters")
    col1, col2 = st.columns(2)

    with col1:
        pid = st.text_input("Filter by Patient ID")
    with col2:
        diagnosis_filter = st.selectbox(
            "Filter by Diagnosis",
            ["All", "NORMAL", "PNEUMONIA"]
        )

    if pid:
        df = df[df["patient_id"] == pid]

    if diagnosis_filter != "All":
        df = df[df["diagnosis"] == diagnosis_filter]

    
    st.markdown("### 📋 Patient Records")
    st.dataframe(
        df.sort_values("created_at", ascending=False),
        use_container_width=True
    )

    st.markdown("---")

    
    st.markdown("## 📊 Clinical Analytics Overview")

    
    col1, col2 = st.columns(2)

    
    with col1:
        st.markdown("**Diagnosis Distribution**")
        diag_counts = df["diagnosis"].value_counts()

        fig1, ax1 = plt.subplots(figsize=(4, 4))
        ax1.pie(
            diag_counts,
            labels=diag_counts.index,
            autopct="%1.0f%%",
            startangle=90,
            wedgeprops=dict(width=0.4)  
        )
        ax1.axis("equal")
        plt.tight_layout()
        st.pyplot(fig1)

    
    with col2:
        st.markdown("**Model Confidence Distribution**")

        fig2, ax2 = plt.subplots(figsize=(4, 4))
        ax2.hist(df["confidence"], bins=8)
        ax2.set_xlabel("Confidence (%)", fontsize=8)
        ax2.set_ylabel("Cases", fontsize=8)
        plt.tight_layout()
        st.pyplot(fig2)

    
    col3, col4 = st.columns(2)

    
    with col3:
        st.markdown("**Diagnosis Trend Over Time**")

        daily_cases = df.groupby(df["created_at"].dt.date).size()

        fig3, ax3 = plt.subplots(figsize=(4.5, 3))
        ax3.plot(daily_cases.index, daily_cases.values, marker="o")
        ax3.set_xlabel("Date", fontsize=8)
        ax3.set_ylabel("Cases", fontsize=8)
        plt.tight_layout()
        st.pyplot(fig3)

    
    with col4:
        st.markdown("**Age Group vs Diagnosis**")

        df["age_group"] = pd.cut(
            df["age"],
            bins=[0, 20, 40, 60, 80, 120],
            labels=["0–20", "21–40", "41–60", "61–80", "80+"]
        )

        age_diag = pd.crosstab(df["age_group"], df["diagnosis"])

        fig4, ax4 = plt.subplots(figsize=(4.5, 3))
        age_diag.plot(kind="bar", ax=ax4)
        ax4.set_xlabel("Age Group", fontsize=8)
        ax4.set_ylabel("Cases", fontsize=8)
        plt.tight_layout()
        st.pyplot(fig4)

elif menu == "Model Information":

    st.subheader(" CNN Model Details")

    st.markdown("""
    **Model Type:** Convolutional Neural Network (CNN)  
    **Task:** Binary Classification (Normal vs Pneumonia)  
    **Input Size:** 224 × 224  
    **Framework:** TensorFlow / Keras  

    **Disclaimer:**  
    This system is intended for **educational and research purposes only**  
    and does **not** replace professional medical diagnosis.
    """)

