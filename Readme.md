# 🎙️ Speech Analysis using OpenAI Whisper API

This Streamlit application leverages OpenAI's Whisper API to transcribe speech and analyze fluency, vocabulary, grammar, and relevance to a given topic.

---

## 🌍 Live Demo
You can try out the deployed application here:  
🔗 **[Byte-XL ASR Web App](https://byte-xl-asr.streamlit.app/)**

---

## 📌 Features
- **Speech Transcription**: Uses OpenAI Whisper API to convert audio into text.
- **Fluency Analysis**: Calculates Words Per Minute (WPM), pauses, and fluency score.
- **Grammar & Vocabulary Check**: Analyzes speech for grammatical correctness and richness of vocabulary.
- **Topic Relevance Analysis**: Evaluates how well the response aligns with the given topic.
- **Custom Scoring Parameters**: Allows users to define their own evaluation criteria.

---

## ⚙️ Setup & Installation

### 1️⃣ **Clone the Repository**
```sh
git clone https://github.com/aakarshhh/byte-xl-audllm.git
cd byte-xl-audllm
```

### 2️⃣ **Create a Virtual Environment (Recommended)**
```sh
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ **Install Dependencies**
Ensure you have Python 3.8+ installed. Install dependencies from `requirements.txt`:

```sh
pip install -r requirements.txt
```

---

## 🚀 Running the Application Locally
Once dependencies are installed, start the Streamlit app:

```sh
streamlit run app.py
```

This will launch the web interface in your default browser.

---

## 📂 File Structure
```
byte-xl-audllm/
│── app.py                # Main Streamlit application
│── requirements.txt       # Required Python dependencies
│── README.md              # Setup & execution instructions
│── app.log                # Log file for debugging (generated after execution)
```

---

## 🔑 API Key Configuration
To use OpenAI's Whisper API, you need an API key:

1. Get your **OpenAI API key** from [OpenAI](https://platform.openai.com/).
2. Enter it in the sidebar of the application when prompted.

---

## 🖥️ Running on Streamlit Cloud
The app is already deployed at:  
🔗 **[Byte-XL ASR Web App](https://byte-xl-asr.streamlit.app/)**

If you wish to deploy it yourself:
1. Sign up at [Streamlit Cloud](https://streamlit.io/cloud).
2. Fork the repository and connect it to Streamlit Cloud.
3. Configure the environment variables (if needed).
4. Deploy the app!

---

## 🔍 Logs & Debugging
The application logs errors and execution details in `app.log`. If you encounter issues, check the log file:

```sh
cat app.log  # macOS/Linux
type app.log # Windows
```

---

## 🛠️ Troubleshooting
- **Missing dependencies?** Run `pip install -r requirements.txt` again.
- **Python version mismatch?** Ensure you are using Python 3.8+.
- **OpenAI API error?** Check if your API key is valid and has sufficient quota.

---

## 🤝 Contributions
Feel free to contribute by submitting issues or pull requests.

---

### **Summary of What's Included**
✅ **Setup Instructions**  
✅ **Installation of Dependencies**  
✅ **Execution Steps**  
✅ **Live Deployment Link**  
✅ **API Key Configuration**  
✅ **Debugging & Logging**  
✅ **Project Structure Explanation**  
✅ **Streamlit Cloud Deployment Guide**  
✅ **Troubleshooting Section**  
✅ **Contribution & License Info**  

---