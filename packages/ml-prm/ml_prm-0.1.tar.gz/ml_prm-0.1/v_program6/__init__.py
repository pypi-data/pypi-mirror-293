from sklearn.datasets import load_iris, fetch_20newsgroups
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn import metrics

def naive_bayes_iris():
    data = load_iris()
    X = data.data
    y = data.target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = GaussianNB()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    accuracy = metrics.accuracy_score(y_test, y_pred)
    return accuracy

def naive_bayes_newsgroups():
    data = fetch_20newsgroups(subset='all')
    X = data.data
    y = data.target

    # Convert text data to numeric using TF-IDF
    from sklearn.feature_extraction.text import TfidfVectorizer
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = MultinomialNB()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    accuracy = metrics.accuracy_score(y_test, y_pred)
    return accuracy
