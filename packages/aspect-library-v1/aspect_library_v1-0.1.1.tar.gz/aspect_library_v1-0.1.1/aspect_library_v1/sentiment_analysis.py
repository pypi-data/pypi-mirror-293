import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from deep_translator import GoogleTranslator
import pandas as pd

nltk.download('punkt')
nltk.download('stopwords')

def clean_sentence(sentence):
    sentence = sentence.lower()
    words = word_tokenize(sentence)
    words = [word for word in words if word.isalnum()]
    stop_words = set(stopwords.words('english'))
    cleaned_words = [word for word in words if word not in stop_words]
    return ' '.join(cleaned_words)

def translate_aspects(df):
    translated_aspects = []
    sentiments = []
    
    for lis in df['aspect']:
        aspect_list = []
        for word in lis:
            cleaned_word = clean_sentence(word)
            translated_word = GoogleTranslator(source='en', target='fa').translate(cleaned_word)
            aspect_list.append(translated_word)
            translated_aspects.append(translated_word)
        df['aspects'].append(aspect_list)
    
    for lis in df['sentiment']:
        for word in lis:
            sentiments.append(word)
    
    return pd.DataFrame({'aspect': translated_aspects, 'sentiment': sentiments})

def create_pivot_table(aspect_df):
    pivot_table = aspect_df.pivot_table(index='aspect', columns='sentiment', aggfunc='size', fill_value=0)
    return pivot_table.reset_index()
