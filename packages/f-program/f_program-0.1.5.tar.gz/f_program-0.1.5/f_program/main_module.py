# f_program/main_module.py

from sklearn.datasets import load_iris, fetch_20newsgroups
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn import metrics
import numpy as np
import os

def main_function():
    # Load Iris dataset
    iris = load_iris()
    X = iris.data
    y = iris.target

    # Split the Iris dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=1)

    # Initialize and train Gaussian Naive Bayes model
    gnb = GaussianNB()
    gnb.fit(X_train, y_train)

    # Make predictions and evaluate the model
    y_pred = gnb.predict(X_test)
    print("Gaussian Naive Bayes model accuracy(in %):", metrics.accuracy_score(y_test, y_pred) * 100)

    # Define cache directory
    cache_dir = os.path.join(os.path.expanduser('~'), 'f_program_data')

    # Ensure cache directory exists
    os.makedirs(cache_dir, exist_ok=True)

    try:
        # Load the 20 Newsgroups dataset with caching
        twenty_train = fetch_20newsgroups(subset='train', shuffle=True, download_if_missing=True, data_home=cache_dir)
    except Exception as e:
        print("Failed to download the 20 Newsgroups dataset. Please check your internet connection.")
        print(f"Error: {e}")
        return

    x = len(twenty_train.target_names)
    print("\nThe number of categories:", x)
    print("\nThe %d Different Categories of 20Newsgroups\n" % x)
    for i, cat in enumerate(twenty_train.target_names, start=1):
        print("Category[%d]:" % i, cat)

    print("\nLength of training data is", len(twenty_train.data))
    print("\nLength of file names is ", len(twenty_train.filenames))
    print("\nThe Content/Data of First File is:\n")
    print(twenty_train.data[0])
    print("\nThe Contents/Data of First 10 Files is in Training Data:\n")
    for i in range(10):
        print("\nFILE NO:%d\n" % (i + 1))
        print(twenty_train.data[i])

    # Filter and load specific categories
    categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']
    try:
        twenty_train_small = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42, data_home=cache_dir)
    except Exception as e:
        print("Failed to download the filtered 20 Newsgroups dataset. Please check your internet connection.")
        print(f"Error: {e}")
        return

    print("\nReduced Target Names:\n", twenty_train_small.target_names)
    print("\nReduced Target Length:\n", len(twenty_train_small.data))
    print("\nFirst Document:\n", twenty_train_small.data[0])

    # Convert text data to feature vectors
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(twenty_train_small.data)
    print("\n(Target Length , Distinct Words):", X_train_counts.shape)
    print("\nFrequency of the word 'algorithm':", count_vect.vocabulary_.get('algorithm'))

    # Transform counts to TF-IDF representation
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

    # Initialize and train Multinomial Naive Bayes model
    clf = MultinomialNB().fit(X_train_tfidf, twenty_train_small.target)

    # Make predictions on new documents
    docs_new = ['God is love', 'OpenGL on the GPU is fast']
    X_new_counts = count_vect.transform(docs_new)
    X_new_tfidf = tfidf_transformer.transform(X_new_counts)
    predicted = clf.predict(X_new_tfidf)
    for doc, category in zip(docs_new, predicted):
        print(f"'{doc}' => {twenty_train_small.target_names[category]}")

    # Create a pipeline for text classification
    text_clf = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', MultinomialNB()),
    ])

    # Train and evaluate the pipeline
    text_clf.fit(twenty_train_small.data, twenty_train_small.target)

    # Test the pipeline
    twenty_test = fetch_20newsgroups(subset='test', categories=categories, shuffle=True, random_state=42, data_home=cache_dir)
    docs_test = twenty_test.data
    predicted = text_clf.predict(docs_test)
    accuracy = np.mean(predicted == twenty_test.target) * 100
    print(f"\nPipeline Accuracy: {accuracy:.2f}%")

    # Print classification report and confusion matrix
    print("\nClassification Report:\n")
    print(metrics.classification_report(twenty_test.target, predicted, target_names=twenty_test.target_names))
    print("\nConfusion Matrix:\n")
    print(metrics.confusion_matrix(twenty_test.target, predicted))
