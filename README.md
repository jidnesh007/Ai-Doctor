# 🩺  AI Doctor with Vision and Voice

An AI-powered healthcare assistant that allows users to upload **medical images**, **ask questions** via **text**, **recorded voice**, or **uploaded audio files**, and get expert-style medical responses in **English**, **Hindi**, or **Marathi** — all delivered in **natural voice output** using **gTTS** or **ElevenLabs**.

---

## 🚀 Features

- ✅ **Multimodal Inputs**: Accepts image uploads, text input, live voice recordings, or uploaded audio files.
- 🌐 **Multilingual Support**: Understands and responds in **English**, **Hindi**, or **Marathi**.
- 🧠 **Image Analysis**: Uses vision-language models to analyze medical images and respond like a professional doctor.
- 🗣️ **Text-to-Speech Output**: Delivers responses using gTTS (free) or ElevenLabs (premium).
- 🎤 **Speech Recognition**: Transcribes audio using **GROQ API with Whisper Large V3** model.

---

## 🛠️ Tech Stack

- Python 🐍
- [Gradio](https://www.gradio.app/) – UI for model interaction
- [gTTS](https://pypi.org/project/gTTS/) – Free text-to-speech
- [ElevenLabs](https://www.elevenlabs.io/) – Premium voice synthesis
- [Whisper (GROQ)](https://console.groq.com/) – Speech-to-text engine
- Vision-Language Model: `meta-llama/llama-4-scout-17b-16e-instruct`

---

## 🧪 Sample Use Cases

- Upload an X-ray and ask: _“What do you think is wrong?”_
- Say in Hindi: _“मुझे बुखार और खांसी है”_ and get a diagnosis and audio reply.
- Provide symptoms like: _“My child has a rash on the skin”_ with/without image.

---

## 📸  Interface

![127 0 0 1_7860_ (1)](https://github.com/user-attachments/assets/f95af149-314a-4215-943c-6c26ba8cc3b1)

---

![127 0 0 1_7860_ (2)](https://github.com/user-attachments/assets/581457f9-58e7-428a-b279-caded03b1c8d)


---

## 📂 Folder Structure

```

project/
│
├── brain.py                  # Image encoding & analysis
├── voice.py                  # Audio recording & transcription
├── doc_voice.py              # Text-to-speech using gTTS / ElevenLabs
├── gradio_app.py             # Main Gradio app
└── assets/                   # Optional: Store sample images/audio

````

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/jidnesh007/Ai-Doctor.git
cd multilingual-ai-doctor
````

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

You may also need:

```bash
pip install gradio gtts openai requests
```

### 3. Set Environment Variables

Create a `.env` file or export:

```bash
export GROQ_API_KEY=your_groq_api_key
```

### 4. Run the App

```bash
python gradio_app.py
```

---

## 🔐 Notes on API Usage

* **GROQ Whisper**: Used for fast and accurate speech-to-text conversion.
* **ElevenLabs (optional)**: You must configure your API key and voice ID in `doc_voice.py` if you wish to use ElevenLabs voices.

---

## 🧠 AI Prompt Strategy

Each language has custom medical-style prompts designed to make AI behave like a **professional doctor**, not a generic chatbot. Responses are limited to **2 concise sentences** and mimic human tone.

---

## 💬 Languages Supported

| Language | Code |
| -------- | ---- |
| English  | `en` |
| Hindi    | `hi` |
| Marathi  | `mr` |

