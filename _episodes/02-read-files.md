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
(105012, 4)
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
RangeIndex: 226752 entries, 0 to 226751
Data columns (total 5 columns):
 #   Column         Non-Null Count   Dtype  
---  ------         --------------   -----  
 0   METER_FID      226752 non-null  int64  
 1   START_READ     226752 non-null  float64
 2   END_READ       226752 non-null  float64
 3   INTERVAL_TIME  226752 non-null  object 
 4   INTERVAL_READ  226656 non-null  float64
dtypes: float64(3), int64(1), object(1)
memory usage: 8.7+ MB
None
~~~
{: .output}

Note that ```info()``` prints out all of the information we got from the ```type()``` function and the ```shape``` and ```dtypes``` attributes. 

We can also inspect some rows of data. Since the table is large - 226,752 rows - we may only want to look at the first few or the last few rows. To do this, we can use the ```head()``` and ```tail()``` functions, respectively.

~~~
print(data.head())
~~~
{: .language-python}
~~~
   METER_FID  START_READ  END_READ         INTERVAL_TIME  INTERVAL_READ
0       1003     332.308   374.561  13-JUL-2013 00:15:00         0.4098
1       1003     332.308   374.561  13-JUL-2013 00:30:00         0.1548
2       1003     332.308   374.561  13-JUL-2013 00:45:00         0.3168
3       1003     332.308   374.561  13-JUL-2013 01:00:00         0.3084
4       1003     332.308   374.561  13-JUL-2013 01:15:00         0.1320
~~~
{: .output}

~~~
print(data.tail())
~~~
{: .language-python}
~~~
        METER_FID  START_READ   END_READ         INTERVAL_TIME  INTERVAL_READ
226747       1003   56868.876  56897.653  31-DEC-2019 23:00:00         0.2592
226748       1003   56868.876  56897.653  31-DEC-2019 23:15:00         0.2820
226749       1003   56868.876  56897.653  31-DEC-2019 23:30:00         0.4464
226750       1003   56868.876  56897.653  31-DEC-2019 23:45:00         0.4626
226751       1003   56868.876  56897.653  01-JAN-2020 00:00:00         0.4662
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
   METER_FID  START_READ  END_READ         INTERVAL_TIME  INTERVAL_READ
0       1003     332.308   374.561  13-JUL-2013 00:15:00         0.4098
1       1003     332.308   374.561  13-JUL-2013 00:30:00         0.1548
2       1003     332.308   374.561  13-JUL-2013 00:45:00         0.3168
3       1003     332.308   374.561  13-JUL-2013 01:00:00         0.3084
4       1003     332.308   374.561  13-JUL-2013 01:15:00         0.1320
5       1003     332.308   374.561  13-JUL-2013 01:30:00         0.3534
6       1003     332.308   374.561  13-JUL-2013 01:45:00         0.3318
7       1003     332.308   374.561  13-JUL-2013 02:00:00         0.1566
8       1003     332.308   374.561  13-JUL-2013 02:15:00         0.3318
9       1003     332.308   374.561  13-JUL-2013 02:30:00         0.1314
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
0    13-JUL-2013 00:15:00
1    13-JUL-2013 00:30:00
2    13-JUL-2013 00:45:00
3    13-JUL-2013 01:00:00
4    13-JUL-2013 01:15:00
Name: INTERVAL_TIME, dtype: object
~~~
{: .output}

Note as well that the data type (```dtype```) is given as ```object```, even though ```datetime``` is a data type recognized by Pandas. In order to use date information in analyses, we can convert the data in the ```INTERVAL_TIME``` column into a recognized date format. Pandas come with functions to do this.

Explain what is happening in the next code block...

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
RangeIndex: 226752 entries, 0 to 226751
Data columns (total 6 columns):
 #   Column         Non-Null Count   Dtype         
---  ------         --------------   -----         
 0   METER_FID      226752 non-null  int64         
 1   START_READ     226752 non-null  float64       
 2   END_READ       226752 non-null  float64       
 3   INTERVAL_TIME  226752 non-null  object        
 4   INTERVAL_READ  226656 non-null  float64       
 5   iso_date       226752 non-null  datetime64[ns]
dtypes: datetime64[ns](1), float64(3), int64(1), object(1)
memory usage: 10.4+ MB
None
~~~
{: .output}

Note too that we are adding the new column but leaving the original date data intact.

## Combining multiple files into a single dataframe

Now that we have read a single file into our Python environment and explored its structure a little, we want to develop a process to combine all of our data files into a single dataframe.

In order to do this, we need to introduce two new concepts: lists and loops.

In Python a list is ...

~~~
my_list = ["orange", "yellow", "purple", "green", "red", "blue"]
print(my_list)
~~~
{: .language-python}
~~~
['orange', 'yellow', 'purple', 'green', 'red', 'blue']
~~~
{: .output}

We will take a more in depth look at lists in another lesson, but for now we can use the ```glob``` library that we imported earlier to create a list of the individual data files that we will combine into a single dataset.

~~~
file_list = glob.glob("*.csv")
print(len(file_list))
~~~
{: .language-python}
~~~
1825
~~~
{: .output}

If we were to print out the entire list of files, the output would be too long to read. We can print a subset of the loop using index slicing.

~~~
print(file_list[0:5])
~~~
{: .language-python}
~~~
['1003.csv', '10042.csv', '10063.csv', '10175.csv', '1020.csv']
~~~
{: .output}


The other concept is a loop, or more specifically in this case a _for_ loop. What that is...

Syntax of a for loop...

For example, now that we have a list of filenames of our data files, we can print them using a for loop.

~~~
for file in file_list[0:10]:
    print(file)
~~~
{: .language-python}
~~~
1003.csv
10042.csv
10063.csv
10175.csv
1020.csv
10211.csv
10214.csv
10226.csv
10270.csv
10274.csv
~~~
{: .output}

More pragmatically, we can use the ```concat()``` function in Pandas in combination with a ```for``` loop to combine the files in our list.
Since the dataset is large, we are going to read only the first 10 files.

~~~
# Start by reading the first file

master_data = pd.read_csv(file_list[0])

# Use a loop to concatenate the data from the other files

for file in file_list[1:10]:
    new_data = pd.read_csv(file)
    master_data = pd.concat([master_data, new_data], axis=0)
	
# Once the data have been concatenated, add the iso_date column

master_data["iso_date"] = pd.to_datetime(master_data["INTERVAL_TIME"], infer_datetime_format=True)

print(master_data.info())
~~~
{: .language-python}
~~~
<class 'pandas.core.frame.DataFrame'>
Int64Index: 2252736 entries, 0 to 226271
Data columns (total 6 columns):
 #   Column         Dtype         
---  ------         -----         
 0   METER_FID      int64         
 1   START_READ     float64       
 2   END_READ       float64       
 3   INTERVAL_TIME  object        
 4   INTERVAL_READ  float64       
 5   iso_date       datetime64[ns]
dtypes: datetime64[ns](1), float64(3), int64(1), object(1)
memory usage: 120.3+ MB
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
> file "1003.csv" and split the "INTERVAL_TIME" column into
> three new columns for "year," "month," and "day."
>
> ~~~
> data["day"] = pd.to_datetime(data["INTERVAL_TIME"], infer_datetime_format=True).dt.day)
>
> data["year"] = pd.to_datetime(data["INTERVAL_TIME"], infer_datetime_format=True).dt.year)
>
> data = pd.read_csv(1003.csv)
>
> data["month"] = pd.to_datetime(data["INTERVAL_TIME"], infer_datetime_format=True).dt.month)
> ~~~
> {: .language-python}
>
> > ## Solution
> > ~~~
> > data = pd.read_csv(1003.csv)
> >
> > data["year"] = pd.to_datetime(data["INTERVAL_TIME"], infer_datetime_format=True).dt.year)
> >
> > data["month"] = pd.to_datetime(data["INTERVAL_TIME"], infer_datetime_format=True).dt.month)
> >
> > data["day"] = pd.to_datetime(data["INTERVAL_TIME"], infer_dateteim_format=True).dt.day)
> > ~~~
> > {: .output}
> {: .solution}
{: .challenge}


> ## Challenge: Different Ways of Doing the Same Thing
>
> In the code that we wrote earlier to concatenate our data files into a single
> data frame, we combined all of the data in a "master\_data" data frame using
> a for loop. Then, once the loop was finished, we created the "iso\_date"
> column for all of the data at once.
>
> An alternative approach would be to create the "iso\_date" column for each
> file's data before concatenating. Given the lines of code below, put them
> in the correct order to add the "iso\_date" column for each file before 
> appending or concatenating the data to the "master\_data" data frame.
>
> ~~~
> master_data = pd.read_csv(file_list[0])
>
> file_list = glob.glob("*.csv")
>
> for file in file_list[1:10]:
>     master_data = pd.concat([master_data, new_data], axis=0)
>     new_data["iso_date"] = pd.to_datetime(new_data["INTERVAL_TIME"], infer_datetime_format=True)
>     new_data = pd.read_csv(file)
>
> master_data["iso_date"] = pd.to_datetime(master_data["INTERVAL_TIME"], infer_datetime_format=True)
> ~~~
> {: .language-python}
>
> > ## Solution
> > ~~~
> > file_list = glob.glob("*.csv)
> >
> > master_data = pd.read_csv(file_list[0])
> >
> > master_data["iso_date"] = pd.to_datetime(master_data["INTERVAL_TIME"], infer_datetime_format=True)
> >
> > for file in file_list[1:10]:
> >     new_data = pd.read_csv(file)
> >     new_data["iso_date"] = pd.to_datetime(new_data["INTERVAL_TIME"], infer_datetime_format=True)
> >     master_data = pd.concat([master_data, new_data], axis=0)
> > ~~~
> > {: .output}
> {: .solution}
>
> What are the advantages or disadvantages to doing it this way?
{: .challenge}

{% include links.md %}
