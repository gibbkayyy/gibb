import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder
import os
import io

# Page Configuration
st.set_page_config(page_title="G.I.B.B. AI System", page_icon="🤖", layout="wide")

# Custom CSS to match your neon cyberpunk theme
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f0e;
        color: #e0e0e0;
        background-image: linear-gradient(rgba(0, 255, 100, 0.02) 1px, transparent 1px),
                          linear-gradient(90deg, rgba(0, 255, 100, 0.02) 1px, transparent 1px);
        background-size: 30px 30px;
    }
    [data-testid="stSidebar"] {
        background-color: #070a09;
        border-right: 1px solid rgba(0, 255, 100, 0.2);
    }
    h1, h2, h3 {
        color: #ffffff !important;
        text-shadow: 0 0 10px rgba(0, 255, 100, 0.4);
        font-family: monospace;
    }
    .stButton > button {
        background-color: #121a16;
        color: #00ff66;
        border: 1px solid #00ff66;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 255, 100, 0.2);
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #00ff66;
        color: #070a09;
        box-shadow: 0 0 20px rgba(0, 255, 100, 0.8);
    }
    input, textarea, .stTextInput > div > div > input {
        background-color: #121a16 !important;
        color: #ffffff !important;
        border: 1px solid rgba(0, 255, 100, 0.3) !important;
        border-radius: 6px !important;
    }
    input:focus, textarea:focus {
        border-color: #00ff66 !important;
        box-shadow: 0 0 10px rgba(0, 255, 100, 0.5) !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 G.I.B.B.: Core Systems Online")
st.write("Advanced AI assistant with memory, text, voice, and vision capabilities.")

# Set your custom password here
CUSTOM_PASSWORD = "prki3210"

# Password prompt input in the sidebar
entered_password = st.sidebar.text_input("Enter Authorized Password:", type="password")

# Check if the entered password matches
if entered_password == CUSTOM_PASSWORD:
    st.sidebar.success("Access Granted")
    
    # ⚠️ NOTE: Put your Google Gemini API key inside the quotes below 
    # so G.I.B.B. has a working brain behind the scenes!
    api_key = "YOUR_API_KEY_HERE"
    
    if api_key and api_key != "YOUR_API_KEY_HERE":
        client = genai.Client(api_key=api_key)
        model_name = "gemini-2.5-flash"

        if "chat_session" not in st.session_state:
            st.session_state.chat_session = client.chats.create(model=model_name)

        mode = st.sidebar.radio("Select System Mode:", [
            "💬 Text Chat & Memory", 
            "🎙️ Voice Command (Speech-to-Speech)", 
            "🔍 Visual Lens Analysis"
        ])

        # MODE 1: TEXT CHAT
        if mode == "💬 Text Chat & Memory":
            st.header("💬 Text Interface & Memory Matrix")
            st.write("G.I.B.B. remembers everything discussed in this session.")

            for message in st.session_state.chat_session.get_history():
                role = "user" if message.role == "user" else "assistant"
                with st.chat_message(role):
                    for part in message.parts:
                        if part.text:
                            st.markdown(part.text)

            user_input = st.chat_input("Enter command for G.I.B.B....")
            if user_input:
                with st.chat_message("user"):
                    st.markdown(user_input)
                
                with st.chat_message("assistant"):
                    with st.spinner("Processing..."):
                        response = st.session_state.chat_session.send_message(user_input)
                        st.markdown(response.text)
                        
                        tts = gTTS(text=response.text, lang='en', slow=False)
                        audio_io = io.BytesIO()
                        tts.write_to_fp(audio_io)
                        st.audio(audio_io.getvalue(), format="audio/mp3")

        # MODE 2: VOICE COMMAND
        elif mode == "🎙️ Voice Command (Speech-to-Speech)":
            st.header("🎙️ Voice Command Center")
            st.write("Record your voice command. G.I.B.B. will process it, answer, and speak back.")

            audio_bytes = audio_recorder(text="Click to record voice", icon_size="3x")

            if audio_bytes:
                st.audio(audio_bytes, format="audio/wav")
                
                if st.button("Transmit Audio to G.I.B.B."):
                    with st.spinner("Analyzing audio input..."):
                        response = client.models.generate_content(
                            model=model_name,
                            contents=[
                                types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav"),
                                "Listen to this voice command, transcribe it, and respond concisely as G.I.B.B."
                            ]
                        )
                        st.markdown("### G.I.B.B. Response:")
                        st.write(response.text)
                        
                        tts = gTTS(text=response.text, lang='en', slow=False)
                        speech_io = io.BytesIO()
                        tts.write_to_fp(speech_io)
                        st.audio(speech_io.getvalue(), format="audio/mp3")

        # MODE 3: VISUAL LENS
        elif mode == "🔍 Visual Lens Analysis":
            st.header("🔍 Visual Detection Matrix")
            st.write("Capture or upload an image for instant analysis.")

            uploaded_file = st.camera_input("Take photo") or st.file_uploader("Upload image", type=["jpg", "png", "jpeg"])

            if uploaded_file:
                image = Image.open(uploaded_file)
                st.image(image, caption="Target Acquired", use_column_width=True)

                if st.button("Run Visual Diagnostics"):
                    with st.spinner("Analyzing visuals..."):
                        analysis = client.models.generate_content(
                            model=model_name,
                            contents=[image, "Identify this object accurately and provide a clean breakdown of what it is."]
                        )
                        st.success("Diagnostics Complete:")
                        st.markdown(analysis.text)
    else:
        st.warning("⚠️ Access granted via password, but you still need to paste a working Gemini API key into the `api_key` variable inside `app.py` so G.I.B.B. has a brain!")

else:
    if entered_password:
        st.sidebar.error("Incorrect Password")
    st.info("🔒 Enter your authorized password (`prki3210`) in the sidebar to unlock G.I.B.B.")
