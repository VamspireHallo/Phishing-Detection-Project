import random
import mailbox
import email as eml
import pandas as pd
import re
import os
import pickle

from bs4 import BeautifulSoup

from webScraper import getFeatures

from sklearn.feature_extraction.text import TfidfVectorizer



def parse_html_text(html):
    # input needs to be  ---> .get_payload(decode=True).decode('latin-1')
    # cannot be str
    soup = BeautifulSoup(html, 'lxml')

    inline_tags = ['a', 'abbr', 'acronym', 'b', 'bdo', 'button', 'cite', 'code',
                   'dfn', 'em', 'i', 'kbd', 'label', 'output', 'q', 'samp', 'small',
                   'span', 'strong', 'sub', 'sup', 'time', 'var']
    tags = soup.find_all(inline_tags)
    for t in tags:
        t.unwrap()
    new_soup = BeautifulSoup(str(soup), 'lxml')
    text = new_soup.get_text('\n', strip=True)
    return text

def parse_html_url(html):
    # input needs to be  ---> part.get_payload(decode=True).decode('latin-1')
    # cannot be str
    soup = BeautifulSoup(html, 'lxml')
    urls = []
    tags = soup.find_all('a')
    for t in tags:
        if t.name == 'a':
            url = t.get('href')
            if url:
                urls.append(url)
    return urls

# def extract_text_from_html(html_content):
#     # input needs to be  ---> part.get_payload(decode=True).decode('latin-1')
#     # cannot be str
#     soup = BeautifulSoup(html_content, 'html.parser')
#     return soup.get_text()

def extract_email_content(message):
    try:
        text = ''
        urls = []
        if message.is_multipart():
            for part in message.walk():  # iterating through the message parts
                content_type = part.get_content_type()
                if content_type == 'text/html':
                    html_content = part.get_payload(decode=True).decode('latin-1')
                    text = parse_html_text(html_content)
                    urls = parse_html_url(html_content)
                elif content_type == 'text/plain':
                    text = part.get_payload(decode=True).decode('latin-1')
        return text, urls
    except UnicodeDecodeError:
        pass

def predict_url(urls, model, scaler):
    try:
        # Call web scraper and get features
        features = []
        for u in urls:
            features.append(getFeatures(u))
        features = pd.DataFrame(features)
        # Scale features
        features_scaled = scaler.transform(features)
        # Feed features into URL model
        url_model = model
        prediction = url_model.predict(features_scaled)

        return prediction
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


# Example usage:
# url_to_predict = "https://example.com"
# url_prediction = predict_url(url_to_predict)
#
# if url_prediction is not None:
#     print(f"Prediction for URL '{url_to_predict}': {url_prediction}")
# else:
#     print("Prediction failed.")

def vectorize_text(text, vectorizer):
    vectorized_text = vectorizer.transform([text])
    return vectorized_text


def predict_email(text, model, vectorizer):
    vectorized_text = []
    try:
        # Step 1: Vectorize the text
        vectorized_text = vectorize_text(text, vectorizer)
        # Step 2: Feed vectorized text into email model
        # Assuming you have an email model initialized somewhere in your code
        email_model = model
        prediction = email_model.predict(vectorized_text)

        return prediction
    except Exception as e:
        print(vectorized_text)
        print(f"An error occurred: {str(e)}")
        return None


# Example usage:
# email_content_to_predict = "This is an example email content."
# email_prediction = predict_email(email_content_to_predict)
#
# if email_prediction is not None:
#     print(f"Prediction for email content: {email_prediction}")
# else:
#     print("Prediction failed.")

