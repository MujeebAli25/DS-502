import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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
    except Exception:
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
    except Exception:
        diff_file = None

    # Clusters visualization: PCA projection
    try:
        from sklearn.decomposition import PCA
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
        else:
            cluster_file = None
    except Exception:
        cluster_file = None

    return {
        'heatmap': heatmap_file,
        'difficulty': diff_file,
        'clusters': cluster_file
    }
