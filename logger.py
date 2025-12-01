import datetime
from collections import Counter

def WriteLog(log_file, pipeline_results):
    with open(log_file, 'w') as f:
        f.write(f"Pipeline run: {datetime.datetime.now()}\n")
        f.write("="*50 + "\n")

        df = pipeline_results.get('df', None)
        difficulty_df = pipeline_results.get('topicDifficultyDF', None)
        topic_cols = difficulty_df['topic'].tolist() if difficulty_df is not None else []

        if df is not None:
            f.write(f"Number of students: {len(df)}\n")
            avg_risk = pipeline_results.get('progress_students', [])
            if avg_risk:
                mean_risk = sum(s['risk_score'] for s in avg_risk) / len(avg_risk)
                f.write(f"Average student risk score: {mean_risk:.1f}\n")
        else:
            f.write("No student data available.\n")
        f.write(f"Topics: {topic_cols}\n\n")

        f.write("Topic Difficulty (top 5 hardest):\n")
        if difficulty_df is not None:
            for idx, row in difficulty_df.head(5).iterrows():
                f.write(f"- {row['topic']}: difficulty_score={row['difficulty_score']:.1f}\n")
        f.write("\n")

        clusters = pipeline_results.get('student_clusters', {})
        labels = clusters.get('labels', [])
        f.write(f"Number of clusters: {len(set(labels))}\n")
        if labels:
            counter = Counter(labels)
            f.write("Cluster sizes:\n")
            for cl, size in counter.items():
                f.write(f"- Cluster {cl}: {size} students\n")
        sil_score = clusters.get('silhouette_score')
        f.write(f"Silhouette score: {sil_score}\n\n")

        alerts = pipeline_results.get('tutorRecs', {}).get('alerts', [])
        f.write(f"Number of mastery alerts: {len(alerts)}\n\n")

        f.write("Generated files:\n")
        for name, path in pipeline_results.get('dashboard_files', {}).items():
            f.write(f"- Dashboard {name}: {path}\n")
        for name, path in pipeline_results.get('reports', {}).items():
            f.write(f"- Report {name}: {path}\n")
        f.write("="*50 + "\n")
