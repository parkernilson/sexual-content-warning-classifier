import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.model_selection import train_test_split


wnl = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

### Prelabeled Text Corpus
# Import from database
es_sentences = [
    "this is a   group. of sentences",
    "Each of them is 5a sentence from the given subreddit!",
    "here is another one1",
]

n_sentences = [
    "These ones are neutral sentences",
    "They are meant to be a case where the stuff is neutral"
]

### Pre-processing


def pre_process(phrase: str):
    lower_cased_phrase = phrase.lower()
    tokens = nltk.word_tokenize(lower_cased_phrase)
    # TODO: should I use spacy for lemmatization? Is lemmatization only lemmatizing nouns?
    tokens = [wnl.lemmatize(token) for token in tokens if token.isalpha()]
    tokens = [token for token in tokens if token not in stop_words]
    return tokens

processed_es_phrases = [" ".join(pre_process(phrase)) for phrase in es_sentences]
processed_n_phrases = [" ".join(pre_process(phrase)) for phrase in n_sentences]

vectorizer = TfidfVectorizer()
# TODO: am I doing this right?
X = vectorizer.fit_transform(processed_es_phrases + processed_n_phrases)
y = ['erotic_sexual' for _ in processed_es_phrases] \
    + ['neutral' for _ in processed_n_phrases]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = svm.SVC()
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)