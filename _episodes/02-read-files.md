---
title: "Reading Data Files with Python"
teaching: 45
exercises: 20
questions:
- "How can we manipulate tabular data files in Python?"
objectives:
- "Read tabular data from a file into Pandas."
- "Change the structure of a dataframe."
- "Combine multiple files into a single dataset."
keypoints:
- "PANDAS is a Python library designed to work with large datasets."
- "Use `concat()` to concatenate tabular dataframes that have the same structure."
---

Our data have been stored in one CSV file per smart meter, in which the data include all of the meter readings taken from that meter during the period of study. Readings are taken every 15 minutes, for a total of 96 readings per day. 

The structure of the data has not been altered from the source data. Each CSV file contains the following fields:

- **METER_FID**: The identification number of the meter for which the data were recorded.
- **START_READ**: The meter reading at 00:15 (12:15 AM) of the date specified in the **INTERVAL_TIME** field. Note that this value is the same for each reading taken during a day, and is the same as the **END_READ** value of the previous day.
- **END_READ**: The actual value of the meter after the final interval of the date specified in the **INTERVAL_TIME** field, representing the total amount of power consumed during the whole day. This value becomes the value of the **START_READ** field for the next day.
- **INTERVAL_TIME**: The time at which a meter reading was taken. Readings are taken every 15 minutes, with the first reading for a day taken at 00:15 (12:15 AM) and representing power usage since 00:00 (12:00 AM) of the same day.
- **INTERVAL_READ**: The amount of power consumed between readings. The sum of readings between 00:15 of a given day and 00:00 of the following day should be equal (to two decimal places) to the difference between the **END_READ** and **START_READ** values for that day.

In order to inspect and analyze the data for each meter, we could read and work with each file independently. However, as we may also want to compare statistics or trends across multiple meters, it can be more practical to combine or concatenate the data from multiple meters into a single dataset. Having done that, we can group the data by meter, date, or other variables of interest. The Pandas library for Python allows us to do just this.

## Libraries

When you launch a Python environment, it opens with a set of default libraries loaded. These libraries provide access to a default set of functions, including commonly used functions like ```print()``` and ```help()```. Libraries can be used to extend the functionality of the environment beyond the default. Here, we are going to import the ```pandas``` and ```glob``` libraries to add functionality to our environment. Specifically, ```pandas``` is a library that provides methods for indexing and manipulating large datasets. The ```glob``` library allows us to quickly create lists of files based on patterns in filenames. 

~~~
import pandas as pd
import glob
~~~
{: .language-python}

## Reading files

Creating a list of filenames that we want to read is a common way of iterating over files in Python. We use ```glob``` to create the list, though for now we will only read the first file in the list. 

~~~
file_list = glob.glob('../data/*.csv')
print(file_list)
~~~
{: .language-python}

Lists may or may not be sorted in Python. That is, our files may appear in any order in the list. We can sort the files by name before reading the first file.

~~~
file_list = sorted(file_list)
data = pd.read_csv(file_list[0])
~~~
{: .language-python}

## Inspecting the data

The data is assigned to the variable ```data```, which is an object.

Get information about ```data``` as an object, and also information about the data.

~~~
# Find the data type of the 'data' object

print(type(data))
~~~
{: .language-python}
~~~
<class 'pandas.core.frame.DataFrame'>
~~~
{: .output}

We can get information about the data by requesting its attributes or using functions.

Use the ```shape``` attribute to see the size in rows and columns.

~~~
print(data.shape)
~~~
{: .language-python}
~~~
(105012, 5)
~~~
{: .output}

Use the ```dtypes``` attribute to see the data types of all columns in the dataset.

~~~
print(data.dtypes)
~~~
{: .language-python}
~~~
INTERVAL_TIME     object
METER_FID          int64
START_READ       float64
END_READ         float64
INTERVAL_READ    float64
dtype: object
~~~
{: .output}

We can limit the above to a single column.

~~~
print(data.START_READ.dtypes)
~~~
{: .language-python}
~~~
dtype('float64')
~~~
{: .output}

```shape``` and ```dtypes``` are two examples of attributes.

We can also use functions or methods to see information about the dataframe.

The ```info()``` function outputs structural information about the data.

~~~
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

Note that ```info()``` prints out all of the information we got from the ```type()``` function and the ```shape``` and ```dtypes``` attributes. 

We can also inspect some rows of data. Since the table is large - over 100,000 rows - we may only want to look at the first few or the last few rows. To do this, we can use the ```head()``` and ```tail()``` functions, respectively.

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

~~~
print(data.tail())
~~~
{: .language-python}
~~~
              INTERVAL_TIME  METER_FID  START_READ   END_READ  INTERVAL_READ
105007  2019-12-31 22:45:00        285   28358.546  28397.749         0.4944
105008  2019-12-31 23:00:00        285   28358.546  28397.749         0.4974
105009  2019-12-31 23:15:00        285   28358.546  28397.749         0.4422
105010  2019-12-31 23:30:00        285   28358.546  28397.749         0.4212
105011  2019-12-31 23:45:00        285   28358.546  28397.749         0.3816
~~~
{: .output}

So far we have called all of the functions using default arugments. For example, by default ```head()``` and ```tail()``` will
print the first or last five rows. If we want to view more (or fewer) rows, we can pass the number of rows as an argument. If for example
we wanted to see the first ten rows of data, we would pass that number as the argument:

~~~
print(data.head(10))
~~~
{: .language-python}
~~~
         INTERVAL_TIME  METER_FID  START_READ   END_READ  INTERVAL_READ
0  2017-01-01 00:00:00        285   14951.787  14968.082         0.0744
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

> ## Challenge: Know Your Data
>
> Which of the following commands will output the data type
> of the 'INTERVAL\_TIME\' column in our 'data' dataframe?
>
> ~~~
> A. print(type(INTERVAL_TIME))
> B. print(data.info())
> C. print(data.INTERVAL_TIME.dtypes)
> D. print(INTERVAL_TIME.dtypes)
> ~~~
> {: .language-python}
>
> > ## Solution
> > ~~~
> > B and C will both work. Option B prints the dtypes 
> > for the whole dataframe. Option C prints the dtype
> > for the INTERVAL_TIME column.
> > ~~~
> > {: .output}
> {: .solution}
{: .challenge}


> ## Challenge: Drilling Down
>
> We have seen how we can use _dot notation_ to get the 'dtypes' information
> for a single column:
>
> ~~~
> print(data.START_READ.dtypes)
> ~~~
> {: .language-python}
> 
> Dot notation can be used in function calls, too.
> Which of the following commands would we use to view
> the first 20 rows of data from the *START_READ* column:
> ~~~
> A. print(data.START_READ.head())
> B. print(data.START_READ.info())
> C. print(data.head(20).START_READ)
> D. print(data.START_READ.head(20))
> ~~~
> {: .language-python}
>
> > ## Solution
> > ~~~
> > Options C and D print out the first 20 rows of data
> > from the START_READ column.
> > ~~~
> > {: .output}
> {: .solution}
{: .challenge}


## Modifying data frames - adding columns

If we inspect the first five rows of the ```INTERVAL_TIME``` column, we see that dates are provided in a long format.

~~~
print(data.INTERVAL_TIME.head())
~~~
{: .language-python}
~~~
0    2017-01-01 00:00:00
1    2017-01-01 00:15:00
2    2017-01-01 00:30:00
3    2017-01-01 00:45:00
4    2017-01-01 01:00:00
Name: INTERVAL_TIME, dtype: object
~~~
{: .output}

Note as well that the data type (```dtype```) is given as ```object```, even though ```datetime``` is a data type recognized by Pandas. In order to use date information in analyses, we can convert the data in the ```INTERVAL_TIME``` column into a recognized date format. In a later episode, we will look at ways we can manipulate datetime information by creating a datetime index. For now we will begin by exploring some of Pandas datetime methods without reindexing the data.

We can change the data type of the "INTERVAL_TIME" column in place, but for a closer look at what is happening we will save the date data in a new column with the updated data type.

~~~
data["iso_date"] = pd.to_datetime(data["INTERVAL_TIME"], infer_datetime_format=True)
~~~
{: .language-python}

We can verify that the new column was added and that the data type of the new column is ```datetime``` using the ```info()``` command.

~~~
print(data.info())
~~~
{: .language-python}
~~~
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 105012 entries, 0 to 105011
Data columns (total 6 columns):
 #   Column         Non-Null Count   Dtype         
---  ------         --------------   -----         
 0   INTERVAL_TIME  105012 non-null  object        
 1   METER_FID      105012 non-null  int64         
 2   START_READ     105012 non-null  float64       
 3   END_READ       105012 non-null  float64       
 4   INTERVAL_READ  105012 non-null  float64       
 5   iso_date       105012 non-null  datetime64[ns]
dtypes: datetime64[ns](1), float64(3), int64(1), object(1)
memory usage: 4.8+ MB
None
~~~
{: .output}

Note too that we are adding the new column but leaving the original date data intact.

## Combining multiple files into a single dataframe

Now that we have read a single file into our Python environment and explored its structure a little, we want to develop a process to combine all of our data files into a single dataframe. We can do this using _list comprehension_ to read the files in our file list and concatenate them into a single dataframe.

To do this, we will re-assign our ```data``` variable to include the complete, concatenated dataset. Note that it is a large dataset, with over 1,500,000 rows.

~~~
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
{: .output}

Let's take a moment to unpack the line of code that creates the dataframe:

~~~
data = pd.concat([pd.read_csv(f) for f in file_list])
~~~
{: .language-python}

This line of code includes several statements that are evaluated in the following order:

1. The for loop ```for f in file_list``` is evaluated first. As denoted by the square brackets, this creates a list of dataframes by calling Pandas' ```read_csv()``` function on each of the files in the *file_list* variable that we created above.
1. The list of 15 dataframes is combined into a single dataframe using the ```concat()``` function. This function takes as its default argument a list of dataframes that share the same structure, and combines them vertically into a single dataframe.

Now we can add the **iso_date** column using the same command as before:

~~~
data["iso_date"] = pd.to_datetime(data["INTERVAL_TIME"], infer_datetime_format=True)
print(data.info())
~~~
{: .language-python}
~~~
<class 'pandas.core.frame.DataFrame'>
Int64Index: 1575180 entries, 0 to 105011
Data columns (total 6 columns):
 #   Column         Non-Null Count    Dtype         
---  ------         --------------    -----         
 0   INTERVAL_TIME  1575180 non-null  object        
 1   METER_FID      1575180 non-null  int64         
 2   START_READ     1575180 non-null  float64       
 3   END_READ       1575180 non-null  float64       
 4   INTERVAL_READ  1575180 non-null  float64       
 5   iso_date       1575180 non-null  datetime64[ns]
dtypes: datetime64[ns](1), float64(3), int64(1), object(1)
memory usage: 84.1+ MB
None
~~~
{: .output}


> ## Challenge: Separating Dates into Columns
>
> It can be useful in a variety of contexts to split date data into multiple columns, 
> with one column for the year, one for the month, and another for the day. This can
> facilitate filtering or ordering by date in systems like SQLite, for example, that
> don't by default have a date data type.
>
> Given the lines of code below, put them in the correct order to read the data
> file "ladpu_smart_meter_data_01.csv" and split the "INTERVAL_TIME" column into
> three new columns for "year," "month," and "day."
>
> ~~~
> data["day"] = pd.to_datetime(data["INTERVAL_TIME"], infer_datetime_format=True).dt.day
>
> data["year"] = pd.to_datetime(data["INTERVAL_TIME"], infer_datetime_format=True).dt.year
>
> data = pd.read_csv("../data/ladpu_smart_meter_data_01.csv")
>
> data["month"] = pd.to_datetime(data["INTERVAL_TIME"], infer_datetime_format=True).dt.month
> ~~~
> {: .language-python}
>
> > ## Solution
> > ~~~
> > data = pd.read_csv("../data/ladpu_smart_meter_data_01.csv")
> >
> > data["year"] = pd.to_datetime(data["INTERVAL_TIME"], infer_datetime_format=True).dt.year
> >
> > data["month"] = pd.to_datetime(data["INTERVAL_TIME"], infer_datetime_format=True).dt.month
> >
> > data["day"] = pd.to_datetime(data["INTERVAL_TIME"], infer_datetime_format=True).dt.day
> > ~~~
> > {: .output}
> {: .solution}
{: .challenge}

{% include links.md %}
