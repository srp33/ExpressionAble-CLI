#! /usr/bin/env python

from expressionable.errors import ColumnNotFoundError
from expressionable import ExpressionAble
import argparse
import sys
import pandas as pd
import pyarrow


def is_gzipped(file_name):
    extensions = file_name.rstrip("\n").split(".")
    if extensions[len(extensions) - 1] == 'gz':
        return True
    return False


def parse_columns(columns):
    if columns == []:
        return []
    colList = columns.rstrip("\n").split(",")
    return colList


def execute_expressionable(allCols, args, colList, gzip, inFileType, indexCol, isTransposed, outFileType, filters):
    try:
        ea = ExpressionAble(args.input_file, inFileType)
        ea.export_filter_results(args.output_file, outFileType, filters=filters, columns=colList, transpose=isTransposed,
                                 include_all_columns=allCols, gzip_results=gzip, index=indexCol)
    except pyarrow.lib.ArrowIOError as e:
        print("Error: " + str(e))
    except pd.core.computation.ops.UndefinedVariableError as e:
        print("Error: Variable not found: " + str(e))
        print("Hint: If the variable not found is a column name, make sure it is spelled correctly. "
              "If the variable is a value, make sure it is surrounded by quotes")
    except SyntaxError as error:
        try:
            print("Error: \'" + error.text.rstrip() + "\'\n" + " " * (error.offset + 6) + "^")
        except AttributeError:
            pass
        finally:
            print("Syntax is invalid. Valid python syntax must be used")
    except ValueError as e:
        print("Error: " + str(e))
    except TypeError as e:
        print("Error: Type error. You may have tried to compare items that are not comparable (strings and integers),"
              " or you may left the filter blank")
    except KeyError as e:
        print("Error: " + str(e))
    except NotImplementedError as e:
        print("Error: " + str(e))
    except RecursionError as e:
        print("Error: " + str(e))
    except ColumnNotFoundError as e:
        print(
            "Error: columns you requested or tried to filter on were not found in the file and the following"
            " error was caught: " + str(e))


def run(args, parser):
    inFileType = args.input_file_type
    outFileType = args.output_file_type
    isTransposed = args.transpose
    filters = args.filter
    colList = parse_columns(args.columns)
    # TODO find a way to remove duplicates in the list without reordering the list (ex: -c int1, int1, int2)
    allCols = args.all_columns
    gzip = args.gzip
    indexCol = args.set_index

    # Handle argparse errors and user failures
    # TODO disable transpose entirely?
    if isTransposed and outFileType == 'parquet' or outFileType == 'stata':
        print("Error: Parquet and Stata file types do not support transposing. "
              "Either choose a different output file type or remove the --transpose flag")
        sys.exit()

    if filters != None and not ("==" in filters or "!=" in filters or "<" in filters or ">" in filters or "<=" in filters or ">=" in filters):
        print("Error: Filter must be an expression involving an operator such as '==' or '<'. "
              "If you simply want to include specific columns in the output, try using the --columns flag")
        sys.exit()

    if (not is_gzipped(args.output_file) and args.gzip):
        print("NOTE: Because you requested the output be gzipped, it will be saved to " + args.output_file + ".gz")
    if is_gzipped(args.output_file):
        gzip = True


    execute_expressionable(allCols, args, colList, gzip, inFileType, indexCol, isTransposed, outFileType, filters)


def main():
    # TODO prevent flags from being used twice. What's the best way to do this?
    parser = argparse.ArgumentParser(description="Import, filter, and transform data into a format of your choice!")
    supported_input_files = ["CSV", "TSV", "JSON", "Excel", "HDF5", "Parquet", "MsgPack", "Stata",
                             "Pickle", "SQLite", "ARFF", "GCT", "GCTX", "StarReads", "PDF", "Kallisto", "GEO", "Salmon"]
    supported_output_files = ["CSV", "TSV", "JSON", "Excel", "HDF5", "Parquet", "MsgPack", "Stata",
                              "Pickle", "SQLite", "ARFF", "GCT", "RMarkdown", "JupyterNotebook"]

    parser.add_argument("input_file", help="Data file to be imported, filtered, and/or transformed")
    parser.add_argument("output_file", help="File path to which results are exported")
    parser.add_argument("-i", "--input_file_type",
                        help="Type of file to be imported. If not specified, file type will be "
                             "determined by the file extension given. Available choices are: " +
                             ", ".join(supported_input_files), metavar='File_Type')  # choices = supportedFiles,
    parser.add_argument("-o", "--output_file_type",
                        help="Type of file to which results are exported. If not specified, "
                             "file type will be determined by the file extension given. "
                             "Available choices are: " + ", ".join(supported_output_files),
                        choices=supported_output_files, metavar='File_Type')
    parser.add_argument("-t", "--transpose", help="Transpose index and columns in the output file", action="store_true")
    parser.add_argument("-f", "--filter", type=str, default=None,
                        help="Filter data using python logical syntax. Your filter must be surrounded "
                             "by quotes.\n\nFor example: -f \"ColumnName1 > 12.5 and (ColumnName2 == 'x' or ColumnName2 =='y')\"",
                        metavar="\"FILTER\"", action='store')
    parser.add_argument("-c", "--columns", action='store', default=[],
                        help="List of additional column names to include in the output "
                             "file. Column names must be seperated by commas and without "
                             "spaces. For example: -c ColumnName1,ColumnName2,ColumnName3")
    parser.add_argument("-a", "--all_columns",
                        help="Includes all columns in the output file. Overrides the \"--columns\" flag",
                        action="store_true")
    parser.add_argument("-g", "--gzip", help="Gzips the output file", action="store_true")
    parser.add_argument("-s", "--set_index", default=None, help="Sets the given column to become the index column, "
                                                                    "where appropriate.")
    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args, parser)


# if __name__ == "__main__":
#     main()
