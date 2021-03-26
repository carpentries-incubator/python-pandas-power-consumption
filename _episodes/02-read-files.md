---
title: "Reading Data Files with Python"
teaching: 45
exercises: 20
questions:
- "How can we manipulate tabular data files in Python?"
objectives:
- "Read tabular data from a file into a program."
- "Change the structure of a dataframe."
- "Combine multiple files into a master dataset."
keypoints:
- "PANDAS is a Python library designed to work with large datasets."
- "Use `concat()` to concatenate tabular dataframes that have the same structure."
---

Time series data are often stored at intervals as files. In order to analyze the complete time series, it's necessary to combine these files. This can present challenges as the instruments used to record the data may change over time, resulting in the use of different layouts and column headers across time to describe the same types of measurements.

## Libraries

When you launch a Python environment, it opens with a set of default libraries loaded. These libraries provide access to a default set of functions, including commonly used functions like ```print()``` and ```help()```. Libraries can be used to extend the functionality of the environment beyond the default.

About Pandas...

About glob


~~~
import pandas as pd
import glob
~~~
{: .language-python}

## Reading files

~~~
data = pd.read_csv("0_power_consumption_subset.txt")
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

Use the ```shape`` attribute to see the size in rows and columns.

~~~
print(data.shape)
~~~
{: .language-python}
~~~
(207526, 9)
~~~
{: .output}

Use the ```dtypes``` attribute to see the data types of all columns in the dataset.

~~~
print(data.dtypes)
~~~
{: .language-python}
~~~
Date                      object
Time                      object
Global_active_power      float64
Global_reactive_power    float64
Voltage                  float64
Global_intensity         float64
Sub_metering_1           float64
Sub_metering_2           float64
Sub_metering_3           float64
dtype: object
~~~
{: .output}

We can limit the above to a single column.

~~~
print(data.Voltage.dtypes)
~~~
{: .language-python}
~~~
dtype('float64')
~~~
{: .output}

```shape``` and ```dtypes`` are two examples of attributes.

We can also use functions or methods to see information about the dataframe.

The ```info()``` function outputs structural information about the data.

~~~
print(data.info())
~~~
{: .language-python}
~~~
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 207526 entries, 0 to 207525
Data columns (total 9 columns):
 #   Column                 Non-Null Count   Dtype  
---  ------                 --------------   -----  
 0   Date                   207526 non-null  object 
 1   Time                   207526 non-null  object 
 2   Global_active_power    203794 non-null  float64
 3   Global_reactive_power  203794 non-null  float64
 4   Voltage                203794 non-null  float64
 5   Global_intensity       203794 non-null  float64
 6   Sub_metering_1         203794 non-null  float64
 7   Sub_metering_2         203794 non-null  float64
 8   Sub_metering_3         203794 non-null  float64
dtypes: float64(7), object(2)
memory usage: 14.2+ MB
None
~~~
{: .output}

Note that ```info()``` prints out all of the information we got from the ```type()``` function and the ```shape``` and ```dtypes``` attributes. 

We can also inspect some rows of data. Since the table is large - 207,526 rows - we may only want to look at the first few or the last few rows. To do this, we can use the ```head()``` and ````tail()``` functions, respectively.

~~~
print(data.head())
~~~
{: .language-python}
~~~
         Date      Time  ...  Sub_metering_2  Sub_metering_3
0  16/12/2006  17:24:00  ...             1.0            17.0
1  16/12/2006  17:25:00  ...             1.0            16.0
2  16/12/2006  17:26:00  ...             2.0            17.0
3  16/12/2006  17:27:00  ...             1.0            17.0
4  16/12/2006  17:28:00  ...             1.0            17.0
[5 rows x 9 columns]
~~~
{: .output}

~~~
print(data.tail())
~~~
{: .language-python}
~~~
Date      Time  ...  Sub_metering_2  Sub_metering_3
207521  9/5/2007  20:05:00  ...             0.0            16.0
207522  9/5/2007  20:06:00  ...             0.0            17.0
207523  9/5/2007  20:07:00  ...             0.0            17.0
207524  9/5/2007  20:08:00  ...             0.0            17.0
207525  9/5/2007  20:09:00  ...             0.0            17.0
[5 rows x 9 columns]
~~~
{: .output}

Note that the printed rows are truncated - the three ellipses in the output indicate that some rows have been excluded from the printout.

So far all of the functions we've used have been called using default arugments. For example, by default ```head()``` and ```tail()``` will
print the first or last five rows. If we want to view more (or fewer) rows, we can pass the number of rows as an argument. If for example
we wanted to see the first ten rows of data, we would pass that number as the argument:

~~~
print(data.head(10))
~~~
{: .language-python}
~~~
         Date      Time  ...  Sub_metering_2  Sub_metering_3
0  16/12/2006  17:24:00  ...             1.0            17.0
1  16/12/2006  17:25:00  ...             1.0            16.0
2  16/12/2006  17:26:00  ...             2.0            17.0
3  16/12/2006  17:27:00  ...             1.0            17.0
4  16/12/2006  17:28:00  ...             1.0            17.0
5  16/12/2006  17:29:00  ...             2.0            17.0
6  16/12/2006  17:30:00  ...             1.0            17.0
7  16/12/2006  17:31:00  ...             1.0            17.0
8  16/12/2006  17:32:00  ...             1.0            17.0
9  16/12/2006  17:33:00  ...             2.0            16.0
[10 rows x 9 columns]
~~~
{: .output}

> ## Challenge: Know Your Data
>
> Which of the following commands will output the data type
> of the 'Global\_active\_power' column in our 'data' dataframe?
>
> ~~~
> A. print(type(Global_active_power))
> B. print(data.info())
> C. print(data.Global_active_power.dtypes)
> D. print(Global_active_power.dtypes)
> ~~~
> {: .language-python}
>
> > ## Solution
> > ~~~
> > B and C will both work. Option B prints the dtypes 
> > for the whole dataframe. Option C prints the dtype
> > for the Global_active_power column.
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
> print(data.Voltage.dtypes)
> ~~~
> {: .language-python}
> 
> Dot notation can be used in function calls, too.
> Which of the following commands would we use to view
> the first 20 rows of data from the _Voltage_ column:
> ~~~
> A. print(data.Voltage.head())
> B. print(data.Voltage.info())
> C. print(data.head(20).Voltage)
> D. print(data.Voltage.head(20))
> ~~~
> {: .language-python}
>
> > ## Solution
> > ~~~
> > Option D prints out the first 20 rows of data
> > from the Voltage column.
> > ~~~
> > {: .output}
> {: .solution}
{: .challenge}


{% include links.md %}
