# 🏥 Healthcare Assistant Chatbot

A **Streamlit-based AI-powered chatbot** designed to assist users with healthcare-related queries, book appointments, provide medication recommendations, and more.

---

## 🚀 Features
- 💬 **AI Chatbot** – Provides answers to health-related questions.
- 📅 **Appointment Booking** – Users can book doctor appointments.
- 💊 **Medication Info** – Offers details on prescribed medications.
- 🚑 **Emergency Contacts** – Provides quick access to emergency numbers.
- 🔑 **Uses API Integration** – Requires API keys for chatbot functionality.

---

## 🔧 Project Structure
- **`app.py`** – Main Streamlit chatbot application handling UI and chatbot logic.
- **`nn.py`** – Script to download required NLTK resources.
- **`requirements.txt`** – Lists dependencies needed for installation.

---

## 🔧 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Vinay2314/AI-Healthcare-Chatbot.git
cd AI-Healthcare-Chatbot
```

### 2️⃣ Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Get API Keys
This chatbot requires API keys to function properly. Follow these steps:

1. **Obtain API Keys**:  
   - Sign up for an account with the required API provider (e.g., OpenAI, MedAPI, or any other API you use).
   - Retrieve your API keys from the provider’s dashboard.

2. **Create a `.env` File**:  
   Inside the project folder, create a file named `.env` and add your API keys like this:
   ```env
   API_KEY=your_api_key_here
   ```
   
3. **Load API Keys in Code**:  
   The application reads the API key using the `dotenv` package.

### 5️⃣ Run the Streamlit App
```bash
streamlit run app.py
```

---

## 🌍 Live Demo
🔗 **[Try the Live App Here](https://your-streamlit-app-link.streamlit.app/)**  
*(Replace with your actual Streamlit deployment link.)*

---

## 🛠 Deployment on Streamlit Cloud
To deploy the chatbot on **Streamlit Cloud**:
1. Push the code to **GitHub**.
2. Go to [Streamlit Cloud](https://share.streamlit.io/).
3. Click "New App", select your GitHub repo, and deploy!
4. **Set Environment Variables** on Streamlit:
   - In the Streamlit Cloud settings, add `API_KEY` under **Secrets Management**.

---

## 📷 Screenshots
*(Add a screenshot of your chatbot interface here.)*

---

## 🤝 Contributing
Want to improve this chatbot?  
Fork the repo, create a new branch, and submit a **pull request**.

---

### 🚀 **Happy Coding!**
