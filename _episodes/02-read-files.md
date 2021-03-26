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

When you launch a Python environment, it opens with a set of default libraries loaded. These libraries provide access to a default set of functions, including commonly used functions like ~~~print~~~ and ~~~help~~~. Libraries can be used to extend the functionality of the environment beyond the default.

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

The data is assigned to the variable ~~~data~~~, which is an object.

Get information about ~~~data~~ as an object, and also information about the data.

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

~~~
print(data.shape)
~~~
{: .language-python}
~~~
(207526, 9)
~~~
{: .output}


> ## Check Your Understanding
>
> What values do the variables `mass` and `age` have after each of the following statements?
> Test your answer by executing the lines.
>
> ~~~
> mass = 47.5
> age = 122
> mass = mass * 2.0
> age = age - 20
> ~~~
> {: .language-python}
>
> > ## Solution
> > ~~~
> > `mass` holds a value of 47.5, `age` does not exist
> > `mass` still holds a value of 47.5, `age` holds a value of 122
> > `mass` now has a value of 95.0, `age`'s value is still 122
> > `mass` still has a value of 95.0, `age` now holds 102
> > ~~~
> > {: .output}
> {: .solution}
{: .challenge}

{% include links.md %}
