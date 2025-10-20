from data_loader import LoadData
from difficulty import CalculateTopicDifficulty
from progress import TrackStudentProgress
from clustering import ClusterStudents
from prediction import PredictMastery
from recommendations import GenerateTutorRecommendations
from dashboard import GenerateDashboard
from reports import GenerateReports

def run_pipeline(csv_path='students.csv'):
    print("Loading data...")
    df, topic_cols = LoadData(csv_path)
    print(f"Found topics: {topic_cols}")

    print("Calculating topic difficulty...")
    topicDifficultyDF = CalculateTopicDifficulty(df, topic_cols)
    print(topicDifficultyDF.head())

    print("Tracking student progress...")
    progress_students, studentProgressDF = TrackStudentProgress(df, topic_cols, threshold=70)
    print(f"{len(progress_students)} students processed.")

    print("Clustering students...")
    student_clusters = ClusterStudents(progress_students, topic_cols, num_clusters=3)
    print("Clusters:", student_clusters.get('labels', [])[:10])

    print("Predicting mastery...")
    mastery_predictions_dict, mastery_pred_df = PredictMastery(df, topic_cols)
    print("Predictions computed.")

    print("Generating tutor recommendations...")
    tutorRecs = GenerateTutorRecommendations(progress_students, student_clusters, mastery_predictions_dict, topic_cols, masteryThreshold=60)
    print(f"Alerts: {len(tutorRecs['alerts'])} | Cluster suggestions: {len(tutorRecs['cluster_suggestions'])}")

    print("Generating dashboard visualizations...")
    dashboard_files = GenerateDashboard(topicDifficultyDF, studentProgressDF, student_clusters, topic_cols)
    print("Dashboard files:", dashboard_files)

    print("Generating reports...")
    reports = GenerateReports(studentProgressDF, topicDifficultyDF, tutorRecs)
    print("Reports generated:", reports)

    print("Pipeline complete.")
    return {
        'df': df,
        'topicDifficultyDF': topicDifficultyDF,
        'progress_students': progress_students,
        'studentProgressDF': studentProgressDF,
        'student_clusters': student_clusters,
        'mastery_predictions': mastery_predictions_dict,
        'mastery_pred_df': mastery_pred_df,
        'tutorRecs': tutorRecs,
        'dashboard_files': dashboard_files,
        'reports': reports
    }

if __name__ == "__main__":
    run_pipeline()
