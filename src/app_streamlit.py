import streamlit as st
from model_utils import SYMPTOMS, predict_from_symptoms

st.set_page_config(page_title="AI Medical Diagnosis Assistant", page_icon="🩺", layout="wide")

st.title("🩺 AI Medical Diagnosis Assistant")
st.markdown("Select your symptoms below and click **Predict** to see possible diseases.")

selected_symptoms = st.multiselect(
    "Choose your symptoms:",
    options=SYMPTOMS,
    help="You can select multiple symptoms."
)

if st.button("Predict"):
    if not selected_symptoms:
        st.warning("⚠️ Please select at least one symptom.")
    else:
        # ✅ FIX: Convert list to dict
        symptom_dict = {s: (1 if s in selected_symptoms else 0) for s in SYMPTOMS}
        predictions = predict_from_symptoms(symptom_dict)

        st.subheader("Top Predictions:")
        for disease, prob in predictions:
            st.write(f"✅ **{disease}** – Probability: **{prob:.2f}**")

st.markdown("---")
st.caption("⚠️ Educational demo only – not for real medical use.")
