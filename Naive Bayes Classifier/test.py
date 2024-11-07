import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
from nltk.corpus import movie_reviews
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy as nltk_accuracy
import nltk
nltk.download('movie_reviews')

def extract_features(words):
    return dict([(word, True) for word in words])

class SentimentAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Movie Review Sentiment Analyzer')
        self.setGeometry(100, 100, 400, 300)
        self.train_classifier()

        layout = QVBoxLayout()

        self.label = QLabel('Enter your movie review:')
        layout.addWidget(self.label)

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        self.button = QPushButton('Analyze Sentiment')
        self.button.clicked.connect(self.analyze_sentiment)
        layout.addWidget(self.button)

        self.result_label = QLabel('')
        layout.addWidget(self.result_label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


    def train_classifier(self):
        print("Training classifier...")
        fileids_pos = movie_reviews.fileids('pos')
        fileids_neg = movie_reviews.fileids('neg')
        features_pos = [(extract_features(movie_reviews.words(fileids=[f])), 'Positive') for f in fileids_pos]
        features_neg = [(extract_features(movie_reviews.words(fileids=[f])), 'Negative') for f in fileids_neg]
        threshold = 0.8
        num_pos = int(threshold * len(features_pos))
        num_neg = int(threshold * len(features_neg))
        features_train = features_pos[:num_pos] + features_neg[:num_neg]
        self.classifier = NaiveBayesClassifier.train(features_train)
        print("Training completed.")

    def analyze_sentiment(self):
        review = self.text_edit.toPlainText()
        words = review.split()
        features = extract_features(words)
        sentiment = self.classifier.classify(features)
        self.result_label.setText('Analyzed Sentiment: ' + sentiment)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SentimentAnalyzer()
    ex.show()
    sys.exit(app.exec_())
