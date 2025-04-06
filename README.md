# 🌐 NewsCraftr

**Multilingual AI-Powered News-to-Video Automation Pipeline**

NewsCraftr is an automated pipeline that scrapes news articles, converts them into videos using GPT-4 (text-to-image, narration, and script), translates them into multiple languages, and uploads them directly to YouTube. All orchestrated with Apache Airflow.

---

## 🚀 Features

- 🔎 **News Scraping**: Pulls the latest headlines from configurable sources.
- 🧠 **GPT-4 Powered Script & Visuals**:
  - Summarizes and rewrites news content.
  - Generates images using DALL·E.
  - Creates voiceovers in multiple languages using a TTS API.
- 🎬 **Video Assembly**: Combines visuals and audio into coherent video segments.
- 🌍 **Multilingual Support**: Translate and narrate content in various languages.
- ☁️ **YouTube Auto-Upload**: Automatically uploads finished videos via YouTube Data API.
- 🛠 **Orchestration with Airflow**: Schedule and monitor your workflow seamlessly.

---

## 📦 Tech Stack

- **Python**
- **OpenAI GPT-4 API** (Text, DALL·E)
- **Text-to-Speech API** (e.g. ElevenLabs, Google TTS, etc.)
- **YouTube Data API**
- **Apache Airflow**
- **FFmpeg** (for video assembly)
- **BeautifulSoup / Newspaper3k / etc.** (for scraping)

---

## 🔧 Setup

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/newscraftr.git
cd newscraftr
