from glob import glob
from pathlib import Path
import sys
sys.path.append("..")
import pandas as pd
import numpy as np

def load_raw_data(save_path=None):
    """
    read multiple csv files and concat as a dataframe
    :param save_path: path to save data frame as a all data csv file
    :return: pandas DataFrame and save it as csv file if path given
    """

    df = pd.concat([pd.read_csv(file) for file in glob("../data/scraped_data/*.csv")],
        ignore_index=True)

    if save_path:
        df.to_csv(Path(save_path), index=False)
    return df


def clean_raw_dataframe(df, drop_columns=False):
    """
    cleanup and format initial DataFrame
    :param df: raw DataFrame
    :return: Processed DataFrame 
    """

    # concat `title`, `pros`, and `cons` as body of each review
    df['reviews'] = df['title'].str.cat(df['pros'].str.cat(df['cons'], sep=" ", na_rep=""), sep=" ", na_rep="")
    df.drop(['title', 'pros', 'cons'], axis=1, inplace=True)

    # handling missing data
    df['job_title'] = df['job_title'].fillna('unknown')
    df['location'] = df['location'].fillna('Australia')

    # casting right type to column
    df['career_opportunity_rating'] = df['career_opportunity_rating'].astype(int)
    df['work_life_balance_rating'] = df['work_life_balance_rating'].astype(int)
    df['work_env_rating'] = df['work_env_rating'].astype(int)
    df['management_rating'] = df['management_rating'].astype(int)
    df['benefits_rating'] = df['benefits_rating'].astype(int)
    df['diversity_rating'] = df['diversity_rating'].astype(int)
    df['overall_rating'] = df['overall_rating'].astype(int)

    # cleaning 'recommendation' & 'salary' columns
    df['recommendation'] = df['recommendation'].str.split().str[-1]
    df['salary'] = df['salary'].str.split().str[-1]

    # new column for overal rating calculated based on employee ratings
    df["calculated_rating"] = df[["career_opportunity_rating", "work_life_balance_rating",
                              "work_env_rating", "management_rating", "benefits_rating",
                              "diversity_rating"]].mean(axis=1).round()

    # removing those reviews with two points difference between overall and calculated rating
    df = df[~(abs(df['overall_rating'] - df['calculated_rating']) > 1)]

    # mapping ratings to three different category labels
    df["labels"] = [get_labels(rating) for rating in df["overall_rating"]]

    # Adding review text length as a new feature
    df["review_len"] = df["reviews"].str.len()

    if drop_columns:
        df.drop(drop_columns, axis=1, inplace=True)

    return df



def get_labels(rating):
    """
    map each reating to a label category used by clean_raw_dataframe() function
    :rating: overal rating given by employee
    "return: data labels
    """
    if rating in [1, 2]:
        return 0
    elif rating == 3:
        return 1
    else:
        return 2


def get_normalized_series(df, col):
    """
    get a normalized version of selcted column/series
    :param df: pandas dataframe
    :param col: column name
    :return: normalized series using Z-score
    """
    return (df[col] - df[col].mean()) / df[col].std()


def get_features(df):
    """
    get the features for model development
    :param df: pandas dataframe
    :return: dataframe updated with features
    """
    # creat a new column with review length normalized
    df["norm_review_len"] = get_normalized_series(df, "review_len")

    # creating new columns each containing if targeted word is in the review or not
    df["has_positive"] = (
        df["reviews"].str.lower().str.contains("great", regex=False) |
        df["reviews"].str.lower().str.contains("good", regex=False)
    )

    df["has_but"] = df["reviews"].str.lower().str.contains("but", regex=False)

    df["has_negative"] = (
        df["reviews"].str.lower().str.contains("bad", regex=False) |
        df["reviews"].str.lower().str.contains("poor", regex=False) |
        df["reviews"].str.lower().str.contains("not", regex=False) |
        df["reviews"].str.lower().str.contains("no", regex=False) |
        df["reviews"].str.lower().str.contains("n't", regex=False)
    )

    # creating new columns each containing number of occurrences for each targeted 
    # word is in the review and total sum of all as a weight factor.
    df["great_count"] = df["reviews"].str.lower().str.count("great")
    df["good_count"] = df["reviews"].str.lower().str.count("good")

    df["bad_count"] = -df["reviews"].str.lower().str.count("bad")
    df["poor_count"] = -df["reviews"].str.lower().str.count("poor")
    df["not_count"] = -df["reviews"].str.lower().str.count("not")
    df["no_count"] = -df["reviews"].str.lower().str.count("no")
    df["n't_count"] = -df["reviews"].str.lower().str.count("n't")

    # total sum based on their content tendency as positive(+) or negative(-)
    df["pos_neg_factor"] = df[["great_count", "good_count", 
                                        "bad_count", "poor_count", "not_count", 
                                        "no_count", "n't_count"]].sum(axis=1)

    # get the normalized weight factor
    df["norm_factor"] = get_normalized_series(df, "pos_neg_factor")

    return df