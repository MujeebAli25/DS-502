import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
import pandas as pd

def PredictMastery(df, topic_cols, n_estimators=50):
    X_cols = topic_cols
    predictions = {}
    pred_rows = []

    for target in topic_cols:
        other_cols = [c for c in topic_cols if c != target]
        if len(other_cols) == 0 or df.shape[0] < 5:
            for _, row in df.iterrows():
                key = (row.get('student_id'), target)
                predictions[key] = float(row[target])
            continue

        X = df[other_cols].values
        y = df[target].values
        try:
            model = RandomForestRegressor(n_estimators=n_estimators, random_state=0)
            model.fit(X, y)
        except Exception:
            model = LinearRegression()
            model.fit(X, y)

        preds = model.predict(X)
        for i, row in df.iterrows():
            key = (row.get('student_id'), target)
            predictions[key] = float(preds[i])

    for _, row in df.iterrows():
        sid = row.get('student_id')
        sname = row.get('student_name')
        d = {'student_id': sid, 'student_name': sname}
        for t in topic_cols:
            d[f"pred_{t}"] = predictions.get((sid, t), float(row[t]))
        pred_rows.append(d)

    pred_df = pd.DataFrame(pred_rows)
    return predictions, pred_df
