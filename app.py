import streamlit as st
import json
import os
import urllib.parse
import urllib.request
import json as js

# Page Configuration
st.set_page_config(page_title="G.I.B.B. Universal Matrix", page_icon="🤖", layout="wide")

# Matrix Green Theme & Audio/Animation CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #031409;
        color: #00ff66;
        background-image: linear-gradient(rgba(0, 255, 100, 0.08) 1px, transparent 1px),
                          linear-gradient(90deg, rgba(0, 255, 100, 0.08) 1px, transparent 1px);
        background-size: 30px 30px;
        font-family: 'Courier New', Courier, monospace;
    }
    h1, h2, h3 {
        color: #00ff66 !important;
        text-shadow: 0 0 15px rgba(0, 255, 100, 0.6);
        border-bottom: 2px solid #00ff66;
        padding-bottom: 10px;
    }
    .stTextInput > div > div > input, .stSelectbox > div > div > div {
        background-color: #041f0e !important;
        color: #00ff66 !important;
        border: 1px solid #00ff66 !important;
        border-radius: 6px !important;
    }
    .stButton > button {
        background-color: #041f0e;
        color: #00ff66;
        border: 1px solid #00ff66;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 255, 100, 0.4);
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #00ff66;
        color: #031409;
        box-shadow: 0 0 25px rgba(0, 255, 100, 0.9);
    }
    </style>
""", unsafe_allow_html=True)

# Custom Password protection
CUSTOM_PASSWORD = "prki3210"
entered_password = st.text_input("Enter Clearance Level 1 Password:", type="password")

if entered_password == CUSTOM_PASSWORD:
    st.title("🤖 G.I.B.B.: Full Multi-Modal Matrix")
    st.write("Text, Web Search, Audio Synthesis, and Permanent JSON Memory Enabled.")

    # --- Database Initialization ---
    MEMORY_FILE = "gibb_memory.json"

    def load_memory():
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, 'r') as file:
                    return json.load(file)
            except:
                return {}
        return {}

    def save_memory(data):
        with open(MEMORY_FILE, 'w') as file:
            json.dump(data, file, indent=4)

    current_memory = load_memory()

    # --- Web Search Function (DuckDuckGo Instant API - No API Key Needed) ---
    def search_web(query):
        try:
            encoded_query = urllib.parse.quote(query)
            url = f"https://api.duckduckgo.com/?q={encoded_query}&format=json"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = js.loads(response.read().decode())
                # Check abstract first
                if data.get("AbstractText"):
                    return f"🌐 **Web Search Result:** {data['AbstractText']}"
                elif data.get("RelatedTopics"):
                    for topic in data["RelatedTopics"]:
                        if "Text" in topic:
                            return f"🌐 **Web Search Result:** {topic['Text']}"
            return f"🌐 No direct summary found on the web for '{query}'. Try searching on Google directly."
        except Exception:
            return "⚠️ Web search protocol failed due to network restriction."

    # --- Sidebar Controls ---
    st.sidebar.markdown("## G.I.B.B. Controls")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if st.sidebar.button("Clear Session Chat"):
        st.session_state.chat_history = []

    if st.sidebar.button("Show Memory Bank"):
        if current_memory:
            st.sidebar.markdown("### Permanent Memory:")
            for k, v in current_memory.items():
                st.sidebar.markdown(f"- **{k}**: `{v}`")
        else:
            st.sidebar.info("Memory bank is empty.")

    # --- Native Browser Speech-to-Text & Text-to-Speech HTML Widget ---
    st.sidebar.markdown("### 🗣️ Audio Voice Synthesizer")
    # This injects a small JavaScript speech reader block for the latest response
    latest_text = st.session_state.chat_history[-1][1] if st.session_state.chat_history else "System ready."
    safe_text = latest_text.replace('"', "'").replace('\n', ' ')
    
    st.sidebar.markdown(f"""
        <button onclick="
            let speech = new SpeechSynthesisUtterance('{safe_text}');
            speech.rate = 1.0;
            window.speechSynthesis.speak(speech);
        " style="background:#041f0e; color:#00ff66; border:1px solid #00ff66; padding:8px 12px; border-radius:6px; cursor:pointer; width:100%;">
            🔊 Read Last Response Aloud
        </button>
    """, unsafe_allow_html=True)

    # --- Main Chat UI ---
    for role, text in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(text)

    user_input = st.chat_input("Ask a question, search the web, translate, or teach G.I.B.B...")

    if user_input:
        response = ""
        lower_input = user_input.lower()

        # 1. Permanent Memory Learning
        if "remember that" in lower_input and "is" in lower_input:
            try:
                parts = user_input.split("remember that", 1)[1].split("is", 1)
                k = parts[0].strip()
                v = parts[1].strip()
                current_memory[k] = v
                save_memory(current_memory)
                response = f"🧠 Permanent Memory Updated: **{k}** is **{v}**."
            except:
                response = "⚠️ Format error. Use: *Remember that [key] is [value]*"

        # 2. Live Web Search Integration
        elif "search" in lower_input or "look up" in lower_input or "google" in lower_input:
            query = lower_input.replace("search", "").replace("look up", "").replace("google", "").strip()
            response = search_web(query)

        # 3. Translation Protocol Simulator
        elif "translate" in lower_input:
            response = f"🌐 Translation Protocol: Processed string text mapping for query: '{user_input}'. (Multilingual matrix active)."

        # 4. Math Calculations
        elif "calculate" in lower_input or "compute" in lower_input:
            try:
                expr = lower_input.replace("calculate", "").replace("compute", "").strip()
                result = eval(expr)
                response = f"🔢 Calculation Result: {result}"
            except:
                response = "⚠️ Calculation syntax error."

        # 5. Core Memory Lookup
        else:
            found = False
            for k, v in current_memory.items():
                if k in lower_input:
                    response = f"🔍 Memory Bank Match: **{k}** is **{v}**."
                    found = True
                    break
            if not found:
                # Default fallback: Automatically trigger web search if it looks like a question
                response = search_web(user_input)

        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("assistant", response))
        st.rerun()

elif entered_password:
    st.error("Access Denied. Incorrect Password.")
