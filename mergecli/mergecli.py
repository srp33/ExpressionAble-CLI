#! /usr/bin/env python
import pyarrow
import pandas as pd
from expressionable.errors import ColumnNotFoundError
from expressionable import ExpressionAble
import argparse

def execute_merge(args):
    try:
        if len(args.input_files_types) == 1:
            ea = ExpressionAble(args.input_files[0], args.input_files_types[0])
            types = args.input_files_types
        elif len(args.input_files_types)>1:
            ea = ExpressionAble(args.input_files[0], args.input_files_types[0])
            types = args.input_files_types[1:]
        else:
            ea = ExpressionAble(args.input_files[0])
            types = []
        ea.merge_files(args.input_files[1:], out_file_path=args.output_file, files_to_merge_types=types,
                       out_file_type=args.output_file_type, gzip_results=args.gzip, on=args.on_column, how=args.how)
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
            "Warning: the following columns requested were not found and therefore not included in the output: " + str(
                e))

def main():
    parser = argparse.ArgumentParser(description="Merge data files of various types into a single file!")
    supported_output_files = ["CSV", "TSV", "JSON", "Excel", "HDF5", "Parquet", "MsgPack", "Stata",
                              "Pickle", "SQLite", "ARFF", "GCT", "RMarkdown", "JupyterNotebook"]
    parser.add_argument("-i", "--input_files", nargs="+", help="List of files that will be merged together. "
                                                             "Files must have appropriate extensions to be recognized properly.")
    parser.add_argument("-f", "--input_files_types", nargs="*", default=[],
                        help="list of file types corresponding to files_to_merge. If the list is empty, types will be inferred from file extensions. If the list has one value, that will be the type of every file in files_to_merge. If the list has the same number of items as files_to_merge, the types will correspond to the files in files_to_merge.")
    parser.add_argument("-o", "--output_file", help="File path to which results are exported")
    parser.add_argument("-t", "--output_file_type",
                        help="Type of file to which results are exported. If not specified, "
                             "file type will be determined by the file extension given. "
                             "Available choices are: " + ", ".join(supported_output_files),
                        choices=supported_output_files, metavar='File_Type')
    parser.add_argument("-g", "--gzip", help="Gzips the output file", action="store_true")
    parser.add_argument("-c", "--on_column", help="Merge files on a specific column", default=None)
    parser.add_argument("--how", help="Type of merge to perform. Options are left, right, inner, or outer,"
                                      " with inner being default behavior.", default="inner")
    parser.set_defaults(func=execute_merge)
    args = parser.parse_args()
    args.func(args)
