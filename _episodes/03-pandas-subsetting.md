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
- "Rows can be selected in Pandas using label or position based indexing."
- "Boolean indexing and the ```query()``` method can be used to select subsets of a dataframe using conditions."
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
> A. print(df[START_READ, END_READ].max())
> B. print(df["START_READ", "END_READ"].max())
> C. print(df[[START_READ, END_READ]].max())
> D. print(df[["START_READ", "END_READ"]].max())
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
> A. print(df.select_dtypes(float).sum())
> B. print(df.select_dtypes([["START_READ", "END_READ", "INTERVAL_READ"]]).sum())
> C. print(df[["START_READ", "END_READ", "INTERVAL_READ"]].sum())
> D. print(df.sum(select_dtypes(float))
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

## Selecting Specific Rows

Subsets of rows of a Pandas dataframe can be selected different ways. The first two methods we'll look at, ```.loc``` and ```.iloc``` indexing, have some subtle differences that are worth exploring.

```.loc``` indexing will select rows with specific _labels_. Recall from earlier that when we read our CSV file into a dataframe, a row index was created which used integers as the label for each row. We can see information about the row index using the dataframe's ```index``` attribute.

~~~
print(df.index)
~~~
{: .language-python}
~~~
RangeIndex(start=0, stop=1440, step=1)
~~~
{: .output}

To select a specific row using ```.loc```, we need to know the label of the index. In this case, the labels start with 0 and go up to 1439, so if we want to select the first row we use the first index label. In this cast that is 0.

~~~
print(df.loc[0])
~~~
{: .language-python}
~~~
METER_FID                       10063
START_READ                  15685.143
END_READ                    15704.015
INTERVAL_TIME    19-DEC-2015 00:00:00
INTERVAL_READ                  0.1596
date                       2015-12-19
Name: 0, dtype: object
~~~
{: .output}

Note that above we said the label of the last row is 1439, even though the ```stop``` value of the index attribute is 1440. That is because default row indexing uses zero-indexing, which is common for Python data structures. The ```stop``` value given above should be understood as  _up to but not including_. We can demonstrate this by trying to use the label 1440 to select a row:

~~~
print("last row:")
print(df.loc[1439])
print("\nindex error:")
print(df.loc[1440])
~~~
{: .language-python}
~~~
last row:
METER_FID             10063
START_READ        16006.595
END_READ          16030.496
INTERVAL_TIME     02-JAN-16
INTERVAL_READ        0.1944
date             2016-01-02
Name: 1439, dtype: object

index error:

---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
C:\ProgramData\Anaconda3\lib\site-packages\pandas\core\indexes\range.py in get_loc(self, key, method, tolerance)
    384                 try:
--> 385                     return self._range.index(new_key)
    386                 except ValueError as err:

ValueError: 1440 is not in range
~~~
{: .output}

The error message in this case means that we tried to select a row using a label that is not in the index.

```iloc``` is used to select a row or subset of rows based on the integer position of row indexers. This method also uses zero-indexing, so integers will range from 0 to 1 less than the number of rows in the dataframe. The first row would have a position integer of 0, the second row would have a position integer of 1, etc.

~~~
print(df.iloc[0])
~~~
{: .language-python}
~~~
METER_FID                        1003
START_READ                  27326.181
END_READ                    27362.047
INTERVAL_TIME    19-DEC-2015 00:00:00
INTERVAL_READ                  0.3216
date                       2015-12-19
Name: 0, dtype: object
~~~
{: .output}

As above, we know there are 1440 rows in our dataset but zero-indexing means that the position integer of the last row is 1439. If we try to select a row using the position integer 1440, we get the same error as before.

~~~
print(df.iloc[1440])
~~~
{: .language-python}
~~~
IndexError: single positional indexer is out-of-bounds
~~~
{: .output}

We can also select rows using their position relative to the last row. If we want to select the last row without already knowing how many rows are in the dataframe, we can refer to its position using ```[-1]```.

~~~
print(df.iloc[-1])
~~~
{: .language-python}
~~~
METER_FID              1003
START_READ        27957.523
END_READ           27987.06
INTERVAL_TIME     02-JAN-16
INTERVAL_READ        0.4932
date             2016-01-02
Name: 1439, dtype: object
~~~
{: .output}

An alternative, more roundabout way is to use the ```len()``` function. Above, we noted that position integers will range from 0 to 1 less than the number of rows in the dataframe. In combination with the ```len()``` function, we can select the last row in a dataframe using:

~~~
print(df.iloc[len(df) - 1])
~~~
{: .language-python}
~~~
METER_FID              1003
START_READ        27957.523
END_READ           27987.06
INTERVAL_TIME     02-JAN-16
INTERVAL_READ        0.4932
date             2016-01-02
Name: 1439, dtype: object
~~~
{: .output}

> ## Challenge: Selecting Cells
>
> Given the lines of code below, put them in the correct order to read the data file *43_dec_2015.csv* and print the starting and ending meter readings.
> ~~~
> print(df.iloc[0]["START_READ"])
>
> df = pd.read_csv("43_dec_2015.csv")
>
> print(df.iloc[-1]["END_READ"])
> ~~~
> {: .language-python}
>
> > ## Solution
> > ~~~
> df = pd.read_csv("./lesson_data/43_dec_2015.csv")
> print(df.iloc[0]["START_READ"])
> print(df.iloc[-1]["END_READ"])
> > ~~~
> > {: .output}
> {: .solution}
{: .challenge}

## Slicing Data

So far we have used label and position based indexing to select single rows from a data frame. We can select larger subsets using index slicing. Because this is a common operation, we don't have to specify the index. 

~~~
print(df[1:10])
~~~
{: .language-python}
~~~
	METER_FID 	START_READ 	END_READ 	INTERVAL_TIME 	INTERVAL_READ 	date
1 	1003 	27362.047 	27419.506 	19-DEC-2015 00:15:00 	0.2856 	2015-12-19
2 	1003 	27362.047 	27419.506 	19-DEC-2015 00:30:00 	0.3252 	2015-12-19
3 	1003 	27362.047 	27419.506 	19-DEC-2015 00:45:00 	0.3054 	2015-12-19
4 	1003 	27362.047 	27419.506 	19-DEC-2015 01:00:00 	0.2934 	2015-12-19
5 	1003 	27362.047 	27419.506 	19-DEC-2015 01:15:00 	0.2742 	2015-12-19
6 	1003 	27362.047 	27419.506 	19-DEC-2015 01:30:00 	0.3300 	2015-12-19
7 	1003 	27362.047 	27419.506 	19-DEC-2015 01:45:00 	0.3078 	2015-12-19
8 	1003 	27362.047 	27419.506 	19-DEC-2015 02:00:00 	0.3258 	2015-12-19
9 	1003 	27362.047 	27419.506 	19-DEC-2015 02:15:00 	0.3216 	2015-12-19
~~~
{: .output}

When only a single colon is used in the square brackets, the integer on the left indicates the starting position. The integer on the right indicates the ending position, but here again note that the returned rows will be _up to but not including_ the row with the specified position. 

By default, all rows between the starting and ending position will be returned. We can also specify a number of rows to increment over, using a second colon followed by the interval of rows to use. For example, if we want to return every other row out of the first twenty rows in the dataset, we would use the following:

~~~
print(df[0:20:2])
~~~
{: .language-python}
~~~

	METER_FID 	START_READ 	END_READ 	INTERVAL_TIME 	INTERVAL_READ 	date
0 	1003 	27326.181 	27362.047 	19-DEC-2015 00:00:00 	0.3216 	2015-12-19
2 	1003 	27362.047 	27419.506 	19-DEC-2015 00:30:00 	0.3252 	2015-12-19
4 	1003 	27362.047 	27419.506 	19-DEC-2015 01:00:00 	0.2934 	2015-12-19
6 	1003 	27362.047 	27419.506 	19-DEC-2015 01:30:00 	0.3300 	2015-12-19
8 	1003 	27362.047 	27419.506 	19-DEC-2015 02:00:00 	0.3258 	2015-12-19
10 	1003 	27362.047 	27419.506 	19-DEC-2015 02:30:00 	0.2766 	2015-12-19
12 	1003 	27362.047 	27419.506 	19-DEC-2015 03:00:00 	0.2382 	2015-12-19
14 	1003 	27362.047 	27419.506 	19-DEC-2015 03:30:00 	0.2592 	2015-12-19
16 	1003 	27362.047 	27419.506 	19-DEC-2015 04:00:00 	0.3408 	2015-12-19
18 	1003 	27362.047 	27419.506 	19-DEC-2015 04:30:00 	0.3258 	2015-12-19
~~~
{: .output}

If we don't specify a starting or ending position, Python will default to the first and last positions, respectively. The following will output the first ten rows.

~~~
print(df[:10])
~~~
{: .language-python}
~~~
	METER_FID 	START_READ 	END_READ 	INTERVAL_TIME 	INTERVAL_READ 	date
0 	1003 	27326.181 	27362.047 	19-DEC-2015 00:00:00 	0.3216 	2015-12-19
1 	1003 	27362.047 	27419.506 	19-DEC-2015 00:15:00 	0.2856 	2015-12-19
2 	1003 	27362.047 	27419.506 	19-DEC-2015 00:30:00 	0.3252 	2015-12-19
3 	1003 	27362.047 	27419.506 	19-DEC-2015 00:45:00 	0.3054 	2015-12-19
4 	1003 	27362.047 	27419.506 	19-DEC-2015 01:00:00 	0.2934 	2015-12-19
5 	1003 	27362.047 	27419.506 	19-DEC-2015 01:15:00 	0.2742 	2015-12-19
6 	1003 	27362.047 	27419.506 	19-DEC-2015 01:30:00 	0.3300 	2015-12-19
7 	1003 	27362.047 	27419.506 	19-DEC-2015 01:45:00 	0.3078 	2015-12-19
8 	1003 	27362.047 	27419.506 	19-DEC-2015 02:00:00 	0.3258 	2015-12-19
9 	1003 	27362.047 	27419.506 	19-DEC-2015 02:15:00 	0.3216 	2015-12-19
~~~
{: .output}

We can use a negative position index to return the last ten rows.

~~~
print(df[-10:])
~~~
{: .language-python}
~~~
	METER_FID 	START_READ 	END_READ 	INTERVAL_TIME 	INTERVAL_READ 	date
1430 	1003 	27957.523 	27987.06 	02-JAN-16 	0.2586 	2016-01-02
1431 	1003 	27957.523 	27987.06 	02-JAN-16 	0.2778 	2016-01-02
1432 	1003 	27957.523 	27987.06 	02-JAN-16 	0.5970 	2016-01-02
1433 	1003 	27957.523 	27987.06 	02-JAN-16 	0.5448 	2016-01-02
1434 	1003 	27957.523 	27987.06 	02-JAN-16 	0.5202 	2016-01-02
1435 	1003 	27957.523 	27987.06 	02-JAN-16 	0.5070 	2016-01-02
1436 	1003 	27957.523 	27987.06 	02-JAN-16 	0.4896 	2016-01-02
1437 	1003 	27957.523 	27987.06 	02-JAN-16 	0.4908 	2016-01-02
1438 	1003 	27957.523 	27987.06 	02-JAN-16 	0.4872 	2016-01-02
1439 	1003 	27957.523 	27987.06 	02-JAN-16 	0.4932 	2016-01-02
~~~
{: .output}

This works the same with position based indexing. It can also work for label based indexing, depending on the labels used. 

~~~
print(df.iloc[2:12:2])
~~~
{: .language-python}
~~~
	METER_FID 	START_READ 	END_READ 	INTERVAL_TIME 	INTERVAL_READ 	date
2 	1003 	27362.047 	27419.506 	19-DEC-2015 00:30:00 	0.3252 	2015-12-19
4 	1003 	27362.047 	27419.506 	19-DEC-2015 01:00:00 	0.2934 	2015-12-19
6 	1003 	27362.047 	27419.506 	19-DEC-2015 01:30:00 	0.3300 	2015-12-19
8 	1003 	27362.047 	27419.506 	19-DEC-2015 02:00:00 	0.3258 	2015-12-19
10 	1003 	27362.047 	27419.506 	19-DEC-2015 02:30:00 	0.2766 	2015-12-19
~~~
{: .output}

~~~
print(df.loc[3:19:3])
~~~
{: .language-python}
~~~
 	METER_FID 	START_READ 	END_READ 	INTERVAL_TIME 	INTERVAL_READ 	date
3 	1003 	27362.047 	27419.506 	19-DEC-2015 00:45:00 	0.3054 	2015-12-19
6 	1003 	27362.047 	27419.506 	19-DEC-2015 01:30:00 	0.3300 	2015-12-19
9 	1003 	27362.047 	27419.506 	19-DEC-2015 02:15:00 	0.3216 	2015-12-19
12 	1003 	27362.047 	27419.506 	19-DEC-2015 03:00:00 	0.2382 	2015-12-19
15 	1003 	27362.047 	27419.506 	19-DEC-2015 03:45:00 	0.3348 	2015-12-19
18 	1003 	27362.047 	27419.506 	19-DEC-2015 04:30:00 	0.3258 	2015-12-19
~~~
{: .output}

We can select the values of single cells or column and row subsets by combining the methods used so far. First we specify the row index to use, then the column.

~~~
print(df.iloc[0]['INTERVAL_READ'])
~~~
{: .language-python}
~~~
0.3216
~~~
{: .output}

We can select multiple rows and/or columns. Note that selecting multiple columns requires us to put them into a list.

~~~
print(df.iloc[:10][['INTERVAL_READ', 'date']])
~~~
{: .language-python}
~~~
   INTERVAL_READ        date
0         0.3216  2015-12-19
1         0.2856  2015-12-19
2         0.3252  2015-12-19
3         0.3054  2015-12-19
4         0.2934  2015-12-19
5         0.2742  2015-12-19
6         0.3300  2015-12-19
7         0.3078  2015-12-19
8         0.3258  2015-12-19
9         0.3216  2015-12-19
~~~
{: .output}

We can also use position indexing to select columns, with the same slicing syntax as above.

~~~
print(df.iloc[1:10, 0:2])
~~~
{: .language-python}
~~~
   METER_FID  START_READ
1      10063   15704.015
2      10063   15704.015
3      10063   15704.015
4      10063   15704.015
5      10063   15704.015
6      10063   15704.015
7      10063   15704.015
8      10063   15704.015
9      10063   15704.015
~~~
{: .output}

> ## Challenge: Subsetting
>
> The frequency at which meter readings were taken means that a single day's worth of data consists of 96 rows. 
> Which of the following lines of code would we use to select daily start and ending meter readings, plus the date for each day?
> ~~~
> A. df.loc[::96][['START_READ', 'END_READ', 'date']]
> B. df.loc[0:1439:96]['START_READ', 'END_READ', 'date']
> C. df.loc[::96]['START_READ', 'END_READ', 'date']
> D. df.loc[:-1:96][['START_READ', 'END_READ', 'date']]
> ~~~
> {: .language-python}
>
> > ## Solution
> > ~~~
> > Option A returns the first row of the specified columns for each day.
> > ~~~
> > {: .output}
> {: .solution}
{: .challenge}

## Conditions

There are several ways to select subsets of a data frame using conditions to select rows based on the value of specific variables. One commonly used method is boolean indexing, which returns rows for which a given condition evaluates to _True_. The following example uses the ```head()``` method to test whether the values of the "INTERVAL_READ" variable are greater than 0.16.

~~~
print(df["INTERVAL_READ"] > 0.16)
~~~
{: .language-python}
~~~
0    False
1     True
2     True
3     True
4    False
Name: INTERVAL_READ, dtype: bool
~~~
{: .output}

Note that we have to include the condition to be evaluated as the indexer in order to see the rows for which the condition evaluates to _True_.

~~~
print(df[df["INTERVAL_READ"] > 0.16].head())
~~~
{: .language-python}
~~~
 	METER_FID 	START_READ 	END_READ 	INTERVAL_TIME 	INTERVAL_READ 	date
1 	10063 	15704.015 	15726.103 	19-DEC-2015 00:15:00 	0.1782 	2015-12-19
2 	10063 	15704.015 	15726.103 	19-DEC-2015 00:30:00 	0.2172 	2015-12-19
3 	10063 	15704.015 	15726.103 	19-DEC-2015 00:45:00 	0.2256 	2015-12-19
5 	10063 	15704.015 	15726.103 	19-DEC-2015 01:15:00 	0.1716 	2015-12-19
6 	10063 	15704.015 	15726.103 	19-DEC-2015 01:30:00 	0.2370 	2015-12-19
~~~
{: .output}

The column used for the condition does not have to be included in the subset. Selecting rows in this case requires the use of label based indexing.

~~~
print(df.loc[df["date"] == "2015-12-26", ["INTERVAL_TIME", "INTERVAL_READ"]])
~~~
{: .language-python}
~~~
            INTERVAL_TIME  INTERVAL_READ
672  26-DEC-2015 00:00:00         0.1758
673  26-DEC-2015 00:15:00         0.1752
674  26-DEC-2015 00:30:00         0.1506
675  26-DEC-2015 00:45:00         0.1632
676  26-DEC-2015 01:00:00         0.1830
..                    ...            ...
763  26-DEC-2015 22:45:00         0.2046
764  26-DEC-2015 23:00:00         0.1374
765  26-DEC-2015 23:15:00         0.1908
766  26-DEC-2015 23:30:00         0.2292
767  26-DEC-2015 23:45:00         0.1944

[96 rows x 2 columns]

~~~
{: .output}

It is possible to specify multiple conditions.

~~~
print(df[(df["INTERVAL_READ"] > 0.16) & (df["date"] == "2015-12-25")].head())
~~~
{: .language-python}
~~~
	METER_FID 	START_READ 	END_READ 	INTERVAL_TIME 	INTERVAL_READ 	date
577 	10063 	15827.074 	15850.986 	25-DEC-2015 00:15:00 	0.1662 	2015-12-25
578 	10063 	15827.074 	15850.986 	25-DEC-2015 00:30:00 	0.2280 	2015-12-25
579 	10063 	15827.074 	15850.986 	25-DEC-2015 00:45:00 	0.1668 	2015-12-25
581 	10063 	15827.074 	15850.986 	25-DEC-2015 01:15:00 	0.2112 	2015-12-25
582 	10063 	15827.074 	15850.986 	25-DEC-2015 01:30:00 	0.2460 	2015-12-25
~~~
{: .output}

The ```query()``` method provides similar functionality with a simplified syntax. Using the ```query()``` method, the above example becomes:

~~~
print(df.query('INTERVAL_READ > 0.16 and date == "2015-12-25"').head())
~~~
{: .language-python}
~~~
	METER_FID 	START_READ 	END_READ 	INTERVAL_TIME 	INTERVAL_READ 	date
577 	10063 	15827.074 	15850.986 	25-DEC-2015 00:15:00 	0.1662 	2015-12-25
578 	10063 	15827.074 	15850.986 	25-DEC-2015 00:30:00 	0.2280 	2015-12-25
579 	10063 	15827.074 	15850.986 	25-DEC-2015 00:45:00 	0.1668 	2015-12-25
581 	10063 	15827.074 	15850.986 	25-DEC-2015 01:15:00 	0.2112 	2015-12-25
582 	10063 	15827.074 	15850.986 	25-DEC-2015 01:30:00 	0.2460 	2015-12-25
~~~
{: .output}

Note in this case that the conditions are passed as a string to the query. This requires us to pay close attention to consistent use of single and double quotes.

We can also select specific columns when using the ```query()``` method.

~~~
print(df.query('INTERVAL_READ > 0.16 and date == "2015-12-25"')[["INTERVAL_READ","date"]].head())
~~~
{: .language-python}
~~~
	INTERVAL_READ 	date
577 	0.1662 	2015-12-25
578 	0.2280 	2015-12-25
579 	0.1668 	2015-12-25
581 	0.2112 	2015-12-25
582 	0.2460 	2015-12-25
~~~
{: .output}

> ## Challenge: Select Intervals with Above Average Power Consumption
>
> The dataset used for this lesson is a subset of a much larger dataset measuring power consumption within homes in Los Alamos, New Mexico. Part of the reason for chosing the date range
> of the subset is because there was a record-setting blizzard in the state on December 26 and 27, 2015. In later episodes in this lesson we will dig more deeply into the blizzard's
> effect on power consumption and resulting errors or anomalies in the data, but using what we know already we can select a subset of the data to identify times of above average 
> power consumption.
>
> Fill in the blanks below to select the "INTERVAL_TIME", "INTERVAL_READ", and date for all rows for which the value of the "INTERVAL_READ" variable is above the average value for 
> that variable in the entire dataset.
> 
> ~~~
> df.___[df["_________"] ___ df["INTERVAL_READ"].mean(), ["___________", "___________", "date"]]
> ~~~
> {: .language-python}
>
> > ## Solution
> > ~~~
> > df.loc[df["INTERVAL_READ"] > df["INTERVAL_READ"].mean(), ["INTERVAL_TIME", "INTERVAL_READ", "date"]]
> > ~~~
> > {: .output}
> {: .solution}
{: .challenge}

{% include links.md %}
