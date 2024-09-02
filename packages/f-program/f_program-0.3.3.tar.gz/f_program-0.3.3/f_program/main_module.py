# f_program/main_module.py

def generate_output():
    from sklearn.datasets import load_iris
    iris = load_iris()
    X = iris.data
    y = iris.target
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=1)
    from sklearn.naive_bayes import GaussianNB
    gnb = GaussianNB()
    gnb.fit(X_train, y_train)
    from sklearn import metrics
    print("Gaussian Naive Bayes model accuracy(in %):", metrics.accuracy_score(y_test, gnb.predict(X_test)) * 100)
    
    from sklearn.datasets import fetch_20newsgroups
    twenty_train = fetch_20newsgroups(subset='train', shuffle=True)
    x = len(twenty_train.target_names)
    print("\nThe number of categories:", x)
    print("\n%d Different Categories of 20Newsgroups\n" % x)
    for i, cat in enumerate(twenty_train.target_names, 1):
        print("Category[%d]:" % i, cat)
    print("\nLength of training data is", len(twenty_train.data))
    print("\nLength of file names is ", len(twenty_train.filenames))
    print("\nThe Content/Data of First File is :\n", twenty_train.data[0])
    print("\nThe Contents/Data of First 10 Files in Training Data :\n")
    for i in range(10):
        print("\nFILE NO:%d \n" % (i + 1))
        print(twenty_train.data[i])
    categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']
    twenty_train = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42)
    print("\nReduced Target Names:\n", twenty_train.target_names)
    print("\nReduced Target Length:\n", len(twenty_train.data))
    print("\nFirst Document : ", twenty_train.data[0])
    
    from sklearn.feature_extraction.text import CountVectorizer
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(twenty_train.data)
    print("\n(Target Length, Distinct Words):", X_train_counts.shape)
    print("\nFrequency of the word 'algorithm':", count_vect.vocabulary_.get('algorithm'))
    
    from sklearn.feature_extraction.text import TfidfTransformer
    tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
    X_train_tf = tf_transformer.transform(X_train_counts)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    print("\nX_train_tfidf shape:", X_train_tfidf.shape)
    
    from sklearn.naive_bayes import MultinomialNB
    clf = MultinomialNB().fit(X_train_tfidf, twenty_train.target)
    docs_new = ['God is love', 'OpenGL on the GPU is fast']
    X_new_counts = count_vect.transform(docs_new)
    X_new_tfidf = tfidf_transformer.transform(X_new_counts)
    predicted = clf.predict(X_new_tfidf)
    for doc, category in zip(docs_new, predicted):
        print('%r => %s' % (doc, twenty_train.target_names[category]))
    
    from sklearn.pipeline import Pipeline
    text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB())])
    text_clf.fit(twenty_train.data, twenty_train.target)
    
    import numpy as np
    twenty_test = fetch_20newsgroups(subset='test', categories=categories, shuffle=True, random_state=42)
    docs_test = twenty_test.data
    predicted = text_clf.predict(docs_test)
    print(metrics.classification_report(twenty_test.target, predicted, target_names=twenty_test.target_names))
    print(metrics.confusion_matrix(twenty_test.target, predicted))
