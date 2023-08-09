---
title: "Creating a Datetime Index with Pandas"
teaching: 40
exercises: 20
questions:
- "How can we visualize trends in time series?"
objectives:
- "Use pandas ```datetime``` indexing to subset time series data."
- "Resample and plot time series statistics."
- "Calculate and plot rolling averages."
keypoints:
- "Use ```resample()``` on a datetime index to calculate aggregate statistics across time series."
---

So far we have been interacting with the time series data in ways that are not very different from other tabular datasets. However, time series data can contain unique features that make it difficult to analyze aggregate statistics. For example, the sum of power consumption as measured by a single smart meter over the course of three years may be useful in a limited context, but if we want to analyze the data in order to make predictions about likely demand within one or more households at a given time, we need to account for time features including.

- **trends**
- **seasonality**

In this episode, we will use Pandas' datetime indexing features to illustrate these features.

### Setting a datetime index

To begin with we will demonstrate datetime indexing with data from a single meter. First, let's import the necessary libraries.

~~~
import pandas as pd
import matplotlib.pyplot as plt
import glob
import numpy as np
~~~
{: .language-python}

Create the file list as before, but this time read only the first file.

~~~
file_list = glob.glob("../data/*.csv")
data = pd.read_csv(file_list[0])
print(data.info())
~~~
{: .language-python}
~~~
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 105012 entries, 0 to 105011
Data columns (total 5 columns):
 #   Column         Non-Null Count   Dtype  
---  ------         --------------   -----  
 0   INTERVAL_TIME  105012 non-null  object 
 1   METER_FID      105012 non-null  int64  
 2   START_READ     105012 non-null  float64
 3   END_READ       105012 non-null  float64
 4   INTERVAL_READ  105012 non-null  float64
dtypes: float64(3), int64(1), object(1)
memory usage: 4.0+ MB
None
~~~
{: .output}

We can plot the *INTERVAL_READ* values without making any changes to the data. In the image below, we observe what may be trends or seasonality. But we are able to infer this based on our understanding of the data - note that the labels of the X index in the image are the row index positions, not date information.

~~~
data["INTERVAL_READ"].plot()
~~~
{: .language-python}

![Plot of three years of readings from a single smart meter.](../fig/datetime_indexing_1.png)

The plot is difficult to read because it is dense. Recall that meter readings are taken every 15 minutes, for a total in the case of this meter of 105,012 readings across the three years of data included in the dataset. In the plot above, we have asked Pandas to plot the value of each one of those readings - that's a lot of points!

In order to reduce the amount of information and inspect the data for trends and seasonality, the first thing we need to do is set the index of the dataframe to use the *INTERVAL_TIME* column as a datetime index. 

~~~
data.set_index(pd.to_datetime(data['INTERVAL_TIME']), inplace=True)
print(data.info())
~~~
{: .language-python}
~~~
<class 'pandas.core.frame.DataFrame'>
DatetimeIndex: 105012 entries, 2017-01-01 00:00:00 to 2019-12-31 23:45:00
Data columns (total 5 columns):
 #   Column         Non-Null Count   Dtype  
---  ------         --------------   -----  
 0   INTERVAL_TIME  105012 non-null  object 
 1   METER_FID      105012 non-null  int64  
 2   START_READ     105012 non-null  float64
 3   END_READ       105012 non-null  float64
 4   INTERVAL_READ  105012 non-null  float64
dtypes: float64(3), int64(1), object(1)
memory usage: 4.8+ MB
None
~~~
{: .output}

Note that the output of the ```info()``` function indicates the index is now a *DatetimeIndex.* However, the *INTERVAL_TIME* column is still listed as a column, with a data type of *object* or string.

~~~
print(data.head())
~~~
{: .language-python}
~~~
                           INTERVAL_TIME  METER_FID  START_READ   END_READ  \
INTERVAL_TIME                                                                
2017-01-01 00:00:00  2017-01-01 00:00:00        285   14951.787  14968.082   
2017-01-01 00:15:00  2017-01-01 00:15:00        285   14968.082  14979.831   
2017-01-01 00:30:00  2017-01-01 00:30:00        285   14968.082  14979.831   
2017-01-01 00:45:00  2017-01-01 00:45:00        285   14968.082  14979.831   
2017-01-01 01:00:00  2017-01-01 01:00:00        285   14968.082  14979.831   

                     INTERVAL_READ  
INTERVAL_TIME                       
2017-01-01 00:00:00         0.0744  
2017-01-01 00:15:00         0.0762  
2017-01-01 00:30:00         0.1050  
2017-01-01 00:45:00         0.0636  
2017-01-01 01:00:00         0.0870  
~~~
{: .output}

### Slicing data by date



{% include links.md %}
