---
title: "Summarizing Tabular Data with PANDAS"
teaching: 30
exercises: 15
questions:
- "How can we summarize large datasets?"
objectives:
- "Summarize large datasets using descriptive statistics."
- "Perform operations to identify outliers and missing values in tabular data."
keypoints:
- "Use the PANDAS `describe()` method to generate descriptive statistics for a dataframe."
---

Metadata provided with the published Los Alamos Public Utility Department Smart Meter dataset at Dryad <https://doi.org/10.5061/dryad.m0cfxpp2c> indicates that aside from de-identification the data have not been pre-processed or normalized and may include missing data, duplicate entries. 

The full dataset is too large for this tutorial format. The subset used includes data from two hundred smart meters, recorded between December 19, 2015 and January 2, 2016. The full dataset includes data from 1825 meters and covers a timespan from July, 2013 through December, 2019. The two hundred meters used for the lesson subset were randomly selected. The date range was chosen because it includes the week before and after a major US holiday followed by a blizzard. Coincidentally, date formatting problems with the meters that began in January 2016 also affect the data.

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
    df = df.append(pd.read_csv(f), ignore_index=True)

print(df.info())
~~~
{: .language-python}
~~~
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 273600 entries, 0 to 273599
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
memory usage: 12.5+ MB
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

Some statistics are excluded for non-numeric data types, but Pandas does provide information about the total number of observations, the number of uniquely occuring values, the most commonly occuring value, and the number of time the most commonly occurring value appears in the dataset.

Already we see some potential problems with the data. First, our most frequently occurring "INTERVAL\_TIME" value, 02-JAN-16, is not in the format we expect. It is lacking a timestamp, and it appears that at least 18,240 values in this column are affected. Also, the output of the ```df.info()``` function after reading in the first file in the list indicates that data for a single meter should consist of 1440 rows, yet the most frequently occurring "METER\_FID" value of 10862 occurs twice that many times. This means there is potentially some duplication in the dataset. Finally, although our file list consisted of 200 files, there are only 189 unique values for "METER\_FID." This may also point to some duplication.


### Checking for Null Values

Before proceeding, let's check for missing data. Missing data in pandas are represented using ```NaN```, or "not a number."

~~~
print(pd.isna(df))
~~~
{: .language-python}
~~~
      METER_FID  START_READ  END_READ  INTERVAL_TIME  INTERVAL_READ   date
0         False       False     False          False          False  False
1         False       False     False          False          False  False
2         False       False     False          False          False  False
3         False       False     False          False          False  False
4         False       False     False          False          False  False
...         ...         ...       ...            ...            ...    ...
1435      False       False     False          False          False  False
1436      False       False     False          False          False  False
1437      False       False     False          False          False  False
1438      False       False     False          False          False  False
1439      False       False     False          False          False  False

[276480 rows x 6 columns]
~~~
{: .output}

A quick inspection doesn't show any missing data in the first or last five rows. What we really want is to find rows with missing data or NaN values, and we can look for null values within columns as well as rows.

To search for NaN values across all rows within a dataframe, we use the row axis.

~~~
row_na = df[df.isna().any(axis=1)].copy()
row_na
~~~
{: .language-python}
~~~
Empty DataFrame
Columns: [METER_FID, START_READ, END_READ, INTERVAL_TIME, INTERVAL_READ, date]
Index: []
~~~
{: .output}

The operation above returns an empty dataframe, indicating that there are now missing values in the dataset. But we can also check by column.

~~~
meter_fid_na = df[df["METER_FID"].isna()].copy()
print(meter_fid_na)
~~~
{: .language-python}
~~~
Empty DataFrame
Columns: [METER_FID, START_READ, END_READ, INTERVAL_TIME, INTERVAL_READ, date]
Index: []
~~~
{: .output}

As expected, this operation also returns an empty dataframe. 

### Working with Values

Returning to our descriptive statistics, we have already noted that the maximum value is well above the 99th percentile. Our minimum value of zero may also be unusual, since many homes might be expected to use some amount of energy every fifteen minutes, even when residents are away. 

~~~
df["INTERVAL_READ"].describe()
~~~
{: .language-python}
~~~
count    276480.000000
mean          0.262069
std           0.270478
min           0.000000
25%           0.090600
50%           0.171600
75%           0.336000
max           3.232200
Name: INTERVAL_READ, dtype: float64
~~~
{: .output}

As we have seen, we can select the minimum and maximum values in a column using the ```min()``` and ```max()``` functions.

~~~
print("Minimum value:", df["INTERVAL_READ"].min())
print("Maximum value:", df["INTERVAL_READ"].max())
~~~
{: .language-python}
~~~
Minimum value: 0.0
Maximum value: 3.2322
~~~
{: .output}

This is useful if we want to know what those values are. We may want to have more information about the corresponding meter's start and end reading, the date, and the meter ID. One way to discover this information is to use the ```idxmin()``` and ```idxmax()``` functions to get the position indices of the rows where the minimum and maximum values occur.

~~~
print("Position index of the minimum value:", df["INTERVAL_READ"].idxmin())
print("Position index of the maximum value:", df["INTERVAL_READ"].idxmax())
~~~
{: .language-python}
~~~
Position index of the minimum value: 2883
Position index of the maximum value: 86815
~~~
{: .output}

Now we can use the position index to select the row with the reported minimum value.

~~~
print(df.iloc[2883])
~~~
{: .language-python}
~~~
METER_FID                       10274
START_READ                    1616.99
END_READ                       1619.7
INTERVAL_TIME    19-DEC-2015 00:45:00
INTERVAL_READ                       0
date                       2015-12-19
Name: 2883, dtype: object
~~~
{: .output}

We can do the same with the maximum value.

~~~
print(df.iloc[86815])
~~~
{: .language-python}
~~~
METER_FID                       22918
START_READ                    23541.6
END_READ                      23603.1
INTERVAL_TIME    23-DEC-2015 07:45:00
INTERVAL_READ                  3.2322
date                       2015-12-23
Name: 86815, dtype: object
~~~
{: .output}

Notice that in both cases, the ```idxmin()``` and ```idxmax()``` functions return a single position index number, when in fact the minimum and maximum values may occur multiple times. We can use the ```value_counts()``` function to demonstrate that 0 occurs thousands of times in the dataset.

~~~
print(pd.value_counts(df["INTERVAL_READ"]))
~~~
{: .language-python}
~~~
0.0000    6346
0.1488    1087
0.1482     918
0.0012     903
0.0060     765
          ... 
1.8162       1
1.7976       1
2.1366       1
1.5072       1
1.7850       1
Name: INTERVAL_READ, Length: 3293, dtype: int64
~~~
{: .output}

To find the number of rows with "INTERVAL\_READ" values equal to a specific value, we can also create a subset of rows with that value and then get the length of the subset.

~~~
print("Number of rows with minimum interval read values:", len(df[df["INTERVAL_READ"] == 0]))
print("Number of rows with maximum interval read values:", len(df[df["INTERVAL_READ"] == 3.2322]))
~~~
{: .language-python}
~~~
Number of rows with minimum interval read values: 6346
Number of rows with maximum interval read values: 1
~~~
{: .output}

{% include links.md %}
