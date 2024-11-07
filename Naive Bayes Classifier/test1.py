import streamlit as st
from nltk.corpus import movie_reviews
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy as nltk_accuracy
import nltk
nltk.download('movie_reviews')

def extract_features(words):
    return dict([(word, True) for word in words])

def train_classifier():
    st.write("Training classifier...")
    fileids_pos = movie_reviews.fileids('pos')
    fileids_neg = movie_reviews.fileids('neg')
    features_pos = [(extract_features(movie_reviews.words(fileids=[f])), 'Positive') for f in fileids_pos]
    features_neg = [(extract_features(movie_reviews.words(fileids=[f])), 'Negative') for f in fileids_neg]
    threshold = 0.8
    num_pos = int(threshold * len(features_pos))
    num_neg = int(threshold * len(features_neg))
    features_train = features_pos[:num_pos] + features_neg[:num_neg]
    classifier = NaiveBayesClassifier.train(features_train)
    st.write("Training completed.")
    return classifier

classifier = train_classifier()

def main():
    st.title('Movie Review Sentiment Analyzer')
    review = st.text_area('Enter your movie review:', height=150)
    if st.button('Analyze Sentiment'):
        words = review.split()
        features = extract_features(words)
        sentiment = classifier.classify(features)
        st.write('Analyzed Sentiment: ', sentiment)

if __name__ == '__main__':
    main()
