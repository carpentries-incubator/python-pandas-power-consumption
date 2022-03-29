---
title: "Summarizing Tabular Data with PANDAS"
teaching: 30
exercises: 15
questions:
- "How can we summarize large datasets?"
objectives:
- "Summarize large datasets using descriptive statistics."
- "Perform operations to identify outliers and missing values in tabular data."
- "Visualize data with plots."
- "Need an objective about grouping."
keypoints:
- "Use the PANDAS `describe()` method to generate descriptive statistics for a dataframe."
---

Metadata provided with the published Los Alamos Public Utility Department Smart Meter dataset at Dryad <https://doi.org/10.5061/dryad.m0cfxpp2c> indicates that aside from de-identification the data have not been pre-processed or normalized and may include missing data, duplicate entries. 

The full dataset is too large for this tutorial format. The subset used includes data from two hundred smart meters, recorded between December 19, 2015 and January 2, 2016. The full dataset includes ... [this info should go in the setup, too]. The two hundred meters used for the lesson subset were randomly selected. The date range was chosen because it includes the week before and after a major holiday that coincided with a blizzard. 

For this lesson we will use Pandas functions to normalize the data subset.

## Descriptive Statistics

Descriptive statistics provide us with a means to summarize large datasets, and to identify the presence of outliers, missing data, etc.

First, import Pandas and the ```glob``` library, which provides utilities for generating lists of files that match specific file name patterns.

~~~
import pandas as pd
import glob
~~~
{: .language-python}

Next, use the ```glob``` function to create a list of files that Pandas will combine into a single data frame.

~~~
flist = glob.glob("./lesson_data/*.csv")
print(flist[:5])
~~~
{: .language-python}
~~~
['./lesson_data\\10063_dec_2015.csv',
 './lesson_data\\10270_dec_2015.csv',
 './lesson_data\\10274_dec_2015.csv',
 './lesson_data\\10373_dec_2015.csv',
 './lesson_data\\10577_dec_2015.csv']
~~~
{: .output}

Use index slicing to read the first file into a dataframe and inspect it.

~~~
df = pd.read_csv(flist[0])
print(df.axes)
~~~
{: .language-python}
~~~
[RangeIndex(start=0, stop=1440, step=1),
 Index(['METER_FID', 'START_READ', 'END_READ', 'INTERVAL_TIME', 'INTERVAL_READ',
        'date'],
       dtype='object')]
~~~
{: .output}

~~~
print(df.info())
~~~
{: .language-python}
~~~
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 1440 entries, 0 to 1439
Data columns (total 6 columns):
 #   Column         Non-Null Count  Dtype  
---  ------         --------------  -----  
 0   METER_FID      1440 non-null   int64  
 1   START_READ     1440 non-null   float64
 2   END_READ       1440 non-null   float64
 3   INTERVAL_TIME  1440 non-null   object 
 4   INTERVAL_READ  1440 non-null   float64
 5   date           1440 non-null   object 
dtypes: float64(3), int64(1), object(2)
memory usage: 67.6+ KB
None
~~~
{: .output}

Note that the *date* field in the dataset is not in the original raw data, but was added as pre-processing for this tutorial using a process described in a previous episode.



{% include links.md %}
