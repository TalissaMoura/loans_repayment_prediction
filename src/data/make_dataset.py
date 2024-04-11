# -*- coding: utf-8 -*-
import logging
from pathlib import Path
from typing import Union

import click
import numpy as np
import pandas as pd
import sqlalchemy
from datetime import date

# define columns to select 

USER_TRANS_HIST_AT_CREATED_LOAN = [
       'user_id',
       'created_at', 
       'date_created',
       'sum_amt_transactions_at_created_loan',
       'sum_amt_payment_method_credit_at_created_loan',
       'sum_amt_payment_method_debit_at_created_loan',
       'sum_amt_transactions_in_visa_at_created_loan',
       'sum_amt_transactions_in_mastercard_at_created_loan',
       'sum_amt_transactions_in_elo_at_created_loan',
       'sum_amt_transactions_in_hipercard_at_created_loan',
       'sum_amt_transactions_in_amex_at_created_loan',
       'max_amt_transactions_at_created_loan',
       'max_installments_at_created_loan',
       'median_installments_at_created_loan',
       'most_frequent_transactions_payment_method_at_created_loan'
]
USER_TRANS_HIST_IN_LAST_MONTH = [
       'user_id', 
       'created_at', 
       'date_created',
       'sum_amt_transactions_in_last_month',
       'sum_amt_payment_method_credit_in_last_month',
       'sum_amt_payment_method_debit_in_last_month',
       'sum_amt_transactions_in_visa_in_last_month',
       'sum_amt_transactions_in_mastercard_in_last_month',
       'sum_amt_transactions_in_elo_in_last_month',
       'sum_amt_transactions_in_hipercard_in_last_month',
       'sum_amt_transactions_in_amex_in_last_month',
       'max_amt_transactions_in_last_month', 'max_installments_in_last_month',
       'median_installments_in_last_month',
       'most_frequent_transactions_payment_method_in_last_month'
]
USER_TRANS_HIST_IN_LAST_THREE_MONTHS = [
       'user_id', 
       'created_at', 
       'date_created', 
       'avg_amt_transactions_in_last_three_months',
       'avg_amt_payment_method_credit_in_last_three_months',
       'avg_amt_payment_method_debit_in_last_three_months',
       'avg_amt_transactions_in_visa_in_last_three_months',
       'avg_amt_transactions_in_mastercard_in_last_three_months',
       'avg_amt_transactions_in_elo_in_last_three_months',
       'avg_amt_transactions_in_hipercard_in_last_three_months',
       'avg_amt_transactions_in_amex_in_last_three_months',
       'max_amt_transactions_in_last_three_months',
       'max_installments_in_last_three_months',
       'median_installments_in_last_three_months',
       'most_frequent_transactions_payment_method_in_last_three_months'
]
USER_TRANS_HIST_IN_LAST_SIX_MONTHS = [
       'user_id', 
       'created_at', 
       'date_created',
       'avg_amt_transactions_in_last_six_months',
       'avg_amt_payment_method_credit_in_last_six_months',
       'avg_amt_payment_method_debit_in_last_six_months',
       'avg_amt_transactions_in_visa_in_last_six_months',
       'avg_amt_transactions_in_mastercard_in_last_six_months',
       'avg_amt_transactions_in_elo_in_last_six_months',
       'avg_amt_transactions_in_hipercard_in_last_six_months',
       'avg_amt_transactions_in_amex_in_last_six_months',
       'max_amt_transactions_in_last_six_months',
       'max_installments_in_last_six_months',
       'median_installments_in_last_six_months',
       'most_frequent_transactions_payment_method_in_last_six_months'
]
USER_LOANS_REPAYS_HIST_IN_LAST_MONTH = [
       'user_id', 
       'created_at',
       'date_created',
       'avg_repaid_total_amt_loans_in_last_month',
       'avg_pct_repaid_first_month_loans_in_last_month',
       'avg_pct_repaid_sec_month_loans_in_last_month',
       'avg_pct_repaid_trd_month_loans_in_last_month',
       'max_repaid_total_amt_loans_in_last_month',
       'most_frequent_loans_repayment_method_in_last_month',
       'pct_repaid_loans_in_last_month'
]
USER_LOANS_REPAYS_HIST_IN_LAST_THREE_MONTHS = [
       'user_id', 
       'created_at', 
       'date_created',
       'avg_repaid_total_amt_loans_in_last_three_months',
       'avg_pct_repaid_first_month_loans_in_last_three_months',
       'avg_pct_repaid_sec_month_loans_in_last_three_months',
       'avg_pct_repaid_trd_month_loans_in_last_three_months',
       'max_repaid_total_amt_loans_in_last_three_months',
       'most_frequent_loans_repayment_method_in_last_three_months',
       'pct_repaid_loans_in_last_three_months'
]
USER_LOANS_REPAYS_HIST_IN_LAST_SIX_MONTHS = [
       'user_id', 
       'created_at',
       'date_created',
       'avg_repaid_total_amt_loans_in_last_six_months',
       'avg_pct_repaid_first_month_loans_in_last_six_months',
       'avg_pct_repaid_sec_month_loans_in_last_six_months',
       'avg_pct_repaid_trd_month_loans_in_last_six_months',
       'max_repaid_total_amt_loans_in_last_six_months',
       'most_frequent_loans_repayment_method_in_last_six_months',
       'pct_repaid_loans_in_last_six_months'
]

@click.command()
@click.argument("database_filepath",type=click.Path())
@click.argument("tables_filepath",type=click.Path())
@click.argument("output_filepath", type=click.Path())
def main(database_filepath,tables_filepath,output_filepath):
    """Runs data processing scripts to turn raw data from (../raw) into
    cleaned data ready to be analyzed (saved in ../processed).
    """
    output_path = Path(output_filepath)
    database_path = Path(database_filepath)
    tables_path = Path(tables_filepath)
    logger = logging.getLogger(__name__)
    logger.info("making final data set from raw data")

    ## read tables
    engine = sqlalchemy.create_engine(f"sqlite:///{database_path}/database.db", echo=True)

    df_loans = pd.read_sql(
       sql="""
       SELECT * FROM loans l
       """,
       con=engine
       )

    df_loans_trans_hist_at_created_loan = pd.read_csv(f"{tables_path}/df_transactions_history_per_user_at_loan_created.csv")
    df_loans_trans_hist_in_last_month = pd.read_csv(f"{tables_path}/df_transactions_history_per_user_in_last_month.csv")
    df_loans_trans_hist_in_last_three_mths = pd.read_csv(f"{tables_path}/df_transactions_history_per_user_in_last_three_months.csv")
    df_loans_trans_hist_in_last_six_mths = pd.read_csv(f"{tables_path}/df_transactions_history_per_user_in_last_six_months.csv")
    df_loans_repays_hist_in_last_month = pd.read_csv(f"{tables_path}/df_loans_repay_history_per_user_in_last_month.csv")
    df_loans_repays_hist_in_last_three_mths = pd.read_csv(f"{tables_path}/df_loans_repay_history_per_user_in_last_three_months.csv")
    df_loans_repays_hist_in_last_six_mths = pd.read_csv(f"{tables_path}/df_loans_repay_history_per_user_in_last_six_months.csv")

    ## preprocessing

    #convert to datetime
    df_loans["created_at"] = pd.to_datetime(df_loans["created_at"],utc=True,format="ISO8601")
    df_loans_repays_hist_in_last_month["created_at"] = pd.to_datetime(df_loans_repays_hist_in_last_month["created_at"],utc=True,format="ISO8601")
    df_loans_repays_hist_in_last_three_mths["created_at"] = pd.to_datetime(df_loans_repays_hist_in_last_three_mths["created_at"],utc=True,format="ISO8601")
    df_loans_repays_hist_in_last_six_mths["created_at"] = pd.to_datetime(df_loans_repays_hist_in_last_six_mths["created_at"],utc=True,format="ISO8601")
    df_loans_trans_hist_at_created_loan["created_at"] = pd.to_datetime(df_loans_trans_hist_at_created_loan["created_at"],utc=True,format="ISO8601")
    df_loans_trans_hist_in_last_month["created_at"] = pd.to_datetime(df_loans_trans_hist_in_last_month["created_at"],utc=True,format="ISO8601")
    df_loans_trans_hist_in_last_three_mths["created_at"] = pd.to_datetime(df_loans_trans_hist_in_last_three_mths["created_at"],utc=True,format="ISO8601")
    df_loans_trans_hist_in_last_six_mths["created_at"] = pd.to_datetime(df_loans_trans_hist_in_last_six_mths["created_at"],utc=True,format="ISO8601")

    #convert to date
    df_loans["due_date"] = pd.to_datetime(df_loans["due_date"],format="%Y-%m-%d")
    df_loans_repays_hist_in_last_month["due_date"] = pd.to_datetime(df_loans_repays_hist_in_last_month["due_date"],format="%Y-%m-%d")
    df_loans_repays_hist_in_last_three_mths["due_date"] = pd.to_datetime(df_loans_repays_hist_in_last_three_mths["due_date"],format="%Y-%m-%d")
    df_loans_repays_hist_in_last_six_mths["due_date"] = pd.to_datetime(df_loans_repays_hist_in_last_six_mths["due_date"],format="%Y-%m-%d")
    df_loans_trans_hist_at_created_loan["due_date"] = pd.to_datetime(df_loans_trans_hist_at_created_loan["due_date"],format="%Y-%m-%d")
    df_loans_trans_hist_in_last_month["due_date"] = pd.to_datetime(df_loans_trans_hist_in_last_month["due_date"],format="%Y-%m-%d")
    df_loans_trans_hist_in_last_three_mths["due_date"] = pd.to_datetime(df_loans_trans_hist_in_last_three_mths["due_date"],format="%Y-%m-%d")
    df_loans_trans_hist_in_last_six_mths["due_date"] = pd.to_datetime(df_loans_trans_hist_in_last_six_mths["due_date"],format="%Y-%m-%d")

       #create date_created 
    df_loans["date_created"] = df_loans["created_at"].apply(func=lambda d:d.date())
    df_loans_repays_hist_in_last_month["date_created"] = df_loans_repays_hist_in_last_month["created_at"].apply(func=lambda d:d.date())
    df_loans_repays_hist_in_last_three_mths["date_created"] = df_loans_repays_hist_in_last_three_mths["created_at"].apply(func=lambda d:d.date())
    df_loans_repays_hist_in_last_six_mths["date_created"] = df_loans_repays_hist_in_last_six_mths["created_at"].apply(func=lambda d:d.date())
    df_loans_trans_hist_at_created_loan["date_created"] = df_loans_trans_hist_at_created_loan["created_at"].apply(func=lambda d:d.date())
    df_loans_trans_hist_in_last_month["date_created"] = df_loans_trans_hist_in_last_month["created_at"].apply(func=lambda d:d.date())
    df_loans_trans_hist_in_last_three_mths["date_created"] = df_loans_trans_hist_in_last_three_mths["created_at"].apply(func=lambda d:d.date())
    df_loans_trans_hist_in_last_six_mths["date_created"] = df_loans_trans_hist_in_last_six_mths["created_at"].apply(func=lambda d:d.date())

    # add reference_date in df_loans
    df_loans["reference_date"] = [date(year=d.year,month=d.month,day=1)
                                   for d in df_loans["date_created"]]

    df_res = df_loans.merge(
        right=df_loans_trans_hist_at_created_loan[USER_TRANS_HIST_AT_CREATED_LOAN].set_index(["user_id","date_created","created_at"]),
        right_index=True,
        left_on = ["user_id","date_created","created_at"],
        how="inner"
        )\
        .merge(
        right=df_loans_trans_hist_in_last_month[USER_TRANS_HIST_IN_LAST_MONTH].set_index(["user_id","date_created","created_at"]),
        right_index=True,
        left_on = ["user_id","date_created","created_at"],
        how="inner"
        )\
        .merge(
        right=df_loans_trans_hist_in_last_three_mths[USER_TRANS_HIST_IN_LAST_THREE_MONTHS].set_index(["user_id","date_created","created_at"]),
        right_index=True,
        left_on = ["user_id","date_created","created_at"],
        how="inner"
        )\
        .merge(
        right=df_loans_trans_hist_in_last_six_mths[USER_TRANS_HIST_IN_LAST_SIX_MONTHS].set_index(["user_id","date_created","created_at"]),
        right_index=True,
        left_on = ["user_id","date_created","created_at"],
        how="inner"
        )\
        .merge(
        right=df_loans_repays_hist_in_last_month[USER_LOANS_REPAYS_HIST_IN_LAST_MONTH].set_index(["user_id","date_created","created_at"]),
        right_index=True,
        left_on = ["user_id","date_created","created_at"],
        how="inner"
        )\
        .merge(
        right=df_loans_repays_hist_in_last_three_mths[USER_LOANS_REPAYS_HIST_IN_LAST_THREE_MONTHS].set_index(["user_id","date_created","created_at"]),
        right_index=True,
        left_on = ["user_id","date_created","created_at"],
        how="inner"
        )\
        .merge(
        right=df_loans_repays_hist_in_last_six_mths[USER_LOANS_REPAYS_HIST_IN_LAST_SIX_MONTHS].set_index(["user_id","date_created","created_at"]),
        right_index=True,
        left_on=["user_id","date_created","created_at"],
        how="inner"
        )
    df_res.to_csv(output_path / "df_loans_with_loans_repays_hist_and_trans_hist_per_user2.csv", index=False)


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    main()
