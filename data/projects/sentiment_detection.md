# Project : SENTIMENT DETECTION

## Introduction
Date: July 25 2025 - break - August 5 2025

Data: We download the data with this command: wget http://cs.stanford.edu/people/alecmgo/trainingandtestdata.zip and then we decompressed it. This data contains 1,600,000 lines (text or tweet).

Description: In this project, we will build a model able to predict the feeling or sentiment expressed in a tweet( positif or negatif)

## Model used
LogisticRegression()
MultinomialNB()

## Conclusion
We can notice that the Logistic Regression model have a better score in every metric than the Naive Bayes one. Also despite some very bad scores in the cross validation, the models manage to predict correctly the target in the test.

This project helps to revise principally the task of cleaning the data for learning tasks. We also learn that having bad scores in cross validation doesn't mean everytimes having a bad model.