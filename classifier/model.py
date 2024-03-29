import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

from ..data.db import DB

wnl = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

nlp = spacy.load("en_core_web_sm")

sexual_sentences = None
neutral_sentences = None

with DB() as cursor:
    cursor.execute("SELECT selftext FROM reddit_posts WHERE type = 'sexual'")
    sexual_sentences = cursor.fetchall()
    cursor.execute("SELECT selftext FROM reddit_posts WHERE type != 'sexual'")
    neutral_sentences = cursor.fetchall()

if sexual_sentences is None or neutral_sentences is None:
    raise Exception("Failed to fetch data from database")

def pre_process(phrase: str):
    doc = nlp(phrase.lower())
    tokens = [token.lemma_ for token in doc if token.is_alpha]
    tokens = [token for token in tokens if token not in stop_words]
    return tokens

processed_sexual_phrases = [" ".join(pre_process(phrase)) for phrase in sexual_sentences]
processed_neutral_phrases = [" ".join(pre_process(phrase)) for phrase in neutral_sentences]

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', svm.SVC()),
])

parameters = {
    'tfidf__max_df': (0.5, 0.75, 1.0),
    'clf__C': (0.1, 1, 10),
}

grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1)

y = [1] * len(sexual_sentences) + [0] * len(neutral_sentences)
grid_search.fit(processed_sexual_phrases + processed_neutral_phrases, y)

y_pred = grid_search.predict(processed_sexual_phrases + processed_neutral_phrases)