# Project : CUSTOMER CLASSIFICATION

## NOTE : one of my favorite project

## Introduction

Date: August 5 2025 - August 13 2025

Data: This Online Retail II data set contains all the transactions occurring for a UK-based and registered, non-store online retail between 01/12/2009 and 09/12/2011.The company mainly sells unique all-occasion gift-ware. Many customers of the company are wholesalers.

Description: In this project our goal will be to use this data to detect some similarities between the customers,to divide them in some groups with some particular habits or behaviors. This project could be very interresting for marketing strategies.

Remark: We could we use the data from the year 2009-2010 and after test our result and marketing strategies on the data from 2010-2011. But I have already start so let do it like this for the moment.

## KEY CONCEPT/ THINGS DONE DURING THE PROJECT
- Behavioral Variables (RFM)

This variables define the behavior of a customer in term of purchase. There are:

    R(Recency): numbers of days since the last command. More this value is low, more the customer is recent and potentially engaged the customer is.
    F(Frequency): total number of purchases the customer did in the period. This help to measure the faithfulness of the customer.
    M(Monetay): total amount spent by the customer in this period. show the financial value of this client for the company.

- Scoring

Now we will try to make the different groups using a scoring method.

Let's choose 5 groups and say that:

    for Recency: 1 = the oldest customers(with older purchase dates) , 5 = the regular people or the new ones
    for Frequency: 1 = the customer with lower number of purchase, 5 = our regular customers
    for Monetary: 1 = customers who spent less money , 5 = customer who spent much money

- ML Models

- Churn risk

It will consist into find the probability that a customer leave our company (maybe because of the quality of the service or because of our competitors).And to do that we will use the dataframe "recency" we already created. Like we say before, we will consider a customer almost lost if is recency (the number of day since is last purchase) is over 100.

However it is not totally interresting and true because maybe the customer buy many products at once for some period and will comeback after, so let take in this analysis people with recency above 100 and their monetary above an value. Because we don't want to lose time, energy or money(pubs,...) for people who just buy one time at a very low price and want to leave. In other words, we care about people who buy a lot and whant to leave for a reason we don't know. And for the value, we could take the average of a purchase in our dataset divided by 2. We will call it avg_price.

Of course, the way to define a customer who want ot leave could be changed or improved, but let work like that.


## Models used
KMeans

## Conclusion
Finally this project was very interresting because it helps us to discover many ways to make differences between customers, allows us to think on how we could do to keep them in company, push others to buy more,find and keep leaving customers,and most importanly to earn more income. And for technical aspect, I learn more about how to use panda.

We choose the task to make clusters among customers and do a churn risk, however we could have work on finding the product the most loved, or many other things.
