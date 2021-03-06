# ExpressionAble-CLI

### Background

**The context**: Gene-expression levels help in determining cellular function. To understand these roles, scientists have performed thousands of gene-expression studies using microarray assays and next-generation sequencing. Such data are typically stored in tabular files (with rows and columns).

**The problem**: Different functional-genomics repositories and preprocessing tools store gene-expression data in a cacophony of file formats. Analysis tools (such as Python, R, and Excel) do not support all these formats natively. It is time consuming and labor intensive for bioinformaticians to translate data between file formats and identify samples that match specific criteria.

**The solution**: We developed the ExpressionAble tool to reduce the time from data acquisition to analysis for researchers studying gene expression. This tool can help researchers more easily work with their own data as well as the immense gene-expression resources in public databases.

### expressionable command-line tool

This is the official repository for the `expressionable` command-line tool. It is a command-line interface for the [expressionable](https://github.com/srp33/expressionable) Python module.

From the command-line you can easily take advantage of ExpressionAble's features, such as:

* Transformation of tabular data sets from one format to another.
* Querying large data sets to extract useful data.
* Selection of additional columns/features to include in the resulting data set.
* Option to gzip resulting data sets, as well as the ability to read gzipped files.
* Merging multiple data files of various types into a single file. 

### Install

```bash
pip3 install expressionable-cli
```

### Basic Use

To view instructions for use at any time, simply type the command `expressionable --help` or `ea --help` into the terminal at any time.

Doing so will bring up the following:

```bash
$ expressionable --help
usage: expressionable [-h] [-i File_Type] [-o File_Type] [-t] [-f "FILTER"]
                  [-c COLUMNS] [-a] [-g] [-s SET_INDEX]
                  input_file output_file

Import, filter, and transform data into a format of your choice!

positional arguments:
  input_file            Data file to be imported, filtered, and/or transformed
  output_file           File path to which results are exported

optional arguments:
  -h, --help            show this help message and exit
  -i File_Type, --input_file_type File_Type
                        Type of file to be imported. If not specified, file
                        type will be determined by the file extension given.
                        Available choices are: CSV, TSV, JSON, Excel, HDF5,
                        Parquet, MsgPack, Stata, Pickle, SQLite, ARFF, GCT,
                        Kallisto, GEO, Salmon
  -o File_Type, --output_file_type File_Type
                        Type of file to which results are exported. If not
                        specified, file type will be determined by the file
                        extension given. Available choices are: CSV, TSV,
                        JSON, Excel, HDF5, Parquet, MsgPack, Stata, Pickle,
                        SQLite, ARFF, GCT, RMarkdown, JupyterNotebook
  -t, --transpose       Transpose index and columns in the output file
  -f "FILTER", --filter "FILTER"
                        Filter data using python logical syntax. Your filter
                        must be surrounded by quotes. For example: -f
                        "ColumnName1 > 12.5 and (ColumnName2 == 'x' or
                        ColumnName2 =='y')"
  -c COLUMNS, --columns COLUMNS
                        List of additional column names to include in the
                        output file. Column names must be seperated by commas
                        and without spaces. For example: -c
                        ColumnName1,ColumnName2,ColumnName3
  -a, --all_columns     Includes all columns in the output file. Overrides the
                        "--columns" flag
  -g, --gzip            Gzips the output file
  -s SET_INDEX, --set_index SET_INDEX
                        Sets the given column to become the index column,
                        where appropriate.
```

There are only two required arguments when using the `expressionable` command: the path to the file you wish to read,
and the path to a file you wish to produce. For example, if you had an Excel file called "input_file.xlsx" and you 
 wanted to convert it to a TSV file called "output_file.tsv", you would enter 
`expressionable input_file.xlsx output_file.tsv` into the terminal to execute the conversion.

ExpressionAble automatically infers both the format of the input file and the format of the file you wish to create, based
on the file extension. If for some reason the extensions are irregular or missing, you can specify the 
format of the input file using the `--input_file_type` flag, followed by the name of the file type,
and specify the format of the output file using the `--output_file_type` flag, followed by the name of the file type.

To apply filters during the transformation, use the `--filter` flag, followed by a string query in double quotations.
Syntax for such a query uses basic Python logical syntax, as shown by the following example:
`--filter "ColumnName1 > 12.5 and (ColumnName2 == 'x' or ColumnName2 =='y')"`  

Applying filters means that only those columns that are filtered on (in the above example, ColumnName1 and ColumnName2)
will appear in the output file. If you wish to include additional columns, you can do so with the `--columns` flag 
followed by a list of comma-separated column names. If you wish to include all columns in the output, you can simply
use the `--all_columns` flag.

### Currently Supported Formats

##### Input Formats:

* CSV
* TSV (samples as rows, variables as columns)
* JSON
* Excel
* HDF5
* Parquet
* MsgPack
* Stata
* Pickle
* SQLite
* ARFF
* GCT
* GCTX
* PDF
* Gene Expression Omnibus
* Kallisto (RNA-Sequencing)
* Salmon (RNA-Sequencing)
* STAR (RNA-Sequencing)
* HT-Seq (RNA-Sequencing)
* CBio Portal (RNA expression format)

##### Output Formats:

* CSV 
* TSV
* JSON
* Excel
* HDF5
* Parquet
* MsgPack
* Stata 
* Pickle
* SQLite 
* ARFF 
* GCT 
* RMarkdown notebook
* Jupyter notebook

### Python module

As an alternative to this tool, you can use the [Python module](https://github.com/srp33/ExpressionAble) to programmatically convert between file formats.
