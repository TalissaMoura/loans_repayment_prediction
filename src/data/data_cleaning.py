# -*- coding: utf-8 -*-
import logging
from pathlib import Path
from typing import Union

import click
import numpy as np
import pandas as pd
import datetime as dt



def drop_null_cols_by_threshold(dataframe: pd.DataFrame, threshold:Union[None,float]) -> pd.DataFrame:
    """
    Remove columns from DataFrame that have a percentage of null values bigger than a threshold.

    Args:
        dataframe (pd.DataFrame): Input DataFrame to drop columns.
        threshold (Union[str, list]): A float value between 0.0 and 1.0.

    Returns:
        pd.DataFrame: a new DataFrame with dropped columns.
    """
    new_df = dataframe.copy()
    drop_cols = new_df.columns[(new_df.isnull().sum()/new_df.shape[0])>threshold]
    new_df = new_df.drop(columns=drop_cols)
    return new_df

def change_categories(dataframe:pd.DataFrame,
                     col_to_search_categories:str,
                     old_categories:Union[str,list],
                     new_category:str)-> pd.DataFrame:
    """
    Changes categories in a column. Make a category or categories being of 
    a new category. 
    Args:
        dataframe (pd.DataFrame): Initial dataframe to apply the changes in categories.
        col_to_search_categories (str): Column to search all categorical values.
        old_categories (Union[str,list]): A value (if str) or values (if list) that is/are going to be 
        replace to a new value.
        new_category (str): The new value to input in the old categories values.

    Returns:
        pd.DataFrame: Final dataframe with new category/categories applied to
        the column defined in col_to_search_categories.
    """    
    new_df = dataframe.copy()
    if len(old_categories)>0.0:
        new_df.loc[:,col_to_search_categories] = new_df[col_to_search_categories].map(lambda d: new_category if d in old_categories else d)
    else:
        new_df.loc[:,col_to_search_categories] = new_df[col_to_search_categories].map(lambda d: new_category
                                                                                 if d==old_categories else d)
    return new_df

def convert_to_datetime(
        dataframe:pd.DataFrame,
        col_to_convert:str,
        fmt:str
)->pd.DataFrame:
    """
    Convert a column to datetime with a specific format.

    Args:
        dataframe (pd.DataFrame): Initial dataframe to create new datetime columns
        fmt (str): A format to applied in the datetime column.
    Returns:
        pd.DataFrame: Final dataframe with a new datetime column.
    """    
    new_df = dataframe.copy()
    new_df.loc[:,col_to_convert] = pd.to_datetime(dataframe[col_to_convert],format=fmt)
    return new_df

def convert_to_date(
        dataframe:pd.DataFrame,
        col_to_convert:str,
        fmt:str
)->pd.DataFrame:
    """
    Convert a column to datetime with a specific format.

    Args:
        dataframe (pd.DataFrame): Initial dataframe to create new datetime columns
        fmt (str): A format to applied in the date column.
    Returns:
        pd.DataFrame: Final dataframe with a new datetime column only with date values.
    """    
    new_df = dataframe.copy()
    new_df.loc[:,col_to_convert] = [dt.datetime.strptime(d,fmt).date() for d in dataframe[col_to_convert]]
    return new_df

def convert_int_to_float(
        dataframe:pd.DataFrame,
        col_to_convert:str,
        num_to_divide:Union[int,float,None]=None
)->pd.DataFrame:
    """
    Convert a int32 column to float64 column. Also, can change 
    a value by making a division with a number specified in 
    num_to_divide.

    Args:
        dataframe (pd.DataFrame): Initial dataframe to make the conversions.
        col_to_convert (str): The column to convert from int64 to float64.
        num_to_divide (Union[int,float,None], optional): A number to divide the int values
        in the column to convert. Defaults to None. It's useful to remove zeros after a value.

    Returns:
        pd.DataFrame: A new dataframe with float64 columns.
    """    
    new_df = dataframe.copy()
    new_df.loc[:,col_to_convert] = new_df[col_to_convert].astype("float64")
    if num_to_divide:
        new_df.loc[:,col_to_convert] = new_df[col_to_convert]/num_to_divide
    return new_df

def adjust_minmax_pct_cols(
        dataframe:pd.DataFrame,
        pct_col_to_adjust:Union[str,list]
)->pd.DataFrame:
    """
    Adjust percentage values that are close or bigger than 0.99 to be equal to 1.0 and
    and values that are below 0.0 to be equal to 0.0.

    Args:
        dataframe (pd.DataFrame): Initial dataframe to applied the changes in percentage columns.
        pct_col_to_adjust (Union[str,list]): Percentage columns with values to be converted to 1.0.

    Returns:
        pd.DataFrame: A new dataframe with percentage columns with values between 0.0 and 1.0
    """    
    new_df = dataframe.copy()
    new_df.loc[:,pct_col_to_adjust] = new_df[pct_col_to_adjust].map(lambda d: 1.0 if d >= 0.99 else d)
    new_df.loc[:,pct_col_to_adjust] = new_df[pct_col_to_adjust].map(lambda d: 0.0 if d < 0.0 else d)
    return new_df

def round_columns(
        dataframe:pd.DataFrame,
        columns_to_round:Union[str,list],
        decimals:int
        )->pd.DataFrame:
    """
    Round float columns to a given number of decimal places.

    Args:
        dataframe (pd.DataFrame): Initial dataframe to round values.
        columns_to_round (Union[str,list]): Float columns to be rounded.
        decimals (int): Number of decimal places to round to. 
    Returns:
        pd.DataFrame: A new dataframe with all float columns rounded.
    """    
    new_df = dataframe.copy()
    new_df.loc[:,columns_to_round] = new_df[columns_to_round].apply(func=lambda d: np.round(d,decimals),axis=1)
    return new_df

def calculate_interest_rate(
        dataframe:pd.DataFrame
)-> pd.DataFrame:
    """
    Calcultes the month and interest rate of a loan in the time
    that was created.

    Args:
        dataframe (pd.DataFrame): Initial dataframe with due_date and 
        created_at columns.

    Returns:
        pd.DataFrame: Final dataframe with new columns: "annual_interest_rate","monthly_interest_rate'
        and "time_years".
    """    
    new_df = dataframe.copy()
    # Calculate time in years
    new_df['time_years'] = [
   (date_created - created_at.date()).days/365 for date_created,created_at in new_df[["due_date","created_at"]].values
   ]
    # Calculate annual interest rate
    new_df['annual_interest_rate'] = ((new_df['due_amount'] / new_df['total_amount']) ** (1 / new_df['time_years']) - 1) * 100
    # Calculate monthly interest rate
    new_df['monthly_interest_rate'] = ((1 + new_df['annual_interest_rate'] / 100) ** (1 / 12) - 1) * 100
    return new_df


def add_to_pipe(
    dataframe: pd.DataFrame, func: callable, *args, **kwargs
) -> pd.DataFrame.pipe:
    """
    Add a function to be applied on dataframe to a pipeline using
    the Pandas.DataFrame.pipe function.

    Args:
        dataframe (pd.DataFrame): Input DataFrame to apply the function to
        func (callable): A function be applied on dataframe.
        *args: Positional arguments to apply on function.
        **kwargs: Keyword arguments to apply on function.

    Returns:
        pd.DataFrame.pipe: a pipeline with function to apply on input dataframe
    """
    return dataframe.pipe(func, *args, **kwargs)


def make_pipeline(dataframe: pd.DataFrame, functions: list[dict]) -> pd.DataFrame:
    """
    Apply functions to a dataframe. Useful to apply chainable functions that expect DataFrames.

    Args:
        dataframe (pd.DataFrame): Input data to apply changes.
        functions (list): List of dict with functions to apply on input dataframe.
        The dicts have this pattern:
        {"function":func,"function_kwargs":{"keyword_1":value},"function_args":[value1,value2]}
        The dict must have a function but function_kwargs and function_args can be optional.
        If function_kwargs in dict its value must be a dict and if function_args in
        dict then its must be a iterable.

    Returns:
        pd.DataFrame: A new DataFrame with all the functions listed applied on input dataframe
    """

    new_df = dataframe.copy()
    for f in functions:
        if "function_args" in f.keys() and "function_kwargs" in f.keys():
            try:
                new_df = add_to_pipe(
                    new_df,
                    *f["function_args"],
                    func=f["function"],
                    **f["function_kwargs"],
                )
            except TypeError:
                print(
                    "function_args must be a iterable and function_kwargs must be a dict."
                )
        elif "function_kwargs" in f.keys() and "function_args" not in f.keys():
            try:
                new_df = add_to_pipe(new_df, func=f["function"], **f["function_kwargs"])
            except TypeError:
                raise Exception(f"function_kwargs must be a dict")
        elif "function_args" in f.keys() and "function_kwargs" not in f.keys():
            try:
                new_df = add_to_pipe(new_df, *f["function_args"], func=f["function"])
            except TypeError:
                raise Exception(f"function must be a iterable")
        else:
            try:
                new_df = add_to_pipe(new_df, func=f["function"])
            except TypeError:
                raise Exception(f"function must be a callable")
            except KeyError:
                raise Exception(f"function must be a key on dict.")
    return new_df


@click.command()
@click.argument("input_filepath", type=click.Path(exists=True))
@click.argument("output_filepath", type=click.Path())
def main(input_filepath, output_filepath):
    """Runs data processing scripts to turn raw data from (../raw) into
    cleaned data ready to be analyzed (saved in ../processed).
    """
    input_path = Path(input_filepath)
    output_path = Path(output_filepath)
    logger = logging.getLogger(__name__)
    logger.info("making final data set from raw data")
    raw_df = pd.read_csv(input_path / "df_loans_with_loans_repays_hist_and_trans_hist_per_user.csv")
    raw_df_cols = raw_df.columns.to_list()
    pct_cols = [d for d in raw_df_cols if d.__contains__("avg_pct")]

    list_funcs = [
    {"function":drop_null_cols_by_threshold,
     "function_kwargs":{"threshold":0.8}
     },
    {"function": convert_to_datetime, "function_kwargs": {
        "col_to_convert":"created_at",
        "fmt":"ISO8601"
    }},
    {"function": convert_to_date, "function_kwargs": {
        "col_to_convert":"due_date",
        "fmt":"%Y-%m-%d"
    }},
    {"function": convert_to_date, "function_kwargs": {
        "col_to_convert":"date_created",
        "fmt":"%Y-%m-%d"
    }},
    {"function": convert_to_date, "function_kwargs": {
        "col_to_convert":"reference_date",
        "fmt":"%Y-%m-%d"
    }},
    {"function": convert_int_to_float, 
     "function_kwargs": {
        "col_to_convert":"due_amount",
        "num_to_divide":1000000.0
    }},
    {"function": adjust_minmax_pct_cols, 
     "function_kwargs": {
        "pct_col_to_adjust":pct_cols
    }},
    {"function": calculate_interest_rate
     },
     {"function":change_categories,
      "function_kwargs":{
              "col_to_search_categories":"status",
              "old_categories":["debt_repaid","debt_collection"],
              "new_category":"debt"
          }
      }
    ]

    clean_df = make_pipeline(dataframe=raw_df,functions=list_funcs)
    all_float_cols = [col for col in clean_df.columns if clean_df[col].dtype == "float64"]
    final_df = make_pipeline(dataframe=clean_df, \
                             functions=[
                                 {"function":round_columns,
                                  "function_kwargs":{"columns_to_round":all_float_cols,"decimals":2}}
                             ])

    final_df.to_csv(output_path / "df_loans_with_loans_repays_hist_and_trans_hist_per_user_cleared.csv", index=False)


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    main()
