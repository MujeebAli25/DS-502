import pandas as pd

def TrackStudentProgress(df, topic_cols, threshold=70):
    students = []
    rows = []

    for _, row in df.iterrows():
        student_id = row.get('student_id', None)
        student_name = row.get('student_name', None)
        weak = []
        scores = {}
        for t in topic_cols:
            score = float(row[t])
            scores[t] = score
            if score < threshold:
                weak.append(t)

        mastery_percent = 100 * (len(topic_cols) - len(weak)) / len(topic_cols)
        risk_score = 100 - mastery_percent 

        students.append({
            'student_id': student_id,
            'student_name': student_name,
            'weak_topics': weak,
            'scores': scores,
            'mastery_percent': mastery_percent,
            'risk_score': risk_score
        })

        rows.append({
            'student_id': student_id,
            'student_name': student_name,
            'weak_topics': ','.join(weak),
            'mastery_percent': mastery_percent,
            'risk_score': risk_score,
            **{f"score_{t}": scores[t] for t in topic_cols}
        })

    progress_df = pd.DataFrame(rows)
    return students, progress_df
