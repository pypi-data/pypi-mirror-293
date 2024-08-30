# Data_analyser

data_analyser is a Python package for generating comprehensive profiling reports from pandas DataFrames, helping you quickly understand your data's structure and quality.


## ▶️ Quickstart

### Install
```cmd
pip install data_analyser
```
or
```cmd
conda install -c conda-forge data_analyser
```
### Start profiling

Start by loading your pandas `DataFrame` as you normally would, e.g. by using:

```python
import numpy as np
import pandas as pd
from data_analyser import ProfileReport

df = pd.DataFrame(np.random.rand(100, 5), columns=["a", "b", "c", "d", "e"])
```

To generate the standard profiling report, merely run:

```python
profile = ProfileReport(df, title="Profiling Report")
profile.to_file("output.html")

```

## 📊 Key features

- **Type inference**: automatic detection of columns' data types (*Categorical*, *Numerical*, *Date*, etc.)
- **Warnings**: A summary of the problems/challenges in the data that you might need to work on (*missing data*, *inaccuracies*, *skewness*, etc.)
- **Univariate analysis**: including descriptive statistics (mean, median, mode, etc) and informative visualizations such as distribution histograms
- **Multivariate analysis**: including correlations, a detailed analysis of missing data, duplicate rows, and visual support for variables pairwise interaction
- **Time-Series**: including different statistical information relative to time dependent data such as auto-correlation and seasonality, along ACF and PACF plots.
- **Text analysis**: most common categories (uppercase, lowercase, separator), scripts (Latin, Cyrillic) and blocks (ASCII, Cyrilic)
- **File and Image analysis**: file sizes, creation dates, dimensions, indication of truncated images and existence of EXIF metadata
- **Compare datasets**: one-line solution to enable a fast and complete report on the comparison of datasets
- **Flexible output formats**: all analysis can be exported to an HTML report that can be easily shared with different parties, as JSON for an easy integration in automated systems and as a widget in a Jupyter Notebook.

The report contains three additional sections:

- **Overview**: mostly global details about the dataset (number of records, number of variables, overall missigness and duplicates, memory footprint)
- **Alerts**: a comprehensive and automatic list of potential data quality issues (high correlation, skewness, uniformity, zeros, missing values, constant values, between others)
- **Reproduction**: technical details about the analysis (time, version and configuration)


### Exporting the report to a file

To generate a HTML report file, save the `ProfileReport` to an object and use the `to_file()` function:

```python
profile.to_file("your_report.html")
```

Alternatively, the report's data can be obtained as a JSON file:

```python
# As a JSON string
json_data = profile.to_json()

# As a file
profile.to_file("your_report.json")
```


## 🛠️ Installation


### Using pip


You can install using the `pip` package manager by running:

```sh
pip install -U data_analyser
```

#### Extras

The package declares "extras", sets of additional dependencies.

* `[notebook]`: support for rendering the report in Jupyter notebook widgets.
* `[unicode]`: support for more detailed Unicode analysis, at the expense of additional disk space.
* `[pyspark]`: support for pyspark for big dataset analysis

Install these with e.g.

```sh
pip install -U data_analyser[notebook,unicode,pyspark]
```



## 🙋 Support
Need help? Want to share a perspective? Report a bug? Ideas for collaborations? 

Shoot me an email @ leandroofalero@outlook.com



## 🤝🏽 Contributing

A big thank you to all the team at Ydata-profiling in whose work I based this package


## License 



This project is licensed under the MIT License
