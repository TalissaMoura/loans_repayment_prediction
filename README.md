Loan repayments prediction for fintech
==============================

This project aims to predict loan payments made in 2022 using transaction history data and other user loan repayments.


## How is this project organized?

1. File organization:

This project was based on the cookiecutter structure as a file organization.

  **Project Organization**
  ------------

      ├── LICENSE
      ├── Makefile           <- Makefile with commands like `make data` or `make train`
      ├── README.md          <- The top-level README for developers using this project.
      ├── data
      │   ├── external       <- Data from third party sources.
      │   ├── interim        <- Intermediate data that has been transformed.
      │   ├── processed      <- The final, canonical data sets for modeling.
      │   └── raw            <- The original, immutable data dump.
      │
      ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
      │
      ├── models             <- Trained and serialized models, model predictions, or model summaries
      │
      ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
      │                         the creator's initials, and a short `-` delimited description, e.g.
      │                         `1.0-jqp-initial-data-exploration`.
      │
      ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
      │
      ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
      │   └── figures        <- Generated graphics and figures to be used in reporting
      │
      ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
      │                         generated with `pip freeze > requirements.txt`
      │
      ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
      ├── src                <- Source code for use in this project.
      │   ├── __init__.py    <- Makes src a Python module
      │   │
      │   ├── data           <- Scripts to download or generate data
      │   │   └── make_dataset.py
      │   │
      │   ├── features       <- Scripts to turn raw data into features for modeling
      │   │   └── build_features.py
      │   │
      │   ├── models         <- Scripts to train models and then use trained models to make
      │   │   │                 predictions
      │   │   ├── predict_model.py
      │   │   └── train_model.py
      │   │
      │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
      │       └── visualize.py
      │
      └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


  --------

  <p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

2. Databases and datasets

  - Database: For this project, we used the database provied for the challenge. He has this tabels:
  
    #### Loans Table
    - **id (int)**: Unique identifier for the loan.
    - **user_id (int)**: Unique identifier for the user who has taken the loan.
    - **amount (float)**: The amount of loan disbursed.
    - **total_amount (float)**: The amount of loan, including fees.
    - **due_amount (int)**: The amount of the loan by the due date if there are no repayments during the contract period. Good to get interest rates.
    - **due_date (object)**: The date by which the loan is due.
    - **status (object)**: Current status of the loan (e.g., repaid, debt_collection, ongoing, debt_repaid).
    - **repaid**: A loan that was was paid until due.
    - **debt_collection**: A loan that was not paid until due.
    - **debt_repaid**: A loan that was not paid until due but we recovered the money somehow.
    - **cancelled**: A canceled loan.
    - **error**: Operational error.
    - **created_at (object)**: Timestamp of when the loan record was created. <u>Have it as the beginning of the loan</u>.

    #### Loan Repayments Table

    - **id (int)**: Unique identifier for the repayment record.
    - **loan_id (int)**: The ID of the loan this repayment is associated with.
    - **type (object)**: The type of repayment (e.g., autopilot, pix).
    - **amount (float)**: The amount that was repaid.
    - **status (object)**: Status of the repayment.
    - **paid**: A loan repayment that effectively happened.
    - **defaulted**: A loan repayment that didn`t come to reality.
    - **refunded**: A loan repayment that happened but was fully refunded to the user. 
    - **created_at (object)**: Timestamp of when the repayment record was created. <u>Have it as the moment of the repayment</u>.

    #### Transactions Table
    - **id (int)**: Unique identifier for the transaction.
    - **user_id (int)**: The user ID associated with the transaction.
    - **amount (float)**: Transaction amount.
    - **status (object)**: Status of the transaction.
    - **approved**: A transaction that happened.
    - **denied**: A transaction that didn't happened due to it being denied.
    - **capture_method (object)**: Method of capturing the transaction.
    - **payment_method (object)**: Payment method used (e.g., credit, debit).
    - **installments (int)**: Number of installments for the transaction.
    - **card_brand (object)**: Brand of the card used for the transaction.
    - **created_at (object)**: Timestamp of when the transaction record was created. <u>Have it as the moment the transaction happened</u>.

  - Datasets: The datasets we construct are stored in `/data/processed` and they have this names:
      - Transactions user history features: `df_transactions_history_per_user_at_loan_created`,`df_transactions_history_per_user_in_last_month`,`df_transactions_history_per_user_in_last_six_months`,`df_transactions_history_per_user_in_last_three_months`
      - Loans repayment user history features: `loans_repayment_history_features.csv`,`df_loans_repay_history_per_user_at_loan_created.csv`,`df_loans_repay_history_per_user_in_last_month.csv`,`df_loans_repay_history_per_user_in_last_six_months.csv`, `df_loans_repay_history_per_user_in_last_three_months.csv`
      - Datasets for models: `df_loans_with_loans_repays_hist_and_trans_hist_per_user.csv`,
      `df_loans_with_loans_repays_hist_and_trans_hist_per_user_cleared.csv`

3. Scripts and directories built/used
- `/database`: contains the `database.db` file that have the data provided for the challenge.
- `/notebooks/features`: In this directory we have all the notebooks that creates the transactions user history and loans repayment history features. 
- `/notebooks`: Here we have the notebooks that constructs the optmize model and baselines (`02_create_baseline_model.ipynb and ` and `03_create_optimize_model.ipynb`) and also the data analysis for the dataset we construct for training and test (`01_EDA.ipynb`) the models and evaluate the models results (`04_evaluate_model_results.ipynb`).
- `src/make_dataset.py`: The make_dataset script contains the function that joins all the features datasets and the loans table to create the final dataset to used for models.
- `src/data_cleaning.py`: The data_cleaning script contains the functions that we used to clean the dataset for models.

## Overall results

- Training and test dataset: The final clean dataset `df_loans_with_loans_repays_hist_and_trans_hist_per_user_cleared.csv` has all the transactions and loans loans repayments features for loans repaid and not repaid till the due date. To split the train and test data we select for training all the loans made from Feb/2022 till Ago/2022 and for test we have all loans made in `Sep/2022` and `Oct/2022` (for about 88% of our data is for train and 11% is for test). Also, the transactions features we used have this time spans: `at_loan_created` (in the month of loan creation), `in_last_month` (in the month before the loan creation), `in_last_three_months` (in the three months before the loan creation) and `in_last_six_months` (in the six months before the loan creation). For the loans repayment features we only used the `in_last_month`, `in_last_three_months` and `in_last_six_months` time spans. Finally, the train dataset is at `/data/processed/train_data.csv` and test dataset is at `/data/processed/test_data.csv`

- Models created: We created three models (two baseline models and one optmize model):
    - Heuristic: Apply a business rule: approves a loan if the `total_amount` request is lower than `sum_amt_transactions_in_last_month`.
    - Decision tree: Uses the features in `df_loans_with_loans_repays_hist_and_trans_hist_per_user_cleared.csv` and apply the decision tree.
    - Random forest: Uses the features in `df_loans_with_loans_repays_hist_and_trans_hist_per_user_cleared.csv` apply random forest.

- Models results:

|	    models  | weighted avg precision| weighted avg recall | weighted avg f1-score| AUC |
|---------------|-----------------------|---------------------|----------------------|-----|
|random_forest	|        0.80	        |        0.74	      |     0.76             | 0.79|
|decision_tree	|        0.73	        |        0.73	      |     0.73             | 0.5 |
|heuristic	    |        0.77	        |        0.79	      |       0              | 0.6 |

The weighted avg f1-score of the random forest was 0.76 (4% gain compared to decision tree and 1.3% loss compared to the heuristic model), precision 0.8 (4% gain compared to decision tree and 9.6 % in relation to the heuristic model), recall of 0.74 (gain of 1.3% in relation to the decision tree and decrease of 6.3% in relation to the heuristic model) and AUC of 0.79 (gain of 31.7% in relation to the heuristic model and 41% in relation to the decision tree).

Analysing the gains for each model, we have this:

|models	        |  total_gains_worst_scenario	| total_gains_real_scenario	|  pct_performance_in_worst_sce |	 pct_performance_in_real_sce |  
|---------------|-------------------------------|---------------------------|-------------------------------|--------------------------------|             
|random_forest  |	   3322200.48	            |     554812.78	            |      89.501559	            |        95.768238               |
|decision_tree  |	   2984817.64	            |     3366553.47	        |          80.412315	        |        90.696448               |
|heuristic	    |      2963438.08	            |     3355969.77	        |          79.836340	        |        90.411319               |

Considere the two scenarios this:

- Worst scenario: where all customers do not pay any of the `total_amount`. The debt amount is given by `due_amount`.
- Real scenario: where some customers pay part of the `total_amount` value. In this case, the value of interest accrued on the amounts over the months from the creation of the loan to the `due_date` is calculated based on the interest rate when the loan was created.


As we can analyze, discounting the losses, we see that the random forest model had the greatest total gain when compared to the model with decision tree and heuristic. Considering the worst case scenario, the random forest model had 11.3% more gain than the decision tree and 12.1% more than the heuristic model, whereas in the real case the random forest model had 5.6% more gain than the decision tree and 5.9% more than the heuristic model.

Also, this information confirms what we saw in the chart comparing the ratios above, the random forest it's the model that we least lose gains. This means that we can preserve in worst scenario 89.5% of the gains obtained and about 95.8% in the real scenario.

For a more detailed analysis see the `reports/report.md` file.

## How to run this project?
- The project itself was based on venv conda. To generate this environment locally, simply run `make create_environment`. If this is not possible, use the file `requirements.txt` and run the command `pip install -r requirements.txt`

- For generate the features datasets run the notebooks in the `notebooks/features` folder. They will be
saved in `data/processed`.

- If you want to create the training dataset locally run: `make data` for non conda venvs and for conda venvs
use `cd src/data` and `python make_dataset.py ../../data/database ../../data/processed  ../../data/processed`

