# 🔄 Universal File Converter

A powerful, all-in-one CLI tool designed to convert, compress, and enhance a wide variety of file formats. Built with Python, it leverages standard libraries for data processing, `ffmpeg` for media handling, and Google Gemini AI for content enhancement.

Whether you need to turn a batch of Markdown files into Word docs, optimize a FLAC audio library, or polish a document's grammar, this tool has you covered.

---

## ✨ Key Features

*   **Universal Conversion**: Seamlessly convert between Image, Video, Audio, Document, and Data formats.
*   **Media Optimization (`-r`)**: Smart compression for Images, Audio (e.g., FLAC compression, MP3 bitrate), and Video.
*   **AI Enhancement (`--enhance`)**: Use Google Gemini to professionally edit and improve text content during conversion.
*   **Granular Progress Tracking**: Real-time progress bars for file batches and detailed, time-based tracking for long media conversions (ETA included).
*   **Batch Processing**: Handle dozens of files at once with a single command.
*   **Smart Collision Handling**: Automatically prevents file overwrites by appending `_optimized` or `_enhanced` suffixes when necessary.

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

1.  **Python 3.9+**
2.  **FFmpeg** (Crucial for Audio & Video conversion)
    *   **macOS**: `brew install ffmpeg`
    *   **Windows**: [Download FFmpeg](https://ffmpeg.org/download.html) or `winget install ffmpeg`
    *   **Linux**: `sudo apt install ffmpeg`
3.  **Microsoft Word** (macOS/Windows) *or* **LibreOffice** (Linux)
    *   Required for `.docx` to `.pdf` conversions.

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/file_converter.git
cd file_converter
```

### 2. Set up Virtual Environment (Recommended)
It's best practice to run this tool in an isolated environment.

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Gemini API Key (Optional)
To use the AI enhancement features (`-e`), you need a Google Gemini API key.
1.  Get your key from [Google AI Studio](https://aistudio.google.com/).
2.  Create a `.env` file in the project root:
    ```env
    GEMINI_API_KEY=your_actual_api_key_here
    ```

---

## 🚀 Usage Guide

The general syntax is:
```bash
python3 convert.py <input_files> [output_folder] [flags]
```

### 🎵 Audio & Video Conversion
Convert media files easily. The tool uses `ffmpeg` under the hood.

**Convert WAV to FLAC:**
```bash
python3 convert.py recording.wav -t flac
```

**Optimize Audio (e.g., Max Compression for FLAC, Standard Bitrate for MP3):**
*This creates `recording_optimized.flac` if the input is already FLAC.*
```bash
python3 convert.py recording.flac -r
```

**Convert Video to MP4:**
```bash
python3 convert.py movie.mkv -t mp4
```

### 📄 Document Conversion
Robust conversion between Markdown, Word, and PDF.

**Markdown to Word (.docx):**
*Preserves bold, italics, lists, and headers.*
```bash
python3 convert.py notes.md -t docx
```

**Word to PDF:**
```bash
python3 convert.py report.docx -t pdf
```

### ✨ AI Enhancement
Improve the tone and grammar of your text documents while converting them.

**Enhance text:**
```bash
python3 convert.py rough_draft.txt -t md -e
```

### 📉 Batch Processing
Convert all images in a folder (using shell globbing) to a specific output directory.

```bash
python3 convert.py *.png ./converted_images -t jpg
```

### ⚡ Single File Optimization
Quickly optimize a file without changing its format.

```bash
# Creates image_optimized.jpg
python3 convert.py image.jpg -r
```

---

## 📂 Supported Formats Matrix

| Category | Extensions | Conversion Notes |
| :--- | :--- | :--- |
| **Audio** | `.mp3`, `.wav`, `.aac`, `.flac`, `.ogg`, `.m4a`, `.opus` | Supports bitrate optimization and FLAC compression levels. |
| **Video** | `.mp4`, `.mkv`, `.mov`, `.avi`, `.webm`, `.ogv`, `.ogm` | Supports H.264 encoding and CRF optimization. |
| **Images** | `.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`, `.tiff` | RGB conversion for compatibility; Quality reduction with `-r`. |
| **Documents** | `.docx`, `.pdf`*, `.md`, `.mdx`, `.html`, `.txt` | *.pdf output only (from .docx). Markdown supports rich formatting. |
| **Data** | `.csv`, `.json`, `.xlsx` | Inter-convertible using Pandas. |

---

## 🤝 Collaboration & Development

We welcome contributions! If you want to improve this tool, here is how you can help:

### Project Structure
*   `convert.py`: The main entry point and logic dispatcher.
*   `requirements.txt`: Python package dependencies.
*   `pyproject.toml`: Project metadata and build configuration.

### How to Contribute
1.  **Fork** the repository.
2.  **Clone** your fork locally.
3.  **Create a Branch** for your feature: `git checkout -b feature/amazing-new-format`.
4.  **Install** dependencies: `pip install -r requirements.txt`.
5.  **Implement** your changes.
    *   *Tip:* Check `convert.py` for the `get_converter` function to see how dispatching works.
    *   *Tip:* Add new logic functions (e.g., `convert_newtype`) and register them in the dispatcher.
6.  **Test** your changes with sample files.
7.  **Push** to your branch and open a **Pull Request**.

### Todo List
*   [ ] Add support for epub conversion.
*   [ ] Add a GUI interface.
*   [ ] Add unit tests for all conversion modules.

---

## 📜 License
[MIT](LICENSE)