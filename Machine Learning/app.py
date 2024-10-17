from flask import Flask, request, jsonify
from google.cloud import speech
import os
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import nltk
import torch
import base64
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.data.path.append('/Users/saitejasriyerramsetti/nltk_data')
nltk.download('all')
app = Flask(__name__)

# Set up Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secret_key.json'

# Initialize Google Cloud Speech client
speech_client = speech.SpeechClient()

# Initialize NLP pipelines
# Enable GPU if available
device = 0 if torch.cuda.is_available() else -1
summarizer = pipeline("summarization", device=device)
sentiment_analyzer = pipeline("sentiment-analysis", device=device)

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Feedback Processing API!"}), 200

# Initialize categorization model
categories = ['Billing', 'Insurance', 'Hospital Maintenance', 'Doctor Consultation', 'Nursing Care']
vectorizer = TfidfVectorizer()
classifier = MultinomialNB()

# Sample training data (you should replace this with real data)
train_texts = [
    "I received great care in the Emergency Room today, with Dr Watt and Nurse Mike. After being thoroughly examined, I was admitted to the hospital. I was treated great by Nurse Renea and NA Julian. DOCTOR SHEN WAS GREAT AS WELL!!! On Monday, NA Caitlyn helped me with a shower. On Tuesday, NA Jasmyn also helped me with a shower. THE SHOWER IS ACTUALLY INSIDE THE ROOM!!! I think that's a great thing, every hospital room needs. I also want to compliment JUANITA, the Food Service Coordinator. She was very helpful in taking my food orders. I ate very good at SHARP MEMORIAL HOSPITAL!!!",
    
    "I went to the Emergency Room to get seen for my heart, and was admitted, but they didn't give me my REGULAR pain medication so had to leave before all of the tests were administered!!! NURSE JENN WAS SO UNCARING!!! DOCTOR MULLIN COULD NOT BE REACHED!!! Shame on SHARP MEMORIAL.",
    
    "I had an angioplasty under the care of Dr Justin Parizo and Dr Arvin P.S. Narula of the San Diego Cardiac Center. Although they thought that they might have to put in a stent, they did not. I WISHED THEY HAD PUT IN THE STENT GIVEN MY HISTORY OF STROKE AND 50% BLOCKAGE! Nevertheless, I do want to trust Dr Parizo. In regard to the procedure, I want to thank all of the nurses in the CATH LAB, who provided exceptional care. Even arranging to have my partner there at the exact time of discharge. I NEVER HAVE HAD A NURSE DO THAT BEFORE AT SHARP MEMORI It's just Dr Parizo refused to give clearance for a surgery saying that I had a 50% blockage, and needed an angioplasty and stent. I just don't understand what happened once I was on the table. In one instance it's needed, in another it's not. I do, however, want to thank Dr Parizo for taking an after hours call to answer questions about what to do with my Xarelto, Do I take it, or Do I wait to Take it a Day or Two. I REALLY APPRECIATED THE EXTRA CARE!!!",
    
    "I was treated for a severe, and necessary EMERGENCY SURGERY at the Sharp Memorial ER. I had been suffering from something for a year, but a surgery that was scheduled at the hospital was canceled due to a hospital mistake. I want to thank the ENTIRE EMERGENCY ROOM STAFF for helping me, from Dr Peter Venieris MD to the multiple nurses. I have to say that were very thorough from the start, reviewing my case, getting me a CT with contrast. It took way longer to get the CT than it should have, though, THREE HOURS!!! After getting the results, I was admitted to the hospital for treatment and possible surgery. I have a nice room in the hospital and I have a nice doctor. I have expressed my concerns, but he is working with me. I'm concerned that the surgery will not happen but I am hopeful it will."
]
train_labels = ['Billing', 'Insurance', 'Hospital Maintenance', 'Doctor Consultation']

# Train the categorization model
X_train = vectorizer.fit_transform(train_texts)
classifier.fit(X_train, train_labels)

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    audio_content = audio_file.read()
    
    # Encode audio content
    audio_content_base64 = base64.b64encode(audio_content).decode('utf-8')
    audio = speech.RecognitionAudio(content=audio_content_base64)
    
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,  # Set sample rate if known
        language_code="en-US",
    )

    response = speech_client.recognize(config=config, audio=audio)
    
    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript

    return jsonify({'transcript': transcript})

@app.route('/process_feedback', methods=['POST'])
def process_feedback():
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    # Summarization
    summary = summarizer(text, max_length=100, min_length=30, do_sample=False)[0]['summary_text']

    # Sentiment Analysis
    sentiment = sentiment_analyzer(text)[0]

    # Categorization
    category = classify_text(text)

    # Keyword Extraction
    keywords = extract_keywords(text)

    return jsonify({
        'summary': summary,
        'sentiment': sentiment,
        'category': category,
        'keywords': keywords
    })

def classify_text(text):
    X = vectorizer.transform([text])
    category = classifier.predict(X)[0]
    return category

def extract_keywords(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    keywords = [word for word in word_tokens if word.lower() not in stop_words and word.isalnum()]
    return keywords[:10]  # Return top 10 keywords

if __name__ == '__main__':
    app.run(debug=True)