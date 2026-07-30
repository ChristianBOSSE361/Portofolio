# Project : HOUSE PREDICTION

## Introdution
Date: July 7 2025

Data: The data used in that project came from an American census of 1990. We could find them in the modul datasets from sklearn, then we use the function fetch_california_housing to download the data.

Description: The goal of this project is to build some models able to predict the house's prices.

## Model used
LinearRegression()
DecisionTreeRegressor()
KNeighborsRegressor()
SVR(kernel='rbf')
RandomForestRegressor()

# INterpretation
We can see here that the different models are not really good. Indeed,

    The SVR model (whith the default parameters) :

    Have one of the biggest error rate among the models chosen in this project and his 'r2 score' is negatif, that's means that it is worst than a model which just predict the average. His rate errors is around 1.10 that means that if the price of the house in the dataset were divided by 100,000 , we have an average difference of $110,000 between the prediction and the real value of the house, that is too much. That model is obviously not good enough with that parameters. Maybe we have to change the value of some parameters( as C, gamma,...) to have a better model. And according to ChatGPT, the SVM is not the first choice when we want to do regression like here.

    The K-nearest neighbor(with default neigbors equals 5):

    Have also a big error rate. We have around 1.0 that means we will have a difference of $100.000 from the real value of the price, which is not acceptable. Also we have a 'r2 score' very close to 0 because it's around 0.1, we can say that this model is almost useless like the fisrt one it is just a little bit better than just taking the average.

    The Logistic regressor:

    Have a high rate error rate even if it is lower than the first 2 models. We will have with this model a difference of 70,000 from the real prices, and this is still not acceptable. However, the 'r2 score' is a bit close to 1, this model with predict almost corretly the deviation in our data.

    The Decison Tree regressor:

    Still have a high a error rate like the logistic regressor model. We will have a deviation of almost 70,000 from the real prices. Concerning the 'r2 score', it is amoung the best we have here like the previous one, it will be able to predict nearly correctly the deviation in our data.

We are going to test a new model based on many decision tree (because it was one of the best model among those tested): The random forest.

Let's see what we can have.

## Conclusion
Finally we can say that maybe the models used in that project are not very suitable for the regression (unsupervised learning) or the problem came from the dataset itself.

According to ChatGPT the 3 best models for a regression are :

    Gradient Bosting
    Random Forest Regressor (we use it and it was our best model amoung those used)
    Lasso Regressor

We'll be using them in another project.