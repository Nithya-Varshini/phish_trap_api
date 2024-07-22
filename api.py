from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from flask_cors import CORS
import joblib
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from googletrans import Translator
import re

app = Flask(__name__)

CORS(app)

# Load the data and the trained model
data = pd.read_csv('C:\\Users\\Setup\\Desktop\\hackathon\\chennai_haclkathon\\1.csv', encoding='latin')
data.rename(columns={'v1': 'Class', 'v2': 'Text'}, inplace=True)
data['numClass'] = data['Class'].map({'ham': 0, 'spam': 1})
data['Count'] = data['Text'].apply(len)

# Define stop words
stopset = set(stopwords.words("english"))

# Initialize CountVectorizer without stop words
vectorizer = CountVectorizer(stop_words=None, binary=True)
vectorizer.fit(data['Text'])

loaded_model = joblib.load('C:\\Users\\Setup\\Desktop\\hackathon\\chennai_haclkathon\\API\\saved_models\\stack.sav')

def translate_to_english(text):
    translator = Translator()
    translated_text = translator.translate(text, dest='en').text
    return translated_text

def extract_urls(text):
    # Regular expression pattern to match URLs
    url_pattern = r'https?://\S+|www\.\S+'
    
    # Find all URLs in the text
    urls = re.findall(url_pattern, text)
    for url in urls:
        text = text.replace(url, '')
    
    return urls


@app.route('/predict', methods=['POST'])
def predict():
    # Get the message from the request
    # message1 = "XXXMobileMovieClub: உங்கள் கிரெடிட்டைப் பயன்படுத்த, அடுத்த txt செய்தியில் உள்ள WAP இணைப்பைக் கிளிக் செய்யவும் அல்லது இங்கே கிளிக் செய்யவும்>> http://wap.xxxmobilemovieclub.com?n=QJKGIGHJJGCBL"
    message1 = str(request.json.get('message',''))
    print("Input message:", message1)
    message2=translate_to_english(message1)
    # Transform the message
    message_vectorized = vectorizer.transform([message2])
    # Predict whether the message is spam or legitimate
    prediction = loaded_model.predict(message_vectorized)
    # Return the prediction
    if prediction == 1:
        result = "1"
    else:
        result = "0"

    urls=extract_urls(message1)
    print("Extracted URLs:", urls)
    
    return jsonify({'translated_message': result, 'extracted_urls': urls})



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)
