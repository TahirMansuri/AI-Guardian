# AI Guardian — Windows Setup Guide

Here is the complete, step-by-step guide to set up AI Guardian on a Windows machine.

## 🐍 Step 1: Install Python and Create a Virtual Environment
You need Python to run the backend.

1. **Download Python**: Go to the official Python website ([python.org](https://python.org/)) and download the latest Windows installer (64-bit). Run the installer and **check the box "Add Python to PATH"** on the first screen.
2. **Verify Installation**: Open Command Prompt or PowerShell and type:
   ```cmd
   python --version
   ```
3. **Create a Project Folder**: Navigate to where you want the project, then create a virtual environment:
   ```cmd
   mkdir AI-Guardian
   cd AI-Guardian
   python -m venv .venv
   ```
4. **Activate the Virtual Environment**: In Windows, the activation command is different:
   ```cmd
   .venv\Scripts\activate
   ```
   You should see `(.venv)` at the start of your command line.

## 🧠 Step 2: Install and Run the LLM Runtime (Choose One)
You need a local LLM to analyze the text. Windows users have two main options: Ollama (easier) or `llama.cpp`.

### Option A: Ollama (Recommended for Windows)
Ollama is the simplest way to get a local model running on Windows.
1. **Install Ollama**: Go to [ollama.com/download](https://ollama.com/download), download the Windows `.exe`, and run it. It installs and starts a background service automatically.
2. **Download a Model**: Open a terminal and pull the Qwen model (or a Llama model). You can use a smaller model for faster performance on Windows.
   ```cmd
   ollama pull qwen2.5:7b
   ```
3. **Note the API Endpoint**: Ollama runs on `http://localhost:11434`. You will need this for the backend configuration.

### Option B: llama.cpp
If you want to use the exact same GGUF model files as on Mac, you can install `llama.cpp` on Windows via WinGet.
1. **Install via WinGet**: Open PowerShell as Administrator and run:
   ```powershell
   winget install llama.cpp
   ```
2. **Download the GGUF Model**: You need to download the `.gguf` file (e.g., `Qwen2.5-7B-Instruct-Q4_K_M.gguf`) from Hugging Face to a local folder, for example, `C:\Models\`.
3. **Run the Server**: Open a terminal and run:
   ```cmd
   llama-server -m "C:\Models\Qwen2.5-7B-Instruct-Q4_K_M.gguf" -ngl 20 --port 11434
   ```
   *(Note: `-ngl 20` tries to offload layers to your GPU if you have one; adjust based on your VRAM).*

## 📦 Step 3: Install Python Dependencies
With your virtual environment still active, you need to install the project's Python packages. You will also need some system-level tools for the screenshot/APK analysis features.

1. **Install Python Packages**:
   ```cmd
   pip install -r requirements.txt
   ```
   *(If you don't have the file yet, the key packages are: `fastapi, uvicorn, requests, pydantic, python-multipart, python-whois, pytesseract, pillow, pyzbar, opencv-python-headless, androguard, openai, google-generativeai, python-dotenv`)*

2. **Install Tesseract OCR (for Screenshot Analysis)**:
   - Download the Windows installer from the UB-Mannheim repository (the official Tesseract GitHub points here).
   - Run the installer. Crucially, on the "Select Additional Tasks" screen, check **"Add Tesseract to system PATH"**.
   - After installation, restart your terminal. Verify by typing `tesseract --version`.

3. **Install Visual C++ Redistributable (for QR Code/pyzbar)**:
   - The `pyzbar` library on Windows requires the Visual C++ Redistributable for Visual Studio 2013.
   - Download and install `vcredist_x64.exe` from the official Microsoft link. This prevents common `ImportError: DLL load failed` errors.

## ⚙️ Step 4: Configure the Project Paths
The code from the Mac setup may have hardcoded file paths. You must update them for Windows.

1. **Update `llm_providers/local_provider.py`**:
   - If you use Ollama, the URL should be `http://localhost:11434/v1/chat/completions` and the model name should be just `qwen2.5:7b` (or whatever you pulled).
   - If you use `llama.cpp`, the URL is the same, but the `MODEL_NAME` variable must point to your Windows file path, e.g., `C:\\Models\\Qwen2.5-7B-Instruct-Q4_K_M.gguf`.

2. **Update `security/screenshot_analyzer.py` (for Tesseract)**:
   Add this line at the top of the file to tell Python where Tesseract is installed (if it's not detected in PATH automatically):
   ```python
   import pytesseract
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

## 🚀 Step 5: Run the AI Guardian Application
You are now ready to start the backend server (which also serves the frontend).

1. Ensure your virtual environment is active (`.venv\Scripts\activate`).
2. Start the FastAPI Backend:
   ```cmd
   uvicorn main:app --host 127.0.0.1 --port 8000
   ```
3. **Access the GUI**: Open your web browser and go to `http://127.0.0.1:8000`.

---

## ✅ Summary Checklist

| Task | Windows Command / Action |
|---|---|
| **Create Env** | `python -m venv .venv` |
| **Activate Env** | `.venv\Scripts\activate` |
| **Install Python Deps** | `pip install -r requirements.txt` |
| **Install LLM** | `winget install llama.cpp` OR use Ollama installer |
| **System Tools** | Install Tesseract (add to PATH) + VC++ 2013 Redistributable |
| **Run Server** | `uvicorn main:app --host 127.0.0.1 --port 8000` |
| **Access GUI** | `http://127.0.0.1:8000` |
