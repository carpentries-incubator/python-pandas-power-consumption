---
title: "Introduction"
teaching: 15
exercises: 10
questions:
- "What are common use cases for timeseries analysis?"
objectives:
- "Read and plot timeseries data using Python Pandas."
- "Group data and generate descriptive statistics."
- "Resample timeseries data using datetime indexing in Pandas."
keypoints:
- "Pandas is a Python library that operates efficiently against large datasets."
- "Datetime indexing with Pandas enables resampling of timeseries data using different time steps."
---

## Introducing time series

We regularly encounter time series data in our daily lives. Examples are abundant and include stock prices, daily rates of infection during the COVID-19 pandemic, gas and electricity use as described in our utility bills, and data points from our fitness tracking devices. Any type of observation for which data are collected at specific intervals can be represented as a time series.

Time series data may be analyzed for multiple purposes, including

- Identifying trends.
- Making forecasts.
- Fraud and anomaly detection.

This series of lessons is intended as an introduction to key concepts in the analysis and visualization of time series data. Additional lessons in this series will introduce concepts and methods for making forecasts and classifying time series for different purposes.

> ## Challenge: Time series in our daily lives
>
> Above, we provided examples of information that is best represented using
> time series, for example daily prices of stocks.
>
> What are some other examples of information that is collected consecutively
> or at specific intervals? Think of an example and reflect on the following
> questions:
>
> - Are observations recorded at specific times?
> - Are observations recorded at regular intervals?
> - What types of trends would you expect to see in the data?
> 
{: .challenge}

## Time series analysis using Python

Several Python libraries have been developed which can be used to support analysis of trends, forecasting, and classification of time series data. A non-exhaustive list of libraries includes:

- ```pandas()```
- ```statistics()```
- ```scikitlearn()```
- ```tensorflow()```

This lesson is focused on Pandas, which provides many useful features for inspecting large datasets, as well as resampling time series data to quickly calculate and plot statistics and moving averages.

{% include links.md %}
