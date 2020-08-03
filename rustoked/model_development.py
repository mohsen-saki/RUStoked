import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import vstack, hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, plot_confusion_matrix

from pathlib import Path
import sys
sys.path.append("..")


def get_vectorizer(df):
    """
    Create a vectorizer and train it for further use.
    It should be fitted with training set preventing data leakage
    :param df: training data set
    :return: a fitted tfidf vectorizer instance
    """
    vectorizer = TfidfVectorizer(
        strip_accents='ascii', max_df=0.5, min_df=5, max_features=5000
    )
    
    vectorizer.fit(df['reviews'].copy())
    return vectorizer


def get_vectors_list(text_series, vectorizer):
    """
    Vectorise a series of texts and map it to a list
    :param text_series: a pandas series of texts
    :param vectorizer: a fitted instance of sklearn tfidf vectorizer
    :return: a list of vectors
    """
    vectors = vectorizer.transform(text_series)
    vectors_list = [vectors[i] for i in range(vectors.shape[0])]
    return vectors_list


def get_features_and_labels(df, feature_cols=None):
    """
    generate and return both sets of features and labels
    required for classifier model training and predictions
    :param df: a dataframe instance of training or testing set
    :param feature_cols: a list of columns name required to be included
                         and plugged into vectors of text features
    :return: features in form of sparse matrix and labels series
    """
    if not feature_cols:
        features = vstack(df['vectors'])
    else:
        text_features = vstack(df['vectors'])
        helping_features = df[feature_cols].astype(float)
        features = hstack([text_features, helping_features])
    labels = df['labels']
    return features, labels


def get_metrics(true_labels, predicted_labels):
    """
    print out evaluation metrics for the model
    :param true_labels: a series of true labels
    :param predicted labels: a series of predicted labels
    :return: print performance metrics including:
             precision, recall, f1-score, accuracy, macro & weighted averages
             
    Just as a reminder:
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1 = 2*(precision * recall) / (precision + recall)
    """
    print(classification_report(true_labels, predicted_labels))


def get_cm_plot(classifier, features, labels):
    """
    plot the confusion matrix for classifier
    :param classifier: the classifier model instance
    :param features: sparse matrix of features feeding the model
    :param labels: a series of true labels
    :return: plot the confusion matrix
    """
    classes = ['Dissatisfied', "Disengaged", 'Stoked']
    plot_confusion_matrix(classifier, features, labels,
                          cmap=plt.cm.Greys,
                          display_labels=classes)
    plt.title("Confusion Matrrix")


def get_feature_importance(vectorizer, classifier, feature_cols=None, num=20):
    """
    print out a certain number of Top & Bottom important features
    :param vectorizer: the fitted instance of tfidf vectorizer
    :param classifier: the classifier model
    :param feature_cols: a list of columns name required to be included
                         and plugged into vectors of text features
    :param num: The number of Top or Bottom important features to be printed
    :return: print a certain number of Top & Bottom important features
    """
    feature_names = vectorizer.get_feature_names()
    if not feature_cols:
        feature_names = np.array(feature_names)
    else:
        feature_names.extend(feature_cols)
        feature_names = np.array(feature_names)
    feature_importances = classifier.feature_importances_
    indices = np.argsort(feature_importances)[::-1]
    all_features = list(zip(feature_names[indices], feature_importances[indices]))
        
    print("{} most important features :\n".format(num))
    for feature in all_features[:num]:
        print("{}  :  {}".format(feature[0], feature[1]))
        
    print("\n{} less important features :\n".format(num))
    for feature in all_features[-num:]:
        print("{}  :  {}".format(feature[0], feature[1]))