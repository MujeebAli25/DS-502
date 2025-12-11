from data_loader import LoadData
from difficulty import CalculateTopicDifficulty
from progress import TrackStudentProgress
from clustering import ClusterStudents
from prediction import PredictMastery
from recommendations import GenerateTutorRecommendations
from dashboard import GenerateDashboard
from reports import GenerateReports
from logger import WriteLog

def run_pipeline(csv_path='students.csv', log_file='pipeline_summary.log'):
    df, topic_cols = LoadData(csv_path)

    topicDifficultyDF = CalculateTopicDifficulty(df, topic_cols)

    progress_students, studentProgressDF = TrackStudentProgress(df, topic_cols)

    student_clusters = ClusterStudents(progress_students, topic_cols, num_clusters=3)

    mastery_predictions_dict, mastery_pred_df = PredictMastery(df, topic_cols)

    tutorRecs = GenerateTutorRecommendations(progress_students, student_clusters, mastery_predictions_dict, topic_cols, masteryThreshold=60)

    dashboard_files = GenerateDashboard(topicDifficultyDF, studentProgressDF, student_clusters, topic_cols)

    reports = GenerateReports(studentProgressDF, topicDifficultyDF, tutorRecs)

    WriteLog(log_file, {
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
    })

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
