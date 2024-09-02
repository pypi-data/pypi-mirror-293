from sklearn.datasets import load_iris, fetch_20newsgroups
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn import metrics
import numpy as np

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

    # Load the 20 Newsgroups dataset
    twenty_train = fetch_20newsgroups(subset='train', shuffle=True)
    x = len(twenty_train.target_names)
    print("\n The number of categories:", x)
    print("\n The %d Different Categories of 20Newsgroups\n" % x)
    for i, cat in enumerate(twenty_train.target_names, start=1):
        print("Category[%d]:" % i, cat)

    print("\n Length of training data is", len(twenty_train.data))
    print("\n Length of file names is ", len(twenty_train.filenames))
    print("\n The Content/Data of First File is :\n")
    print(twenty_train.data[0])
    print("\n The Contents/Data of First 10 Files is in Training Data :\n")
    for i in range(10):
        print("\n FILE NO:%d \n" % (i + 1))
        print(twenty_train.data[i])

    # Filter and load specific categories
    categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']
    twenty_train = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42)

    print("\n Reduced Target Names:\n", twenty_train.target_names)
    print("\n Reduced Target Length:\n", len(twenty_train.data))
    print("\nFirst Document : ", twenty_train.data[0])

    # Convert text data to feature vectors
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(twenty_train.data)
    print("\n(Target Length , Distinct Words):", X_train_counts.shape)
    print("\n Frequency of the word algorithm:", count_vect.vocabulary_.get('algorithm'))

    # Transform counts to TF-IDF representation
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

    # Initialize and train Multinomial Naive Bayes model
    clf = MultinomialNB().fit(X_train_tfidf, twenty_train.target)

    # Make predictions on new documents
    docs_new = ['God is love', 'OpenGL on the GPU is fast']
    X_new_counts = count_vect.transform(docs_new)
    X_new_tfidf = tfidf_transformer.transform(X_new_counts)
    predicted = clf.predict(X_new_tfidf)
    for doc, category in zip(docs_new, predicted):
        print('%r => %s' % (doc, twenty_train.target_names[category]))

    # Create a pipeline for text classification
    text_clf = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', MultinomialNB()),
    ])

    # Train and evaluate the pipeline
    text_clf.fit(twenty_train.data, twenty_train.target)

    # Test the pipeline
    twenty_test = fetch_20newsgroups(subset='test', categories=categories, shuffle=True, random_state=42)
    docs_test = twenty_test.data
    predicted = text_clf.predict(docs_test)
    print("Pipeline Accuracy:", np.mean(predicted == twenty_test.target))

    # Print classification report and confusion matrix
    print(metrics.classification_report(twenty_test.target, predicted, target_names=twenty_test.target_names))
    print(metrics.confusion_matrix(twenty_test.target, predicted))
