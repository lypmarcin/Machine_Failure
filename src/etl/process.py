# IMPORTS
# Directory and file
import os
from os.path import dirname

# General
import pandas as pd


# OPTIONAL FEATURE ENGINEERING - FUNCTIONS
# add temperature difference between surrounding and the part.
# use - to easily turn on and off the function (True to use the function)
# keep_original - keep in df the columns the new feature is coming from (True to keep)
def add_temp_difference(df_, use=True, keep_original=True):
    if not use:
        pass
    else:
        df_["Temp difference"] = df["Process temperature [K]"] - df["Air temperature [K]"]

        if not keep_original:
            df_.drop(["Process temperature [K]", "Air temperature [K]"], inplace=True, axis=1)

    return df_


def add_power(df_, use=True, keep_original=True):
    if not use:
        pass
    else:
        df_["Power"] = df_["Torque [Nm]"] * df_["Rotational speed [rpm]"]

        if not keep_original:
            df_.drop(["Torque [Nm]", "Rotational speed [rpm]"], inplace=True, axis=1)

    return df_


# IMPORTING THE DATA
INPUT_FILE_NAME = "machine_failure.csv"
# Path to main directory
path_main = dirname(dirname(os.getcwd()))

# Path to input data
path_input = os.path.join(path_main, "data", "input", INPUT_FILE_NAME)

# import to data frame
df = pd.read_csv(path_input)

# MUST_HAVE CHANGES TO DATA
# drop not-needed columns
COL_TO_DROP = ['TWF', 'HDF', 'PWF', 'OSF', 'RNF', "UDI", "Product ID"]
df.drop(COL_TO_DROP, inplace=True, axis=1)

# map "Type"
DICTIONARY = {"L": 0, "M": 1, "H": 2}
df["Type"] = df["Type"].map(DICTIONARY)

# move target to first column
TARGET_ORIGINAL_NAME = "Machine failure"
target_column = df.pop(TARGET_ORIGINAL_NAME)
df.insert(0, TARGET_ORIGINAL_NAME, target_column)

# OPTIONAL CHANGES TO DATA only boolean can be changed
df = add_temp_difference(df, use=True, keep_original=False)
df = add_power(df, use=True, keep_original=True)

# SAVING THE DATA
# Path to processed data
PROCESSED_FILE_NAME = "machine_failure_processed.csv"
path_processed = os.path.join(path_main, "data", "processed", PROCESSED_FILE_NAME)

# saving
df.to_csv(path_processed)
