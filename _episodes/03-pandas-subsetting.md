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

Next we use the ```glob()``` function to create a list of files. Then we use the same process as before to read all of the files into a single large dataframe. We will also use the ```info()``` function to look at the structure of our dataframe.

~~~
file_list = glob.glob("../data/*.csv")
data = pd.concat([pd.read_csv(f) for f in file_list])
print(data.info())
~~~
{: .language-python}
~~~
<class 'pandas.core.frame.DataFrame'>
Int64Index: 1575180 entries, 0 to 105011
Data columns (total 5 columns):
 #   Column         Non-Null Count    Dtype  
---  ------         --------------    -----  
 0   INTERVAL_TIME  1575180 non-null  object 
 1   METER_FID      1575180 non-null  int64  
 2   START_READ     1575180 non-null  float64
 3   END_READ       1575180 non-null  float64
 4   INTERVAL_READ  1575180 non-null  float64
dtypes: float64(3), int64(1), object(1)
memory usage: 72.1+ MB
None
~~~
{: .ouput}

We can use the ```axes``` attribute to inspect the row and column indices. The output gives the row index first, and the column index second.

~~~
print(data.axes)
~~~
{: .language-python}
~~~
[Int64Index([     0,      1,      2,      3,      4,      5,      6,      7,
                 8,      9,
            ...
            105002, 105003, 105004, 105005, 105006, 105007, 105008, 105009,
            105010, 105011],
           dtype='int64', length=1575180), Index(['INTERVAL_TIME', 'METER_FID', 'START_READ', 'END_READ',
       'INTERVAL_READ'],
      dtype='object')]
~~~
{: .output}

The output above is a list, and the row index of our dataframe is the first object in the list:

~~~
[Int64Index([     0,      1,      2,      3,      4,      5,      6,      7,
                 8,      9,
            ...
            105002, 105003, 105004, 105005, 105006, 105007, 105008, 105009,
            105010, 105011],
           dtype='int64', length=1575180), Index(['INTERVAL_TIME', 'METER_FID', 'START_READ', 'END_READ',
       'INTERVAL_READ'],
      dtype='object')]
~~~
{: .language-python}

This indicates that our rows are indexed or labeled using incremented integers, beginning with the first row labeled 0 and the last row labeled 1439. Recall that Python uses zero-indexing, so the final value in the index should be understood as "up to but not including 105011." 

The final row index number may be surprising. The output of the ```info()``` function above indicates that our dataframe has 1,575,180 rows. But here the last row has an index number of 105011. Why is this?

When we created our dataframe, we did so by reading all of the files in our file list and concatenating them into a single dataframe. Each file was first read into its own dataframe before concatenation, which means that each of the 15 dataframe had its own row index beginning with 0 and stopping at whatever the last row index would be for that dataframe. When dataframes are concatenated, original row index numbers are preserved by default. Because of this, many thousands of row index numbers would have been common across datasets, resulting in duplicate row index numbers in the concatenated dataframe. 

To make the most efficient use of Pandas in this case, we can reset the index of the dataframe. After resetting the index, we will check the ```axes``` attribute again.

~~~
data.reset_index(inplace=True, drop=True)
print(data.axes)
~~~
{: .language-python}

~~~
[RangeIndex(start=0, stop=1575180, step=1), Index(['index', 'INTERVAL_TIME', 'METER_FID', 'START_READ', 'END_READ',
       'INTERVAL_READ'],
      dtype='object')]
~~~
{: .output}

Note that this time the index is identified as a *RangeIndex*, rather than the *Int64index* that was output before. Instead of listing every integer index number, the range is given. This means that our rows are indexed or labeled using incremented integers, beginning with the first row labeled 0 and the last row labeled 1575810. Recall that Python uses zero-indexing, so the stop value in the RangeIndex should be understood as “up to but not including 1575180.” We can confirm this by referring to the output of the info() function above, which states that the dataframe index has 1575180 entries, labeled from 0 to 1575179.

The second object in the list output by printing the dataframe's ```axes``` attribute is the column index. By default, the items in this index will be the column names, which can also be understood as the column axis labels.

~~~
Index(['INTERVAL_TIME', 'METER_FID', 'START_READ', 'END_READ',
       'INTERVAL_READ']
~~~
{: .language-python}

We can see the row labels using the ```head()``` function. Note that there is no column name for the row index. This is because there was no source column in our CSV file that the row labels refer to. We will update the attributes of the row index below.

~~~
print(data.head())
~~~
{: .language-python}
~~~
         INTERVAL_TIME  METER_FID  START_READ   END_READ  INTERVAL_READ
0  2017-01-01 00:00:00        285   14951.787  14968.082         0.0744
1  2017-01-01 00:15:00        285   14968.082  14979.831         0.0762
2  2017-01-01 00:30:00        285   14968.082  14979.831         0.1050
3  2017-01-01 00:45:00        285   14968.082  14979.831         0.0636
4  2017-01-01 01:00:00        285   14968.082  14979.831         0.0870

~~~
{: .output}

## Selecting Specific Columns

If we want to select all of the values in a single column, we can use the column name.

~~~
print(data["INTERVAL_TIME"])
~~~
{: .language-python}
~~~
0          2017-01-01 00:00:00
1          2017-01-01 00:15:00
2          2017-01-01 00:30:00
3          2017-01-01 00:45:00
4          2017-01-01 01:00:00
                  ...         
1575175    2019-12-31 22:45:00
1575176    2019-12-31 23:00:00
1575177    2019-12-31 23:15:00
1575178    2019-12-31 23:30:00
1575179    2019-12-31 23:45:00
Name: INTERVAL_TIME, Length: 1575180, dtype: object

~~~
{: .output}

In order to select multiple columns, we need to provide the column names as a list.

~~~
print(data[["METER_FID", "INTERVAL_TIME"]])
~~~
{: .language-python}
~~~
         METER_FID        INTERVAL_TIME
0              285  2017-01-01 00:00:00
1              285  2017-01-01 00:15:00
2              285  2017-01-01 00:30:00
3              285  2017-01-01 00:45:00
4              285  2017-01-01 01:00:00
...            ...                  ...
1575175       8078  2019-12-31 22:45:00
1575176       8078  2019-12-31 23:00:00
1575177       8078  2019-12-31 23:15:00
1575178       8078  2019-12-31 23:30:00
1575179       8078  2019-12-31 23:45:00
~~~
{: .output}

Note that all of our output includes row labels.

We can request attributes or perform operations on subsets.

~~~
print(data["INTERVAL_TIME"].shape)
~~~
{: .language-python}
~~~
(1575180,)
~~~
{: .output}

~~~
print(data["INTERVAL_READ"].sum())
~~~
{: .language-python}
~~~
365877.39449999994
~~~
{: .output}

> ## Challenge: Find the Maximum Value of a Column
>
> In addition to getting the sum of values from a a specific column, Pandas has functions for generating other statistics. These include ```min()``` for the minimum value within a column and ```max()``` for the maximum value. 
> 
> Which of the below lines of code would give us the maximum values of both the "START\_READ" and "END\_READ" columns?
> ~~~
> A. print(data[START_READ, END_READ].max())
> B. print(data["START_READ", "END_READ"].max())
> C. print(data[[START_READ, END_READ]].max())
> D. print(data[["START_READ", "END_READ"]].max())
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
> A. print(data.select_dtypes(float).sum())
> B. print(data.select_dtypes([["START_READ", "END_READ", "INTERVAL_READ"]]).sum())
> C. print(data[["START_READ", "END_READ", "INTERVAL_READ"]].sum())
> D. print(data.sum(select_dtypes(float))
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
print(data.index)
~~~
{: .language-python}
~~~
RangeIndex(start=0, stop=1575180, step=1)
~~~
{: .output}

To select a specific row using ```.loc```, we need to know the label of the index. In this case, the labels start with 0 and go up to 1575810, so if we want to select the first row we use the first index label. In this cast that is 0.

~~~
print(data.loc[0])
~~~
{: .language-python}
~~~
INTERVAL_TIME    2017-01-01 00:00:00
METER_FID                        285
START_READ                 14951.787
END_READ                   14968.082
INTERVAL_READ                 0.0744
Name: 0, dtype: object
~~~
{: .output}

Note that above we said the label of the last row is 1575179, even though the ```stop``` value of the index attribute is 1575180. That is because default row indexing uses zero-indexing, which is common for Python data structures. The ```stop``` value given above should be understood as  _up to but not including_. We can demonstrate this by trying to use the label 1575180 to select a row:

~~~
print("Index error:")
print(data.loc[1575180])
~~~
{: .language-python}
~~~
Index error:

---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
File C:\ProgramData\Anaconda3\lib\site-packages\pandas\core\indexes\range.py:391, in RangeIndex.get_loc(self, key, method, tolerance)
    390 try:
--> 391     return self._range.index(new_key)
    392 except ValueError as err:

ValueError: 1575180 is not in range
~~~
{: .output}

The error message in this case means that we tried to select a row using a label that is not in the index.

To print the actual last row, we provide a row index number that is one less than the ```stop``` value:

~~~
print("Actual last row:")
print(data.loc[1575179])
~~~
{: .language-python}
~~~
Actual last row:
INTERVAL_TIME    2019-12-31 23:45:00
METER_FID                       8078
START_READ                 40684.475
END_READ                    40695.86
INTERVAL_READ                  0.087
Name: 1575179, dtype: object
~~~
{: .output}

```iloc``` is used to select a row or subset of rows based on the integer position of row indexers. This method also uses zero-indexing, so integers will range from 0 to 1 less than the number of rows in the dataframe. The first row would have a position integer of 0, the second row would have a position integer of 1, etc.

~~~
print(data.iloc[0])
~~~
{: .language-python}
~~~
INTERVAL_TIME    2017-01-01 00:00:00
METER_FID                        285
START_READ                 14951.787
END_READ                   14968.082
INTERVAL_READ                 0.0744
Name: 0, dtype: object
~~~
{: .output}

As above, we know there are 1575180 rows in our dataset but zero-indexing means that the position integer of the last row is 1575179. If we try to select a row using the position integer 1575180, we get the same error as before.

~~~
print(data.iloc[1575180])
~~~
{: .language-python}
~~~
IndexError: single positional indexer is out-of-bounds
~~~
{: .output}

We can also select rows using their position relative to the last row. If we want to select the last row without already knowing how many rows are in the dataframe, we can refer to its position using ```[-1]```.

~~~
print(data.iloc[-1])
~~~
{: .language-python}
~~~
INTERVAL_TIME    2019-12-31 23:45:00
METER_FID                       8078
START_READ                 40684.475
END_READ                    40695.86
INTERVAL_READ                  0.087
Name: 1575179, dtype: object
~~~
{: .output}

An alternative, more roundabout way is to use the ```len()``` function. Above, we noted that position integers will range from 0 to 1 less than the number of rows in the dataframe. In combination with the ```len()``` function, we can select the last row in a dataframe using:

~~~
print(data.iloc[len(data) - 1])
~~~
{: .language-python}
~~~
INTERVAL_TIME    2019-12-31 23:45:00
METER_FID                       8078
START_READ                 40684.475
END_READ                    40695.86
INTERVAL_READ                  0.087
Name: 1575179, dtype: object
~~~
{: .output}

> ## Challenge: Selecting Cells
>
> Given the lines of code below, put them in the correct order to read the data file *ladpu_smart_meter_data_01* and print the starting and ending meter readings.
> ~~~
> print(data.iloc[0]["START_READ"])
>
> df = pd.read\_csv("../data/ladpu\_smart\_meter\_data_01.csv")
>
> print(df.iloc[-1]["END_READ"])
> ~~~
> {: .language-python}
>
> > ## Solution
> > ~~~
> df = pd.read\_csv("../data/ladpu\_smart\_meter\_data_01.csv")
> print(df.iloc[0]["START_READ"])
> print(df.iloc[-1]["END_READ"])
> > ~~~
> > {: .output}
> {: .solution}
{: .challenge}

## Slicing Data

So far we have used label and position based indexing to select single rows from a data frame. We can select larger subsets using index slicing. Because this is a common operation, we don't have to specify the index. 

~~~
print(data[1:10])
~~~
{: .language-python}
~~~
         INTERVAL_TIME  METER_FID  START_READ   END_READ  INTERVAL_READ
1  2017-01-01 00:15:00        285   14968.082  14979.831         0.0762
2  2017-01-01 00:30:00        285   14968.082  14979.831         0.1050
3  2017-01-01 00:45:00        285   14968.082  14979.831         0.0636
4  2017-01-01 01:00:00        285   14968.082  14979.831         0.0870
5  2017-01-01 01:15:00        285   14968.082  14979.831         0.0858
6  2017-01-01 01:30:00        285   14968.082  14979.831         0.0750
7  2017-01-01 01:45:00        285   14968.082  14979.831         0.0816
8  2017-01-01 02:00:00        285   14968.082  14979.831         0.0966
9  2017-01-01 02:15:00        285   14968.082  14979.831         0.0720
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
