# Project : IRIS CLASSIFICAATION

## Introduction

- Date: July 7 2025

- Data: We will use here the iris data from the fetch_ucirepo (id = 53) function come from the ucimlrepo module.

- Description: In this first machine learning projet, we will try to build a model able to predict the type of a flower amoung all the type we have in instance Setosa, Versicolor or Virginica regarding some features.

## Model used
DecisionTreeClassifier()
LogisticRegression()
KNeighborsClassifier(n_neighbors=3)
SVC(kernel='linear')
SVC(kernel='rbf')

## Conclusion
Finaly we don't see here any differences between the different models. Maybe the dataset is too short to help us to see a difference between all this models and algorithms.

We also notice that the SVM methods, with kernel='linear' and kernel='rbf', have the same perfect result, the 'linear' manage to fit with this kind of data that means the different classes are linearly separable and we did even need the 'rbf' one.

Next time we will work on a bigger dataset.