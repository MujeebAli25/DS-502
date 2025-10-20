# dashboard.py
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Saves a few visualizations as PNG files:
# - heatmap of student-topic performance
# - topic difficulty leaderboard (bar chart)
# - clusters scatter using PCA projection (2D)
def GenerateDashboard(topicDifficultyDF, studentProgressDF, student_clusters, topic_cols, output_prefix='dashboard'):
    # Heatmap
    try:
        scores_df = studentProgressDF[[f"score_{t}" for t in topic_cols]]
        plt.figure(figsize=(10, max(4, len(scores_df)/4)))
        plt.imshow(scores_df.values, aspect='auto', interpolation='nearest')
        plt.colorbar(label='Score')
        plt.xlabel('Topics')
        plt.ylabel('Students')
        plt.xticks(ticks=range(len(topic_cols)), labels=topic_cols, rotation=45, ha='right')
        plt.title('Student-Topic Score Heatmap')
        plt.tight_layout()
        heatmap_file = f"{output_prefix}_heatmap.png"
        plt.savefig(heatmap_file)
        plt.close()
    except Exception as e:
        heatmap_file = None

    # Difficulty leaderboard
    try:
        plt.figure(figsize=(8,4))
        plt.bar(topicDifficultyDF['topic'], topicDifficultyDF['difficulty_score'])
        plt.xticks(rotation=45, ha='right')
        plt.ylabel('Difficulty Score (100 - mean)')
        plt.title('Topic Difficulty Leaderboard')
        plt.tight_layout()
        diff_file = f"{output_prefix}_difficulty.png"
        plt.savefig(diff_file)
        plt.close()
    except Exception as e:
        diff_file = None

    # Clusters visualization: project centers/points into 2D using PCA
    try:
        from sklearn.decomposition import PCA
        clusters = student_clusters
        vectors = []
        ids = []
        if 'ids' in clusters and clusters['ids']:
            for (sid, sname) in clusters['ids']:
                # we expect cluster centers -> but we want the original student vectors
                ids.append(sname)
        if 'centers' in clusters and clusters['centers']:
            centers = np.array(clusters['centers'])
            pca = PCA(n_components=2)
            projected = pca.fit_transform(centers)
            plt.figure(figsize=(6,6))
            plt.scatter(projected[:,0], projected[:,1])
            for i, txt in enumerate(range(len(projected))):
                plt.annotate(f"C{txt}", (projected[i,0], projected[i,1]))
            plt.title('Cluster centers (PCA 2D)')
            plt.tight_layout()
            cluster_file = f"{output_prefix}_clusters.png"
            plt.savefig(cluster_file)
            plt.close()
        else:
            cluster_file = None
    except Exception as e:
        cluster_file = None

    return {
        'heatmap': heatmap_file,
        'difficulty': diff_file,
        'clusters': cluster_file
    }
