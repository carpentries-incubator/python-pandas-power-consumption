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

Since the values for "START\_READ" and "END\_READ" are calculated across two hundred different meters, those statistics may not be useful or of interest. Without grouping or otherwise manipulating the data, the only statistics that are interesting in the aggregate are for the "INTERVAL\_READ"


{% include links.md %}
