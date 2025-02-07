import streamlit as st
import openai
import tempfile
import os
import json
import logging
from openai import OpenAI

# Configure Logging
logging.basicConfig(
    filename="app.log", 
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Streamlit App Title
st.title("🎙️ Speech Analysis using OpenAI Whisper API")

# Store API Key in Session State
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = ""

# Sidebar for OpenAI API Key input
st.sidebar.subheader("🔑 API Key Configuration")
api_key_input = st.sidebar.text_input(
    "Enter OpenAI API Key", 
    type="password", 
    value=st.session_state.openai_api_key
)

# Save API Key to Session State
if api_key_input:
    st.session_state.openai_api_key = api_key_input

# Upload Audio File
audio_file = st.file_uploader("📂 Upload an Audio File", type=["mp3", "wav", "m4a"])

# Input Topic/Question
topic = st.text_area("📝 Enter the Topic/Question")

# Default Parameters
default_params = [
    {"name": "English Fluency", "description": "Measures speed, pauses, and hesitations."},
    {"name": "Vocabulary", "description": "Evaluates richness and diversity of words used."},
    {"name": "Grammar", "description": "Checks grammatical correctness."},
    {"name": "Relevance to the Topic", "description": "Assesses response alignment with the topic."}
]

# Load or Initialize Parameters
if "parameters" not in st.session_state:
    st.session_state.parameters = default_params

# Display Current Parameters
st.subheader("⚙️ Analysis Parameters")

def render_parameters():
    """Renders the analysis parameters in the Streamlit UI."""
    for idx, param in enumerate(st.session_state.parameters):
        col1, col2, col3 = st.columns([3, 5, 2])
        col1.write(f"**{param['name']}**")
        col2.write(param["description"])
        if col3.button("❌ Delete", key=f"delete_{idx}"):
            st.session_state.parameters.pop(idx)
            st.rerun()

render_parameters()

# Add New Parameter
st.subheader("➕ Add Custom Parameter")
with st.form("add_param_form"):
    param_name = st.text_input("Parameter Name")
    param_desc = st.text_area("Parameter Description")
    submitted = st.form_submit_button("Add Parameter")
    if submitted and param_name.strip():
        st.session_state.parameters.append({"name": param_name, "description": param_desc})
        st.rerun()

def transcribe_audio(audio_path, api_key):
    """Transcribes an audio file using OpenAI Whisper API."""
    if not api_key:
        st.error("🚨 Please enter a valid OpenAI API Key in the sidebar.")
        return None

    try:
        client = OpenAI(api_key=api_key)
        with open(audio_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-1",
                response_format="verbose_json",
                timestamp_granularities=["word"]
            )
        logger.info("Audio transcription successful")
        return response
    except Exception as e:
        logger.error(f"Error during transcription: {str(e)}")
        st.error(f"❌ Error during transcription: {str(e)}")
        return None

def analyze_fluency(transcription_data):
    """Analyzes fluency of transcribed text."""
    if not transcription_data:
        return None

    duration = transcription_data.duration or 0
    words = transcription_data.words or []

    total_words = len(words)
    speech_rate = (total_words / (duration / 60)) if duration > 0 else 0

    pauses = 0
    prev_end = 0
    for word_data in words:
        start_time = float(word_data.start)
        if start_time - prev_end > 0.4:
            pauses += 1
        prev_end = float(word_data.end)

    fluency_score = max(0, min(100, (200 - (pauses * 5)) / 2)) / 10

    fluency_results = {
        "Total Words": total_words,
        "Speech Duration (seconds)": duration,
        "Words Per Minute (WPM)": round(speech_rate, 2),
        "Pauses Detected": pauses,
        "Fluency Score (0-10)": round(fluency_score, 2)
    }

    logger.info("Fluency analysis complete")
    return fluency_results

def generate_structured_analysis(transcription_text, api_key, fluency_results):
    """Generates a structured analysis of speech using GPT-4o-mini."""
    if not api_key:
        st.error("🚨 OpenAI API Key is missing!")
        return None

    json_schema = {
        "type": "object",
        "properties": {},
        "required": [],
        "strict": "true",
    }

    for param in st.session_state.parameters:
        param_key = param['name'].strip().lower().replace(" ", "_")
        json_schema["properties"][param_key] = {"type": "number" , "description":param['description']}
        json_schema["required"].append(param_key)

    json_schema["properties"]["ReasoningForScores"] = {"type": "string", "description":"Reason For all the Scores"}
    json_schema["required"].append("ReasoningForScores")
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            temperature=0.00125,
            messages=[
                {
                    "role": "system",
                    "content": f"You are an AI language model that evaluates speech transcription based on multiple criteria. Consider {topic} as the Topic/Question for relevance. Score between 0-10 make sure that bad results can be given 0 if they are really bad and 10 if they are really good"
                },
                {
                    "role": "user",
                    "content": f"Analyze the following text Strictly! and return a structured JSON output:\n\nText:\n\n {transcription_text.text}\n\nASR Meta(Based on Speakg speed): {fluency_results} if Stopping words like `um, stammer pauses...` are detected make sure You reduce the fluency score by a little for each pause ,Final Score should be based on Speech Speed and text to search for pause phrases.\n\n Calculate Relevance to topic Strictly if no relevancy is Found you can give low values like 0-3!"
                }
            ],
            tool_choice="required",
            tools=[{"type": "function", "function": {"name": "score_asr", "parameters": json_schema}}]
        )
        logger.info("Structured analysis generated successfully")
        return response.choices[0].message.tool_calls[0].function.arguments
    except Exception as e:
        logger.error(f"Error during structured analysis: {str(e)}")
        st.error(f"❌ Error during structured analysis: {str(e)}")
        return None

# Analyze Speech Button
if st.button("🚀 Analyze Speech", disabled=not audio_file):
    if not st.session_state.openai_api_key:
        st.error("⚠️ OpenAI API Key is missing! Enter your API key in the sidebar.")
    else:
        with st.spinner("Transcribing with OpenAI Whisper API... ⏳"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                temp_audio.write(audio_file.read())
                temp_audio_path = temp_audio.name
            
            transcription_data = transcribe_audio(temp_audio_path, st.session_state.openai_api_key)
            
            if transcription_data and transcription_data.text:
                st.subheader("📊 Fluency Analysis")
                fluency_results = analyze_fluency(transcription_data)
                st.json(fluency_results)
                
                with st.spinner("Generating structured analysis... ⏳"):
                    structured_analysis = generate_structured_analysis(transcription_data, st.session_state.openai_api_key, fluency_results)
                    if structured_analysis:
                        st.subheader("📊 Parametric Analysis")
                        st.table(structured_analysis)
            else:
                st.error("❌ Failed to transcribe the audio.")

            os.remove(temp_audio_path)
