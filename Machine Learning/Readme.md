

# Feedback Processing API

## Overview
This API processes audio feedback and provides text analysis, including transcription, summarization, sentiment analysis, categorization, and keyword extraction. Built using Flask, it utilizes Google Cloud Speech-to-Text for audio processing and various NLP models for text analysis.

## Prerequisites
Before running this application, ensure you have the following installed:

- Python 3.7 or higher
- pip (Python package installer)
- Google Cloud account (with a Speech-to-Text API key)

## Getting Started

### 1. Clone the Repository
Clone this repository to your local machine using:
```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

### 2. Set Up a Virtual Environment
Create and activate a virtual environment:
```bash
# For macOS/Linux
python3 -m venv env
source env/bin/activate

# For Windows
python -m venv env
.\env\Scripts\activate
```

### 3. Install Required Packages
Install the necessary packages using `pip`:
```bash
pip install -r requirements.txt
```

### 4. Set Up Google Cloud Credentials
Create a service account in Google Cloud with access to the Speech-to-Text API and download the credentials JSON file. Save the file as `secret_key.json` in the root of your project directory.

Set the environment variable for Google Cloud credentials:
```bash
export GOOGLE_APPLICATION_CREDENTIALS='secret_key.json'
```
For Windows, use:
```bash
set GOOGLE_APPLICATION_CREDENTIALS=secret_key.json
```

### 5. Run the Application
Start the Flask application:
```bash
python app.py
```
The API will be accessible at `http://127.0.0.1:5000/`.

### 6. API Endpoints
- **Home**: 
  - `GET /` - Returns a welcome message.
  
- **Transcribe Audio**:
  - `POST /transcribe` - Expects an audio file. Returns the transcribed text.

- **Process Feedback**:
  - `POST /process_feedback` - Expects a JSON body with a text field. Returns the summarized text, sentiment analysis, category, and keywords.


### 7. Stop the Application
To stop the Flask server, you can press `Ctrl + C` in the terminal where the server is running.

## Troubleshooting
- Make sure all required packages are installed.
- Ensure that your Google Cloud credentials are set up correctly.
- If you encounter any errors, check the console for error messages.

## Contributing
Feel free to contribute to the project by creating a branch and submitting a pull request with your changes.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```

### Instructions to Use
- Replace `https://github.com/yourusername/your-repo-name.git` with the actual URL of your repository.
- Adjust any specific instructions or details to better fit your project structure or additional features you may have.
- Ensure that all your teammates are informed about the setup process so that they can get everything running smoothly.

Let me know if you need any modifications or additional sections!