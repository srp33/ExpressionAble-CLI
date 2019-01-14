from shapeshifter.errors import ColumnNotFoundError
from shapeshifter import ShapeShifter
import argparse
import sys
import pandas as pd
import pyarrow

def isGzipped(fileName):
    extensions=fileName.rstrip("\n").split(".")
    if extensions[len(extensions)-1]=='gz':
        return True
    return False

def parseColumns(columns):
    colList = columns.rstrip("\n").split(",")
    return colList

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Import, filter, and transform data into a format of your choice!")
    supportedFiles=["CSV", "TSV", "JSON","Excel","HDF5","Parquet","MsgPack","Stata",
                    "Pickle", "SQLite","ARFF", "GCT", "Kallisto"]

    parser.add_argument("input_file", help = "Data file to be imported, filtered, and/or transformed")
    parser.add_argument("output_file", help = "File path to which results are exported")
    parser.add_argument("-i","--input_file_type", help = "Type of file to be imported. If not specified, file type will be "
                                                         "determined by the file extension given. Available choices are: " +
                                                         ", ".join(supportedFiles),  metavar= 'File_Type') #choices = supportedFiles,
    parser.add_argument("-o","--output_file_type", help = "Type of file to which results are exported. If not specified, "
                                                          "file type will be determined by the file extension given. "
                                                          "Available choices are: "+", ".join(supportedFiles), choices = supportedFiles, metavar='File_Type')
    parser.add_argument("-t","--transpose", help="Transpose index and columns in the output file", action= "store_true")
    parser.add_argument("-f", "--filter", help = "Filter data using python logical syntax. Your filter must be surrounded "
                                                 "by quotes.\n\nFor example: -f \"ColumnName1 > 12.5 and (ColumnName2 == 'x' or ColumnName2 =='y')\"", metavar="\"FILTER\"", action='append')
    parser.add_argument("-c","--columns", action='append', help ="List of additional column names to include in the output "
                                                                 "file. Column names must be seperated by commas and without "
                                                                 "spaces. For example: -c ColumnName1,ColumnName2,ColumnName3")
    parser.add_argument("-a", "--all_columns", help = "Includes all columns in the output file. Overrides the \"--columns\" flag", action="store_true")
    parser.add_argument("-g","--gzip", help = "Gzips the output file", action="store_true")
    parser.add_argument("-s","--set_index", help="Sets the given column to become the index column, where appropriate. If not set, the default index will be 'Sample'",nargs=1)
    args = parser.parse_args()

    inFileType = None
    if args.input_file_type:
        inFileType = args.input_file_type
    isInFileGzipped = isGzipped(args.input_file)

    outFileType= None
    if args.output_file_type:
        outFileType = args.output_file_type

    isTransposed = False
    if args.transpose:
        isTransposed=True
        if outFileType == 'parquet' or outFileType == 'stata':
            print("Error: Parquet and Stata file types do not support transposing. Either choose a different output file type or remove the --transpose flag")
            sys.exit()
    colList=[]
    query=None
    if args.filter and len(args.filter)>1:
        parser.error("--filter appears multiple times")
    if args.columns and len(args.columns)>1:
        parser.error("--columns appears multiple times")

    if args.filter:
        query=args.filter[0]
        if not("==" in query or "!=" in query or "<" in query or ">" in query or "<=" in query or ">=" in query):
            print("Error: Filter must be an expression involving an operator such as '==' or '<'. If you simply want to include specific columns in the output, try using the --columns flag")
            sys.exit()
    if args.columns:
        colList=parseColumns(args.columns[0])
        #todo: find a way to remove duplicates in the list without reordering the list
        #colSet=set(args.columns)
        #colList=list(colSet)
    allCols=False
    if args.all_columns:
        allCols=True
    gzip=False
    if (not isGzipped(args.output_file) and args.gzip):
        print("NOTE: Because you requested the output be gzipped, it will be saved to "+args.output_file+".gz")
    if isGzipped(args.output_file) or args.gzip:
        gzip=True
    indexCol="Sample"
    if args.set_index:
        indexCol=args.set_index[0]
    try:
        ss = ShapeShifter(args.input_file, inFileType)
        ss.export_filter_results(args.output_file, outFileType, filters=query, columns=colList, transpose=isTransposed,
                                 include_all_columns=allCols, gzip_results=gzip, index=indexCol)

    except pyarrow.lib.ArrowIOError as e:
        print("Error: " + str(e))
    except pd.core.computation.ops.UndefinedVariableError as e:
        print("Error: Variable not found: " + str(e))
        print("Hint: If the variable not found is a column name, make sure it is spelled correctly. If the variable is a value, make sure it is surrounded by quotes")
    except SyntaxError as error:
        try:
            print("Error: \'" +error.text.rstrip() +"\'\n" +" "*(error.offset+6)+"^")
        except AttributeError:
            pass
        finally:
            print("Syntax is invalid. Valid python syntax must be used")
    except ValueError as e:
        print("Error: "+str(e))
    except TypeError as e:
        print("Error: Type error. You may have tried to compare items that are not comparable (strings and integers), or you may left the filter blank")
    except KeyError as e:
        print("Error: " + str(e))
    except NotImplementedError as e:
        print("Error: " + str(e))
    except RecursionError as e:
        print("Error: " + str(e))
    except ColumnNotFoundError as e:
        print("Warning: the following columns requested were not found and therefore not included in the output: " +str(e))

