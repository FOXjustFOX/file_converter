# 🔄 Universal File Converter

A powerful CLI tool to convert, compress, and enhance various file formats including images, videos, documents, and data files.  
It includes AI-powered text enhancement using Google Gemini and smart file size reduction.

## ✨ Features

- **Universal Conversion**: Supports Images, Videos, Documents, and Data files.
- **Smart Compression (`--reduce`)**: Optimize images and videos for smaller file sizes.
- **AI Enhancement (`--enhance`)**: Improve text quality in documents using Google Gemini.
- **Batch Processing**: Convert multiple files at once with a progress bar.
- **Simple CLI**: Easy-to-use command-line interface.

## 🛠️ Prerequisites

Before running the tool, ensure you have the following installed:

1.  **Python 3.8+**
2.  **FFmpeg** (Required for video conversion)
    - **Mac**: `brew install ffmpeg`
    - **Windows**: [Download FFmpeg](https://ffmpeg.org/download.html)
    - **Linux**: `sudo apt install ffmpeg`
3.  **Gemini API Key** (Optional, for AI enhancement)
    - Get your key from [Google AI Studio](https://aistudio.google.com/).
    - Set it as an environment variable:
      ```bash
      export GEMINI_API_KEY="your_api_key_here"
      ```
    - **Or create a `.env` file** in the project root:
      ```env
      GEMINI_API_KEY=your_api_key_here
      ```

## 📦 Installation

This tool is best installed using **pipx**, which installs it into an isolated environment and makes the `f` command available globally on your system.

### 1. Install pipx (if you haven't already)
- **Mac**: `brew install pipx`
- **Windows**: `scoop install pipx` (or `pip install pipx`)
- **Linux**: `sudo apt install pipx` (or `pip install --user pipx`)
- *Ensure pipx is in your path:* `pipx ensurepath`

### 2. Install using pipx
**Option A: Install directly from GitHub (Recommended)**
```bash
pipx install git+https://github.com/FOXjustFOX/file_converter.git
```
*This will download and install the latest version globally.*

**Option B: Install from source, so you can make changes**
If you have cloned the repository, navigate to the folder, change whatever youwant to change in pyproject.toml and run:
```bash
pipx install .
```

### 3. Verify Installation
Check if the command works:
```bash
f --help
```

### 4. Setup API Key (for AI features)
To use the AI enhancement features globally, add your API key to your shell configuration (e.g., `~/.zshrc` or `~/.bashrc`):
```bash
export GEMINI_API_KEY="your_api_key_here"
```
*Alternatively, the tool will also look for a `.env` file in the folder where you run the command.*

## 🚀 Usage

Basic syntax:
```bash
f <input_files> <output_destination> [flags]
```

### 1. Convert specific files to a folder
Convert image and doc to a specific output folder.
```bash
f image.png doc.docx ./output_folder
```

### 2. Convert a single file with target format
Convert markdown to HTML in the same directory.
```bash
f notes.md -t html
```

### 3. Compress / Reduce File Size
Optimize a video file.
```bash
f video.mov ./output -r
```

### 4. AI Text Enhancement
Convert and polish a document using Gemini AI.
```bash
f draft.docx final.md -e
```

## 📂 Supported Formats

| Category | Extensions |
| :--- | :--- |
| **Images** | `.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`, `.tiff` |
| **Videos** | `.mp4`, `.mkv`, `.mov`, `.avi`, `.webm` |
| **Documents** | `.docx`, `.pdf`, `.md`, `.html`, `.txt` |
| **Data** | `.csv`, `.json`, `.xlsx` |

## ❗ Troubleshooting

- **`command not found: f`**: Make sure you installed the package with `pipx install .` or use `python convert.py` directly.
- **`FFmpeg is not installed`**: Install FFmpeg for video support (see Prerequisites).
- **`GEMINI_API_KEY not found`**: Export your API key to use the `-e` flag.

## 📜 License
[MIT](LICENSE)
