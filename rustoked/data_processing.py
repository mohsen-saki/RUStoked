from glob import glob
from pathlib import Path
import sys
sys.path.append("..")
import pandas as pd

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

    if drop_columns:
        df.drop([], axis=1, inplace=True)