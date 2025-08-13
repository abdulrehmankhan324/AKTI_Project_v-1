import streamlit as st
import google.generativeai as genai
from datetime import date

# Set Gemini API Key
genai.configure(api_key='AIzaSyB0_qU0yBpaHO7LiK2AE3AeKcnVNvjq3tk')

# Load Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

# Streamlit UI
st.set_page_config(page_title="AI Complaint Writer", page_icon="✍")
st.title("✍ AI Complaint Writer | By Abdul Rehman")

with st.form("complaint_form"):
    st.subheader("🧾 Sender Information")
    your_name = st.text_input("Your Name")
    your_address = st.text_input("Your Address")
    your_phone = st.text_input("Your Phone Number")
    your_email = st.text_input("Your Email")

    st.subheader("📨 Recipient Information")
    recipient_name = st.text_input("Recipient's Name")
    recipient_address = st.text_input("Recipient's Address")

    st.subheader("🌐 Language & Complaint")
    input_lang = st.selectbox("Select Language", ["english", "urdu"])
    complaint = st.text_area(f"Write your complaint in {input_lang}:")

    submitted = st.form_submit_button("Generate Complaint")

if submitted:
    current_date = date.today().strftime("%Y-%m-%d")

    # Prompt for selected language
    prompt = f"""
You are a helpful AI Complaint Writer Bot.

Your job is to write a formal complaint letter based on the following issue, in polite and professional tone.
Include the following details:
Date: {current_date}
Sender Name: {your_name}
Sender Address: {your_address}
Sender Phone: {your_phone}
Sender Email: {your_email}
Recipient Name: {recipient_name}
Recipient Address: {recipient_address}

Language: {input_lang}
Complaint: {complaint}

Output only the final complaint letter.
"""

    response = model.generate_content(prompt)
    complaint_text = response.text.strip()

    st.success("✅ Complaint Letter Generated!")
    st.subheader(f"📄 Complaint in {input_lang.capitalize()}:")
    st.text_area("Generated Complaint", complaint_text, height=300)

    # Save to file
    filename = f"complaint_{input_lang}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Original Complaint ({input_lang}): {complaint}\n\n")
        f.write(f"Generated Complaint ({input_lang.title()}):\n\n{complaint_text}")

    with open(filename, "rb") as file:
        st.download_button(
            label=f"📥 Download {input_lang.title()} Complaint",
            data=file,
            file_name=filename,
            mime="text/plain"
        )
