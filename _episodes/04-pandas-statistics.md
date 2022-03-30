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

The full dataset is too large for this tutorial format. The subset used includes data from two hundred smart meters, recorded between December 19, 2015 and January 2, 2016. The full dataset includes data from 1825 meters and covers a timespan from July, 2013 through December, 2019. The two hundred meters used for the lesson subset were randomly selected. The date range was chosen because it includes the week before and after a major holiday followed by a blizzard. Coincidentally, date formatting problems with the meters that began in January 2016 also affect the data.

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

Next we create a loop to append the other files in the list to our dataframe. Since we have already read the first file into the dataframe, we will use index slicing to iterate on the file list beginning with the second item in the list.

~~~
for f in flist[1:]:
    df = df.append(pd.read_csv(f))

print(df.info())
~~~
{: .language-python}
~~~
<class 'pandas.core.frame.DataFrame'>
Int64Index: 273600 entries, 0 to 1439
Data columns (total 6 columns):
 #   Column         Non-Null Count   Dtype  
---  ------         --------------   -----  
 0   METER_FID      273600 non-null  object 
 1   START_READ     273600 non-null  float64
 2   END_READ       273600 non-null  float64
 3   INTERVAL_TIME  273600 non-null  object 
 4   INTERVAL_READ  273600 non-null  float64
 5   date           273600 non-null  object 
dtypes: float64(3), object(3)
memory usage: 14.6+ MB
~~~
{: .output}

The output of the ```info()``` method above indicates that three of the columns in the dataframe have numeric data types: "START\_READ", "END\_READ", and "INTERVAL\_READ". By default, Pandas will calculate descriptive statistics for numeric data types within a dataset.

~~~
print(df.describe())
~~~
{: .language-python}
~~~

	    START_READ 	    END_READ 	    INTERVAL_READ
count 	273600.000000 	273600.000000 	273600.000000
mean 	17144.337763 	17169.473211 	0.261822
std 	10304.468357 	10318.573027 	0.270579
min 	658.789000 	    661.687000 	    0.000000
25% 	9872.956000 	9882.920000 	0.090000
50% 	15800.545000 	15827.074000 	0.171600
75% 	22730.634000 	22752.376000 	0.336000
max 	52071.944000 	52158.061000 	3.232200
~~~
{: .output}

Since the values for "START\_READ" and "END\_READ" are calculated across two hundred different meters, those statistics may not be useful or of interest. Without grouping or otherwise manipulating the data, the only statistics that are interesting in the aggregate are for the "INTERVAL\_READ" variable. This is the variable that measures actual power consumption per time intervals of 15 minutes.

We can view the descriptive statistics for a single column:

~~~
print(df["INTERVAL_READ"].describe())
~~~
{: .language-python}
~~~
count    273600.000000
mean          0.261822
std           0.270579
min           0.000000
25%           0.090000
50%           0.171600
75%           0.336000
max           3.232200
Name: INTERVAL_READ, dtype: float64
~~~
{: .output}

We notice the maximum interval reading is way above the 75% range. For a closer inspection of high readings, we can also specify percentiles.

~~~
df["INTERVAL_READ"].describe(percentiles = [0.75, 0.85, 0.95, 0.99])
~~~
{: .language-python}
~~~
count    273600.000000
mean          0.261822
std           0.270579
min           0.000000
50%           0.171600
75%           0.336000
85%           0.477600
95%           0.837000
99%           1.272600
max           3.232200
Name: INTERVAL_READ, dtype: float64
~~~
{: .output}

There seem to be some meter readings that are unusually high. We will investgate this in more detail below.

First, let's look at descriptive statistics that Pandas provides for non-numeric data types. Even through these are excluded by default, they can still be calculated using the ```include="all"``` argument.

~~~
df.describe(include="all")
~~~
{: .language-python}
~~~
        METER_FID     START_READ       END_READ INTERVAL_TIME  INTERVAL_READ  \
count    273600.0  273600.000000  273600.000000        273600  273600.000000   
unique      189.0            NaN            NaN          1251            NaN   
top       10862.0            NaN            NaN     02-JAN-16            NaN   
freq       2880.0            NaN            NaN         18240            NaN   
mean          NaN   17144.337763   17169.473211           NaN       0.261822   
std           NaN   10304.468357   10318.573027           NaN       0.270579   
min           NaN     658.789000     661.687000           NaN       0.000000   
25%           NaN    9872.956000    9882.920000           NaN       0.090000   
50%           NaN   15800.545000   15827.074000           NaN       0.171600   
75%           NaN   22730.634000   22752.376000           NaN       0.336000   
max           NaN   52071.944000   52158.061000           NaN       3.232200   

              date  
count       273600  
unique          15  
top     2015-12-19  
freq         18240  
mean           NaN  
std            NaN  
min            NaN  
25%            NaN  
50%            NaN  
75%            NaN  
max            NaN  
~~~
{: .output}

Some statistics are excluded for non-numeric data types, but Pandas does provide information about the total number of observations, the number of uniquely occuring values, the most commonly occuring value, and the number of time the most commonly occuring value appears in the dataset.



{% include links.md %}
