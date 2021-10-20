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

It's important to keep some of this terminology clear, because in addition to _indexing_ rows and column labels, Pandas creates an _index_ of row labels for every dataframe. This index can be specified when the dataframe is created, or alternatively Pandas will create an integer based index of row labels by default.

We can demonstrate this by reading a single file from our dataset. First, let's load the libraries we will use for this episode.

~~~
import pandas as pd
import glob
~~~
{: .language-python}

Next we use the ```glob()``` function to create a list of files. Then we read the first file in the list into a new dataframe.

~~~
file_list = glob.glob("./lesson_data/*.csv")
df = pd.read_csv(file_list[0])
df.info()
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


{% include links.md %}
