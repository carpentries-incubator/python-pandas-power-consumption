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

About glob...


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


## Modifying data frames - adding columns

If we inspect the first five rows of the ```Date``` column, we see that dates are provided in a non-standard format. This makes it difficult to do date math, create histograms, etc.

~~~
print(data.Date.head())
~~~
{: .language-python}
~~~
0    16/12/2006
1    16/12/2006
2    16/12/2006
3    16/12/2006
4    16/12/2006
Name: Date, dtype: object
~~~
{: .output}

Note as well that the data type (```dtype```) is given as ```object```, even though ```datetime``` is a data type recognized by Pandas. In order to use date information in analyses, we have to convert the data in the ```Date``` column into a recognized date format. Pandas come with functions to do this.

Explain what is happening in the next code block...

~~~
data["iso_date"] = pd.to_datetime(data["Date"], format='%d/%m/%Y')
~~~
{: .language-python}

We can verify that the new column was added and that the data type of the new column is ```datetime``` using the ```info()``` command.

~~~
print(data.info())
~~~
{: .language-python}
~~~
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 207526 entries, 0 to 207525
Data columns (total 10 columns):
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
 9   iso_date               207526 non-null  datetime64[ns]
dtypes: datetime64[ns](1), float64(7), object(2)
memory usage: 15.8+ MB
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
file_list = glob.glob("*.txt")
print(file_list)
~~~
{: .language-python}
~~~
['0_power_consumption_subset.txt', '1_power_consumption_subset.txt', '2_power_consumption_subset.txt', '3_power_consumption_subset.txt', '4_power_consumption_subset.txt', '5_power_consumption_subset.txt', '6_power_consumption_subset.txt', '7_power_consumption_subset.txt', '8_power_consumption_subset.txt', '9_power_consumption_subset.txt']
~~~
{: .output}

The other concept is a loop, or more specifically in this case a _for_ loop. What that is...

Syntax of a for loop...

For example, now that we have a list of filenames of our data files, we can print them using a for loop.

~~~
for file in file_list:
    print(file)
~~~
{: .language-python}
~~~
0_power_consumption_subset.txt
1_power_consumption_subset.txt
2_power_consumption_subset.txt
3_power_consumption_subset.txt
4_power_consumption_subset.txt
5_power_consumption_subset.txt
6_power_consumption_subset.txt
7_power_consumption_subset.txt
8_power_consumption_subset.txt
9_power_consumption_subset.txt
~~~
{: .output}

More pragmatically, we can use the ```concat()``` function in Pandas in combination with a ```for``` loop to combine the files in our list.

~~~
# Start by reading the first file

master_data = pd.read_csv(file_list[0])

# Use a loop to concatenate the data from the other files

for file in file_list:
    new_data = pd.read_csv(file)
    master_data = pd.concat([master_data, new_data], axis=0)
	
# Once the data have been concatenated, add the iso_date column

master_data["iso_date"] = pd.to_datetime(master_data["Date"], format='%d/%m/%Y')

print(master_data.info())
~~~
{: .language-python}
~~~
<class 'pandas.core.frame.DataFrame'>
Int64Index: 2282785 entries, 0 to 207524
Data columns (total 10 columns):
 #   Column                 Dtype         
---  ------                 -----         
 0   Date                   object        
 1   Time                   object        
 2   Global_active_power    float64       
 3   Global_reactive_power  float64       
 4   Voltage                float64       
 5   Global_intensity       float64       
 6   Sub_metering_1         float64       
 7   Sub_metering_2         float64       
 8   Sub_metering_3         float64       
 9   iso_date               datetime64[ns]
dtypes: datetime64[ns](1), float64(7), object(2)
memory usage: 191.6+ MB
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
> file "1\_power\_consumption\_subset.txt" and split the "Date" column into
> three new columns for "year," "month," and "day."
>
> ~~~
> data["day"] = pd.to_datetime(data["Date"], format='%d/%m/%Y').dt.day)
>
> data["year"] = pd.to_datetime(data["Date"], format='%d/%m/%Y').dt.year)
>
> data = pd.read_csv(1_power_consumption_subset.txt)
>
> data["month"] = pd.to_datetime(data["Date"], format='%d/%m/%Y').dt.month)
> ~~~
> {: .language-python}
>
> > ## Solution
> > ~~~
> > data = pd.read_csv(1_power_consumption_subset.txt)
> >
> > data["year"] = pd.to_datetime(data["Date"], format='%d/%m/%Y').dt.year)
> >
> > data["month"] = pd.to_datetime(data["Date"], format='%d/%m/%Y').dt.month)
> >
> > data["day"] = pd.to_datetime(data["Date"], format='%d/%m/%Y').dt.day)
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
> file_list = glob.glob("*.txt")
>
> for file in file_list:
>     master_data = pd.concat([master_data, new_data], axis=0)
>     new_data["iso_date"] = pd.to_datetime(new_data["Date"], format='%d/%m/%Y')
>     new_data = pd.read_csv(file)
>
> master_data["iso_date"] = pd.to_datetime(master_data["Date"], format='%d/%m/%Y')
> ~~~
> {: .language-python}
>
> > ## Solution
> > ~~~
> > file_list = glob.glob("*.txt)
> >
> > master_data = pd.read_csv(file_list[0])
> >
> > master_data["iso_date"] = pd.to_datetime(master_data["Date"], format='%d/%m/%Y')
> >
> > for file in file_list:
> >     new_data = pd.read_csv(file)
> >     new_data["iso_date"] = pd.to_datetime(new_data["Date"], format='%d/%m/%Y')
> >     master_data = pd.concat([master_data, new_data], axis=0)
> > ~~~
> > {: .output}
> {: .solution}
>
> What are the advantages or disadvantages to doing it this way?
{: .challenge}

{% include links.md %}
