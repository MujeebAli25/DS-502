# Determine the weak topics for each student
# Returns a list-of-dicts for each student and a DataFrame summarizing weak topics.

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
        students.append({
            'student_id': student_id,
            'student_name': student_name,
            'weak_topics': weak,
            'scores': scores
        })
        rows.append({
            'student_id': student_id,
            'student_name': student_name,
            'weak_topics': ','.join(weak),
            **{f"score_{t}": scores[t] for t in topic_cols}
        })
    import pandas as pd
    progress_df = pd.DataFrame(rows)
    return students, progress_df
