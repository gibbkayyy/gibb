import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder
import os
import io

st.set_page_config(page_title="G.I.B.B. AI System", page_icon="🤖", layout="wide")

st.title("🤖 G.I.B.B.: Core Systems Online")
st.write("Advanced AI assistant with memory, text, voice, and vision capabilities.")

# Get Gemini API Key from environment or sidebar input
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    api_key = st.sidebar.text_input("Enter your Gemini API Key", type="password")

if api_key:
    client = genai.Client(api_key=api_key)
    model_name = "gemini-2.5-flash"

    # Initialize chat session history for persistent memory
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = client.chats.create(model=model_name)

    # Navigation Modes
    mode = st.sidebar.radio("Select System Mode:", [
        "💬 Text Chat & Memory", 
        "🎙️ Voice Command (Speech-to-Speech)", 
        "🔍 Visual Lens Analysis"
    ])

    # ---------------------------------------------------------
    # MODE 1: TEXT CHAT & MEMORY
    # ---------------------------------------------------------
    if mode == "💬 Text Chat & Memory":
        st.header("💬 Text Interface & Memory Matrix")
        st.write("G.I.B.B. remembers everything discussed in this session.")

        # Render chat history
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
                    
                    # Text-to-Speech Audio Generation
                    tts = gTTS(text=response.text, lang='en', slow=False)
                    audio_io = io.BytesIO()
                    tts.write_to_fp(audio_io)
                    st.audio(audio_io.getvalue(), format="audio/mp3")

    # ---------------------------------------------------------
    # MODE 2: VOICE COMMAND (SPEECH-TO-SPEECH)
    # ---------------------------------------------------------
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
                    
                    # Generate speech audio output
                    tts = gTTS(text=response.text, lang='en', slow=False)
                    speech_io = io.BytesIO()
                    tts.write_to_fp(speech_io)
                    st.audio(speech_io.getvalue(), format="audio/mp3")

    # ---------------------------------------------------------
    # MODE 3: VISUAL LENS ANALYSIS
    # ---------------------------------------------------------
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
    st.info("⚠️ Please enter your Gemini API Key in the sidebar to initialize G.I.B.B.")
