import datetime
import pandas as pd
from collections import Counter

def WriteLog(log_file, pipeline_results):
    """
    Writes a simple summary log file.
    pipeline_results: the dict returned by run_pipeline()
    """
    with open(log_file, 'w') as f:
        f.write(f"Pipeline run: {datetime.datetime.now()}\n")
        f.write("="*50 + "\n")

        # Students & topics
        df = pipeline_results.get('df', None)
        difficulty_df = pipeline_results.get('topicDifficultyDF', pd.DataFrame())
        topic_cols = difficulty_df['topic'].tolist() if not difficulty_df.empty else []

        if df is not None:
            f.write(f"Number of students: {len(df)}\n")
        else:
            f.write("No student data available.\n")
        f.write(f"Topics: {topic_cols}\n\n")

        # Topic difficulty
        f.write("Topic Difficulty (top 5 hardest):\n")
        for idx, row in difficulty_df.head(5).iterrows():
            f.write(f"- {row['topic']}: difficulty_score={row['difficulty_score']:.1f}\n")
        f.write("\n")

        # Clusters
        clusters = pipeline_results.get('student_clusters', {})
        labels = clusters.get('labels', [])
        f.write(f"Number of clusters: {len(set(labels))}\n")
        if labels:
            counter = Counter(labels)
            f.write("Cluster sizes:\n")
            for cl, size in counter.items():
                f.write(f"- Cluster {cl}: {size} students\n")
        f.write("\n")

        # Mastery alerts
        alerts = pipeline_results.get('tutorRecs', {}).get('alerts', [])
        f.write(f"Number of mastery alerts: {len(alerts)}\n")
        f.write("\n")

        # Generated files
        f.write("Generated files:\n")
        dashboard = pipeline_results.get('dashboard_files', {})
        reports = pipeline_results.get('reports', {})
        for name, path in dashboard.items():
            f.write(f"- Dashboard {name}: {path}\n")
        for name, path in reports.items():
            f.write(f"- Report {name}: {path}\n")
        f.write("="*50 + "\n")
