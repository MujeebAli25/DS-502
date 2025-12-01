import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA

def GenerateDashboard(topicDifficultyDF, studentProgressDF, student_clusters, topic_cols, output_prefix='dashboard'):
    """
    Generates heatmap, topic difficulty leaderboard, cluster PCA visualization, and score distributions
    """
    dashboard_files = {}
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
        dashboard_files['heatmap'] = heatmap_file
    except Exception:
        dashboard_files['heatmap'] = None

    try:
        plt.figure(figsize=(10,5))
        for t in topic_cols:
            plt.hist(studentProgressDF[f"score_{t}"], alpha=0.5, label=t, bins=10)
        plt.xlabel('Score')
        plt.ylabel('Number of students')
        plt.title('Score Distribution by Topic')
        plt.legend()
        dist_file = f"{output_prefix}_score_dist.png"
        plt.tight_layout()
        plt.savefig(dist_file)
        plt.close()
        dashboard_files['score_distribution'] = dist_file
    except Exception:
        dashboard_files['score_distribution'] = None

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
        dashboard_files['difficulty'] = diff_file
    except Exception:
        dashboard_files['difficulty'] = None

    try:
        clusters = student_clusters
        if 'centers' in clusters and clusters['centers']:
            centers = np.array(clusters['centers'])
            pca = PCA(n_components=2)
            projected = pca.fit_transform(centers)
            plt.figure(figsize=(6,6))
            plt.scatter(projected[:,0], projected[:,1])
            for i in range(len(projected)):
                plt.annotate(f"C{i}", (projected[i,0], projected[i,1]))
            plt.title('Cluster centers (PCA 2D)')
            plt.tight_layout()
            cluster_file = f"{output_prefix}_clusters.png"
            plt.savefig(cluster_file)
            plt.close()
            dashboard_files['clusters'] = cluster_file
    except Exception:
        dashboard_files['clusters'] = None

    return dashboard_files
