
import streamlit as st
from google.cloud import translate_v2 as translate
from gtts import gTTS
import speech_recognition as sr
import pyttsx3
from textblob import TextBlob
from langdetect import detect
import tempfile
from fpdf import FPDF
import os

# ✅ Init Translate client
client = translate.Client()

# ✅ Init TTS engine for accent/voice
engine = pyttsx3.init()

# ✅ Streamlit config
st.set_page_config(page_title="🌐✨ Ultimate AI Voice Translator", page_icon="🎙️")
st.title("🌐✨ Speak Once, Be Heard Everywhere! 🎙️")
st.write("Real-time speech-to-speech translator with voice options, sentiment, download & more! 🚀")

# ✅ Available languages
languages = {
    "Hindi": "hi",
    "Tamil": "ta",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Japanese": "ja"
}

# ✅ Voice options (basic pyttsx3)
voices = engine.getProperty('voices')
voice_options = [f"{v.id}" for v in voices]
selected_voice = st.selectbox("🎙️ Select TTS Voice:", voice_options)

# ✅ Speech input
if st.button("🎤 Speak Now"):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        st.info("Listening... Speak now!")
        audio = recognizer.listen(source)
    try:
        text_to_translate = recognizer.recognize_google(audio)
        st.success(f"**You said:** {text_to_translate}")
    except:
        st.error("Could not recognize speech.")
        text_to_translate = ""
else:
    text_to_translate = st.text_area("✏️ Or type your text:", placeholder="Type something...")

# ✅ Auto-detect language
if text_to_translate.strip():
    detected_lang = detect(text_to_translate)
    st.write(f"🌐 **Detected Language:** {detected_lang}")

# ✅ Target language
selected_language = st.selectbox("🌍 Select target language:", list(languages.keys()))
target_lang_code = languages[selected_language]

# ✅ Sentiment
if text_to_translate.strip():
    blob = TextBlob(text_to_translate)
    sentiment = blob.sentiment.polarity
    st.write(f"🚦 **Sentiment:** {'Positive' if sentiment > 0 else 'Negative' if sentiment < 0 else 'Neutral'}")

# ✅ Translate, speak, download, save history
if st.button("🎯 Translate & Speak"):
    if text_to_translate.strip() == "":
        st.warning("Please provide input.")
    else:
        result = client.translate(text_to_translate, target_language=target_lang_code)
        translated_text = result['translatedText']
        st.success(f"**Translated ({selected_language}):** {translated_text}")

        # ✅ gTTS for voice file
        tts = gTTS(translated_text, lang=target_lang_code)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            st.audio(fp.name, format="audio/mp3")
            st.download_button(label="⬇️ Download Audio", data=open(fp.name, "rb"), file_name="translation.mp3", mime="audio/mp3")

        # ✅ pyttsx3 local TTS
        engine.setProperty('voice', selected_voice)
        engine.say(translated_text)
        engine.runAndWait()

        # ✅ Store in session history
        if 'history' not in st.session_state:
            st.session_state['history'] = []
        st.session_state['history'].append((text_to_translate, translated_text))

# ✅ Show history & copy
if 'history' in st.session_state:
    st.write("📝 **Translation History:**")
    for orig, trans in st.session_state['history']:
        st.write(f"**Input:** {orig}")
        st.write(f"**Translated:** {trans}")

# ✅ Export as PDF
if st.button("📄 Export History as PDF"):
    if 'history' in st.session_state:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for orig, trans in st.session_state['history']:
            pdf.multi_cell(0, 10, f"Input: {orig}\nTranslated: {trans}\n")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            pdf.output(tmp_pdf.name)
            st.download_button("⬇️ Download PDF", data=open(tmp_pdf.name, "rb"), file_name="translation_history.pdf", mime="application/pdf")

# ✅ Simple conversation mode starter
if st.button("🤝 Start Conversation Mode (Prototype)"):
    st.info("Speak → Translate → Reply → Repeat! (Basic demo)")
    st.write("👉 Build your 2-way loop here!")

# 👇👇👇 Real Conversation Mode — FULL LOOP 👇👇👇

st.header("🤝 Real Conversation Mode")

# 1️⃣ Setup participants & languages
col1, col2 = st.columns(2)
with col1:
    speaker_A_lang = st.selectbox("🎙️ Speaker A's Language", list(languages.keys()), key="A_lang")
with col2:
    speaker_B_lang = st.selectbox("🎙️ Speaker B's Language", list(languages.keys()), key="B_lang")

speaker_A_code = languages[speaker_A_lang]
speaker_B_code = languages[speaker_B_lang]

# 2️⃣ Init session state for convo log
if 'conversation_log' not in st.session_state:
    st.session_state['conversation_log'] = []

# 3️⃣ Who's turn? A or B
if 'turn' not in st.session_state:
    st.session_state['turn'] = 'A'

st.write(f"🗣️ It's **Speaker {st.session_state['turn']}'s turn**")

# 4️⃣ Speak button
if st.button("🎤 Speak"):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        st.info("🎙️ Listening...")
        audio = recognizer.listen(source)

    try:
        spoken_text = recognizer.recognize_google(audio)
        st.success(f"**You said:** {spoken_text}")

        # Detect lang (optional, because we already know)
        detected_lang = detect(spoken_text)
        st.write(f"🌐 Detected: {detected_lang}")

        # Translate: A->B or B->A
        if st.session_state['turn'] == 'A':
            translated = client.translate(spoken_text, target_language=speaker_B_code)['translatedText']
            tts_lang = speaker_B_code
        else:
            translated = client.translate(spoken_text, target_language=speaker_A_code)['translatedText']
            tts_lang = speaker_A_code

        st.success(f"**Translation:** {translated}")

        # Speak it
        tts = gTTS(translated, lang=tts_lang)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            st.audio(fp.name, format="audio/mp3")

        # Save turn in convo log
        st.session_state['conversation_log'].append({
            'speaker': st.session_state['turn'],
            'spoken': spoken_text,
            'translated': translated
        })

        # Switch turn!
        st.session_state['turn'] = 'B' if st.session_state['turn'] == 'A' else 'A'

    except Exception as e:
        st.error(f"😬 Could not process speech: {e}")

# 5️⃣ Show conversation history
st.write("📝 **Conversation Log:**")
for entry in st.session_state['conversation_log']:
    st.write(f"**Speaker {entry['speaker']} said:** {entry['spoken']}")
    st.write(f"**Translation:** {entry['translated']}")
    st.write("---")

# 6️⃣ Reset convo
if st.button("🔄 Reset Conversation"):
    st.session_state['conversation_log'] = []
    st.session_state['turn'] = 'A'
    st.success("Conversation reset!")
