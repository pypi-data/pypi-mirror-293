from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def train_and_evaluate_text_classifier():
    # Load 20 Newsgroups dataset
    newsgroups = fetch_20newsgroups(subset='all')
    X, y = newsgroups.data, newsgroups.target
    
    # Vectorize text data
    vectorizer = CountVectorizer()
    X_vectorized = vectorizer.fit_transform(X)
    
    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.3, random_state=42)
    
    # Train model
    model = MultinomialNB()
    model.fit(X_train, y_train)
    
    # Predict
    y_pred = model.predict(X_test)
    
    # Calculate accuracy and generate reports
    accuracy = accuracy_score(y_test, y_pred) * 100
    report = classification_report(y_test, y_pred, target_names=newsgroups.target_names)
    conf_matrix = confusion_matrix(y_test, y_pred)
    
    # Example new documents for prediction
    new_docs = ["This is a new document about machine learning.", 
                "Political news and current events are discussed here."]
    new_docs_vectorized = vectorizer.transform(new_docs)
    new_docs_predictions = model.predict(new_docs_vectorized)
    
    new_docs_results = [(doc, newsgroups.target_names[pred]) for doc, pred in zip(new_docs, new_docs_predictions)]
    
    return new_docs_results, accuracy, report, conf_matrix
