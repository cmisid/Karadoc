import time

import numpy as np
import pandas as pd
from sklearn import model_selection
from sklearn import svm
from sklearn.feature_extraction.text import TfidfTransformer

from models import top_terms

# Datasets

tags = pd.read_csv('features/tags.csv', index_col=0)['tag_name']

# 1. Metadata TF
tf_metadata = pd.concat((
    pd.read_csv('features/metadata/tf_descriptions.csv', index_col=0),
    pd.read_csv('features/metadata/tf_keywords.csv', index_col=0)
), axis=1
)
tf_metadata = tf_metadata.groupby(tf_metadata.columns, axis=1).sum()  # Drop duplicate columns


# 2. Metadata TF-IDF
tfidf_metadata = pd.DataFrame(
    data=TfidfTransformer().fit_transform(tf_metadata).todense(),
    index=tf_metadata.index,
    columns=tf_metadata.columns
)

# Models


class Classifier():

    def __init__(self, name, dataframe, model):
        self.name = name
        self.dataframe = dataframe
        self.model = model


classifiers = [
    Classifier(
        name='Top terms on metadata TF',
        dataframe=tf_metadata,
        model=top_terms.TopTermsClassifier(n_terms=20)
    ),
    Classifier(
        name='Linear SVM on metadata TF-IDF',
        dataframe=tfidf_metadata,
        model=svm.LinearSVC(C=6.0, multi_class='crammer_singer')
    )
]

# Individual performance

splitter = model_selection.LeaveOneOut()

for clf in classifiers:
    X = clf.dataframe.values  # n-d array
    y = tags.reindex(clf.dataframe.index).values  # 1-d array
    y_pred = []
    y_true = []
    times = []
    for train, test in splitter.split(X):
        t0 = time.time()
        # Split into train/test (the test only has one observation in leave-one-out)
        X_train, X_test = X[train], X[test]
        y_train, y_test = y[train], y[test]
        # Fit on the training set and predicted the remaining test row
        clf.model.fit(X_train, y_train)
        y_pred.append(clf.model.predict(X_test))
        y_true.append(y_test)
        times.append(time.time() - t0)
    matches = np.array(y_true) == np.array(y_pred)
    total_time = sum(times)
    print('%s: %0.3f (+/- %0.3f) precision' % (clf.name, matches.mean(), matches.std()))
    print('Took %d seconds to evaluate (%0.2f per loop)' % (total_time, total_time / len(times)))
    print('-' * 42)

# Meta performance
