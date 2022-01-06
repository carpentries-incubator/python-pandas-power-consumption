---
title: "Subsetting Dataframes with PANDAS"
teaching: 30
exercises: 15
questions:
- "How can we filter and subset data in Python?"
objectives:
- "Understand how Pandas indexes data."
- "Subset dataframes using index positions and filtering criteria."
keypoints:
- "..."
---

Pandas is designed to work with large datasets. Multiple indexing features allow for quick subsetting and filtering of data.

## Rows and columns

The axes of a dataframe are the rows and columns. Both rows and column labels are indexed when a dataframe is created, such as when reading a CSV file into memory. This allows for quick selection of specific rows, columns, or cells, either through slicing or subsetting a dataframe by filtering values according to specific criteria.

It's important to keep this terminology clear, because in addition to _indexing_ rows and column labels, Pandas creates an _index_ of row labels for every dataframe. This index can be specified when the dataframe is created, or alternatively Pandas will create an integer based index of row labels by default.

We can demonstrate this by reading a single file from our dataset. First, let's load the libraries we will use for this episode.

~~~
import pandas as pd
import glob
~~~
{: .language-python}

Next we use the ```glob()``` function to create a list of files. Then we read the first file in the list into a new dataframe. We will also use the ```info()``` function to look at the structure of our dataframe.

~~~
file_list = glob.glob("./lesson_data/*.csv")
df = pd.read_csv(file_list[0])
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
~~~
{: .ouput}

We can use the ```axes``` attribute to inspect the row and column indices. The output gives the row index first, and the column index second.

~~~
print(df.axes)
~~~
{: .language-python}
~~~
[RangeIndex(start=0, stop=1440, step=1), Index(['METER_FID', 'START_READ', 'END_READ', 'INTERVAL_TIME', 'INTERVAL_READ',
       'date'],
      dtype='object')]
~~~
{: .output}

The output above is a list, and the row index of our dataframe is the first object in the list:

~~~
RangeIndex(start=0, stop=1440, step=1)
~~~
{: .language-python}

This means that our rows are indexed or labeled using incremented integers, beginning with the first row labeled 0 and the last row labeled 1439. Recall that Python uses zero-indexing, so the ```stop``` value in the RangeIndex should be understood as "up to but not including 1440." We can confirm this by referring to the output of the ```info()``` function above, which states that the dataframe index has 1440 _entries_, labeled from 0 to 1439.

The second object in the list output by printing the dataframe's ```axes``` attribute is the column index. By default, the items in this index will be the column names, which can also be understood as the column axis labels.

~~~
Index(['METER_FID', 'START_READ', 'END_READ', 'INTERVAL_TIME', 'INTERVAL_READ',
       'date']
~~~
{: .language-python}

We can see the row labels using the ```head()``` function. Note that there is no column name for the row index. This is because there was no source column in our CSV file that the row labels refer to. We will update the attributes of the row index below.

~~~
df.head()
~~~
{: .language-python}
~~~
	METER_FID 	START_READ 	END_READ 	INTERVAL_TIME 	INTERVAL_READ 	date
0 	10063 	15685.143 	15704.015 	19-DEC-2015 00:00:00 	0.1596 	2015-12-19
1 	10063 	15704.015 	15726.103 	19-DEC-2015 00:15:00 	0.1782 	2015-12-19
2 	10063 	15704.015 	15726.103 	19-DEC-2015 00:30:00 	0.2172 	2015-12-19
3 	10063 	15704.015 	15726.103 	19-DEC-2015 00:45:00 	0.2256 	2015-12-19
4 	10063 	15704.015 	15726.103 	19-DEC-2015 01:00:00 	0.1512 	2015-12-19
~~~
{: .output}

## Selecting Specific Columns

If we want to select all of the values in a single column, we can use the column name.

~~~
df["date"]
~~~
{: .language-python}
~~~
0       2015-12-19
1       2015-12-19
2       2015-12-19
3       2015-12-19
4       2015-12-19
           ...    
1435    2016-01-02
1436    2016-01-02
1437    2016-01-02
1438    2016-01-02
1439    2016-01-02
Name: date, Length: 1440, dtype: object
~~~
{: .output}

In order to select multiple columns, we need to provide the column names as a list.

~~~
df[["METER_FID", "date"]]
~~~
{: .language-python}
~~~
	METER_FID 	date
0 	10063 	2015-12-19
1 	10063 	2015-12-19
2 	10063 	2015-12-19
3 	10063 	2015-12-19
4 	10063 	2015-12-19
... 	... 	...
1435 	10063 	2016-01-02
1436 	10063 	2016-01-02
1437 	10063 	2016-01-02
1438 	10063 	2016-01-02
1439 	10063 	2016-01-02

1440 rows × 2 columns
~~~
{: .output}

Note that all of our output includes row labels.

We can request attributes or perform operations on subsets.

~~~
df["date"].shape
~~~
{: .language-python}
~~~
(138240,)
~~~
{: .output}

~~~
df["INTERVAL_READ"].sum()
~~~
{: .language-python}
~~~
326.46720000000005
~~~
{: .output}

> ## Challenge: Find the Maximum Value of a Column
>
> In addition to getting the sum of values from a a specific column, Pandas has functions for generating other statistics. These include ```min()``` for the minimum value within a column and ```max()``` for the maximum value. 
> 
> Which of the below lines of code would give us the maximum values of both the "START\_READ" and "END\_READ" columns?
> ~~~
> A. print(df[START\_READ, END\_READ].max())
> B. print(df["START\_READ", "END\_READ"].max())
> C. print(df[[START\_READ, END\_READ]].max())
> D. print(df[["START\_READ", "END\_READ"]].max())
> ~~~
> {: .language-python}
>
> > ## Solution
> > ~~~
> > Option D prints out the maximum value of the columns.
> > ~~~
> > {: .output}
> {: .solution}
{: .challenge}

> ## Challenge: Perform Operations on Specific Data Types
>
> In addition to selecting columns by name, Pandas has a ```select\_dtypes()``` method that lets us select columns of a specific data type. 
> 
> Which of the options below will print out the sum of each column with a ```float``` data type?
> ~~~
> A. print(df.select\_dtypes(float).sum())
> B. print(df.select\_dtypes([["START_READ", "END\_READ", "INTERVAL\_READ"]]).sum())
> C. print(df[["START\_READ", "END\_READ", "INTERVAL\_READ"]].sum())
> D. print(df.sum(select\_dtypes(float))
> ~~~
> {: .language-python}
>
> > ## Solution
> > ~~~
> > Both A and C will output the correct result. However, option C requires us to already know that those columns have data of the correct data type. 
> > ~~~
> > {: .output}
> {: .solution}
{: .challenge}

{% include links.md %}
