# AI-Voice-Translator


# 🌐✨ Ultimate AI Voice Translator 🎙️

**Speak Once, Be Heard Everywhere!**

A real-time **speech-to-speech translator** that does it all:
- 🎤 Speak into your mic
- 🌍 Auto-detect input language
- 🔄 Translate to any supported language
- 🗣️ Play the translated speech aloud
- ✅ Pick voices, accents & download audio
- 📝 Save your translation history & export as PDF
- 🤝 Real **Conversation Mode** — 2-way live interpreter loop!

---

## 🚀 Features

✅ **Speech-to-Speech Translation**  
Speak or type → translate → hear the translation spoken.

✅ **Voice & Accent Options**  
Pick TTS voices using `pyttsx3` or `gTTS`.

✅ **Auto Language Detection**  
Supports input text in any language — detects it automatically.

✅ **Sentiment Analysis**  
See if your text feels positive, negative or neutral!

✅ **Download Audio**  
Save your translated audio as `.mp3` instantly.

✅ **Translation History**  
Tracks everything you translate in the session.

✅ **Export as PDF**  
Download your full translation history as a clean PDF.

✅ **Conversation Mode**  
A full prototype of a live interpreter — Speaker A ↔️ Speaker B.

---

## 🧩 Tech Stack

- **Python**
- **Streamlit** (web app UI)
- **Google Cloud Translate API**
- **gTTS** (`google Text-to-Speech`)
- **speech_recognition**
- **pyttsx3** (offline voice synthesis)
- **TextBlob** (sentiment)
- **langdetect**
- **FPDF** (PDF export)

---

## 📂 Project Structure

```plaintext
📁 your-project-folder/
 ├── app.py
 ├── your-service-account.json
```
---

## 🔑 Setup: Google Cloud Credentials
- 1️⃣ Create a Google Cloud Translate API project.
- 2️⃣ Download your Service Account JSON key.
- 3️⃣ Save it in your project folder.
- 4️⃣ Set your environment variable before running:

Windows (PowerShell):
- $env:GOOGLE_APPLICATION_CREDENTIALS = "C:\full\path\to\your\service-account.json"
- streamlit run app.py
Windows (CMD):
- set GOOGLE_APPLICATION_CREDENTIALS=C:\full\path\to\your\service-account.json
- streamlit run app.py

🏃‍♀️ Run Locally
1️⃣ Install requirements:
- pip install -r requirements.txt
2️⃣ Run it:
-streamlit run app.py
