import streamlit as st
import nltk
from medisearch_client import MediSearchClient
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from datetime import datetime
import random
import re

# Download required NLTK resources (already handled in your separate script)
nltk.download("punkt")
nltk.download("stopwords")

# Initialize MediSearch API client
MEDISEARCH_API_KEY = "d4b55ee3-2998-45c8-b31f-d133a664decc"  # Your provided API key
client = MediSearchClient(api_key=MEDISEARCH_API_KEY)

# Custom CSS for healthcare theme with improved visibility for selected text
def add_custom_css():
    st.markdown("""
    <style>
    body {
        background-color: #121212; /* Dark mode background */
        font-family: 'Arial', sans-serif;
    }
    
    /* User message styling */
    div[style*="background-color: rgb(230, 243, 255)"] {
        background-color: #1e3a8a !important; /* Dark Blue */
        color: #ffffff !important; /* White text */
        border-radius: 8px;
        padding: 10px;
    }

    /* Bot message styling */
    div[style*="background-color: rgb(240, 255, 240)"] {
        background-color: #0f766e !important; /* Teal Green */
        color: #ffffff !important; /* White text */
        border-radius: 8px;
        padding: 10px;
    }

    .stTextInput > div > div > input {
        border: 2px solid #0073e6;
        border-radius: 8px;
        padding: 10px;
    }
    
    .stButton > button {
        background-color: #0073e6;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
    }

    .stButton > button:hover {
        background-color: #005bb5;
    }

    h1 {
        color: #ffffff;
        text-align: center;
    }

    </style>
    """, unsafe_allow_html=True)


# Function to preprocess user input
def preprocess_input(user_input):
    tokens = word_tokenize(user_input.lower())
    stop_words = set(stopwords.words("english"))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return " ".join(filtered_tokens)

# Intent detection function
def detect_intent(user_input):
    keywords = {
        "symptoms": {"symptom", "pain", "fever", "cough", "headache", "vomiting"},
        "appointment": {"appointment", "schedule", "doctor", "meet", "consultation"},
        "medication": {"medicine", "drug", "prescription", "pill", "dosage"},
        "emergency": {"emergency", "urgent", "hospital", "ambulance"},
    }
    for intent, words in keywords.items():
        if any(word in user_input for word in words):
            return intent
    return "general"

# MediSearch API call function
def medisearch_chatbot(user_input):
    try:
        response = client.send_user_message(
            conversation=[user_input], 
            conversation_id="health_chat"
        )
        if response:
            text_response = response[0]['text']
            cleaned_text = re.sub(r'\[\d+(,\s*\d+)*\] $', '', text_response)
            return cleaned_text.strip()
        else:
            return "Sorry, I couldn't find an answer."
    except Exception as e:
        return "Error connecting to the medical database."

# Appointment confirmation (simulated)
def send_confirmation(name, email, phone, doctor, date, time):
    confirmation_id = random.randint(1000, 9999)
    return (f"📩 Appointment Confirmed!\n"
            f"Patient: {name}\nDoctor: {doctor}\nDate: {date}\nTime: {time}\n"
            f"Confirmation ID: {confirmation_id}\n"
            f"A confirmation message has been sent to {email} and {phone}.")

# Appointment booking system
def book_appointment():
    with st.expander("📅 Book an Appointment", expanded=False):
        if "appointments" not in st.session_state:
            st.session_state.appointments = []

        name = st.text_input("Your Name:")
        email = st.text_input("Email Address:")
        phone = st.text_input("Phone Number:")

        doctor_types = {
            "General Physician": "Dr. Smith",
            "Cardiologist": "Dr. John",
            "Dermatologist": "Dr. Emily",
            "Dentist": "Dr. Brown"
        }
        selected_specialty = st.selectbox("Select a doctor specialty:", list(doctor_types.keys()))
        selected_doctor = doctor_types[selected_specialty]

        appointment_date = st.date_input("Select a date:", min_value=datetime.today())
        available_slots = ["09:00 AM", "10:00 AM", "11:00 AM", "02:00 PM", "03:00 PM", "04:00 PM"]
        appointment_time = st.selectbox("Select a time slot:", available_slots)

        if st.button("Confirm Appointment"):
            if name and email and phone:
                confirmation_message = send_confirmation(name, email, phone, selected_doctor, appointment_date, appointment_time)
                st.session_state.appointments.append(confirmation_message)
                st.success(confirmation_message)
            else:
                st.warning("Please fill in all details to confirm the appointment.")

# Chatbot logic to handle user queries
def healthcare_chatbot(user_input):
    intent = detect_intent(user_input)
    if intent in ["symptoms", "medication"]:
        response = medisearch_chatbot(user_input)
        return f"**Info:**\n- {response}"
    elif intent == "appointment":
        return "📅 You can book an appointment using the form on the right. Let me know if you need help!"
    elif intent == "emergency":
        return "⚠️ **Emergency Alert:** Please call your local emergency number or visit a hospital immediately."
    else:
        return medisearch_chatbot(user_input)

# Streamlit UI
def main():
    add_custom_css()
    st.markdown("<h1 style='text-align: center;'>💉 Healthcare Assistant Chatbot</h1>", unsafe_allow_html=True)

    # Sidebar with quick links and health tips
    st.sidebar.title("🏥 Quick Links")
    st.sidebar.button("Symptom Checker")
    st.sidebar.button("Book Appointment")
    st.sidebar.button("Medication Info")
    st.sidebar.button("Emergency Contacts")
    health_tips = [
        "Drink 8 glasses of water daily to stay hydrated! 💧",
        "Get at least 30 minutes of exercise daily! 🏃‍♂️",
        "Sleep 7-9 hours for optimal health! 😴",
    ]
    st.sidebar.markdown(f"**Health Tip:** {random.choice(health_tips)}")

    # Two-column layout
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("💬 Chat with Me")
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            if message.startswith("👤"):
                st.markdown(f"<div style='padding: 10px; border-radius: 5px; background-color: #e6f3ff;'>{message}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='padding: 10px; border-radius: 5px; background-color: #f0fff0;'>{message}</div>", unsafe_allow_html=True)

        user_input = st.text_input("How can I assist you today?")
        if st.button("Submit"):
            if user_input:
                user_message = f"👤 User: {user_input}"
                st.session_state.messages.append(user_message)
                st.markdown(f"<div style='padding: 10px; border-radius: 5px; background-color: #e6f3ff;'>{user_message}</div>", unsafe_allow_html=True)
                with st.spinner("🩺 Consulting the medical database..."):
                    response = healthcare_chatbot(preprocess_input(user_input))
                bot_message = f"🤖 Healthcare Assistant: {response}"
                st.session_state.messages.append(bot_message)
                st.markdown(f"<div style='padding: 10px; border-radius: 5px; background-color: #f0fff0;'>{bot_message}</div>", unsafe_allow_html=True)
            else:
                st.warning("Please enter a message to get started.")

    with col2:
        book_appointment()
        if "appointments" in st.session_state and st.session_state.appointments:
            st.subheader("📋 Your Appointments")
            for appt in st.session_state.appointments:
                st.markdown(f"<div style='padding: 10px; border: 1px solid #0073e6; border-radius: 5px;'>{appt}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()