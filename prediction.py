import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression


# Predict next mastery(how well a student has mastered a topic) for each student-topic.
# Strategy:
# - Use per-topic model: train model on students using their other topic scores as features
# to predict the target topic score. This is a simple multi-feature approach and works
# when there are many students.
# - If there are too few students, fallback to a simple rule: predicted = current_score.
# Returns a dictionary: predictions[(student_id, topic)] = predicted_score
# and a DataFrame with predictions per student row.


def PredictMastery(df, topic_cols, n_estimators=50):
    X_cols = topic_cols
    predictions = {}
    pred_rows = []

    # For each topic, train a model to predict that topic from other topics
    for target in topic_cols:
        other_cols = [c for c in topic_cols if c != target]
        if len(other_cols) == 0 or df.shape[0] < 5:
            # too few features or examples; fallback: predicted = current score
            for _, row in df.iterrows():
                key = (row.get('student_id'), target)
                predictions[key] = float(row[target])
            continue

        X = df[other_cols].values
        y = df[target].values
        # use random forest for non-linear relationships; fallback to linear if fails
        try:
            model = RandomForestRegressor(n_estimators=n_estimators, random_state=0)
            model.fit(X, y)
        except Exception:
            model = LinearRegression()
            model.fit(X, y)

        # make predictions for each student
        preds = model.predict(X)
        for i, row in df.iterrows():
            key = (row.get('student_id'), target)
            predictions[key] = float(preds[i])

    # aggregate into DataFrame
    for _, row in df.iterrows():
        sid = row.get('student_id')
        sname = row.get('student_name')
        d = {'student_id': sid, 'student_name': sname}
        for t in topic_cols:
            d[f"pred_{t}"] = predictions.get((sid, t), float(row[t]))
        pred_rows.append(d)

    import pandas as pd
    pred_df = pd.DataFrame(pred_rows)
    return predictions, pred_df
