import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def GenerateReports(studentProgressDF, topicDifficultyDF, tutorRecommendations, output_pdf='reports_summary.pdf'):
    studentProgressDF.to_csv('student_progress.csv', index=False)
    topicDifficultyDF.to_csv('topic_difficulty.csv', index=False)

    with PdfPages(output_pdf) as pdf:
        fig, ax = plt.subplots(figsize=(8.27, 11.69))
        ax.axis('off')
        table = ax.table(cellText=topicDifficultyDF.values, colLabels=topicDifficultyDF.columns, loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1, 1.5)
        ax.set_title('Topic Difficulty Ranking')
        pdf.savefig(fig)
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(8.27, 11.69))
        ax.axis('off')
        sample = studentProgressDF.head(40)
        table = ax.table(cellText=sample.values, colLabels=sample.columns, loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(6)
        table.scale(1, 1.2)
        ax.set_title('Student Progress (sample)')
        pdf.savefig(fig)
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(8.27, 11.69))
        ax.axis('off')
        text = "Tutor Alerts and Group Suggestions\n\n"
        for alert in tutorRecommendations.get('alerts', []):
            text += f"- {alert['student_name']} | {alert['topic']}: predicted {alert['predicted_score']:.1f}\n"
        text += "\nGroup Suggestions:\n"
        for s in tutorRecommendations.get('cluster_suggestions', []):
            text += f"- Cluster {s['cluster']}: {', '.join(s['common_weak_topics'])}\n"
        ax.text(0.01, 0.99, text, va='top', wrap=True, fontsize=10)
        pdf.savefig(fig)
        plt.close(fig)

    return {
        'report_pdf': output_pdf,
        'student_progress_csv': 'student_progress.csv',
        'topic_difficulty_csv': 'topic_difficulty.csv'
    }
