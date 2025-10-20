# data_loader.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


# Reads student scores from CSV .
# Cleans and normalizes data: fills missing values, scales scores to 0-100 if needed.
# Returns tuple: (cleaned_df, topic_columns)

def LoadData(path_or_df="students.csv", from_df=False, id_col='student_id', name_col='student_name'):
    if from_df and isinstance(path_or_df, pd.DataFrame):
        df = path_or_df.copy()
    else:
        df = pd.read_csv(path_or_df)

    # Standardize column names
    df.columns = [c.strip() for c in df.columns]

    # Identify topic columns: assume id/name are present, others are topics
    reserved = {id_col, name_col}
    topic_cols = [c for c in df.columns if c not in reserved]

    # If scores are in 0-1, convert to 0-100 (heuristic)
    # Check max value among scores
    if df[topic_cols].max().max() <= 1.01:
        df[topic_cols] = df[topic_cols] * 100

    # Fill missing scores: use per-student mean or per-topic mean as fallback
    df[topic_cols] = df[topic_cols].apply(pd.to_numeric, errors='coerce')
    df[topic_cols] = df[topic_cols].apply(lambda col: col.fillna(col.mean()), axis=0)
    df[topic_cols] = df[topic_cols].apply(lambda row: row.fillna(row.mean()), axis=1)

    # Clip to 0-100
    df[topic_cols] = df[topic_cols].clip(lower=0, upper=100)

    # Add normalized version for ML algorithms
    scaler = StandardScaler()
    normalized = scaler.fit_transform(df[topic_cols])
    norm_df = pd.DataFrame(normalized, columns=[f"{c}_norm" for c in topic_cols], index=df.index)
    out_df = pd.concat([df.reset_index(drop=True), norm_df.reset_index(drop=True)], axis=1)

    return out_df, topic_cols
