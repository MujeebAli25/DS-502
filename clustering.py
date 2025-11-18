import numpy as np
from sklearn.cluster import KMeans

def convertProgressToVectors(progress_students, topic_cols):
    vectors = []
    ids = []
    for s in progress_students:
        scores = [s['scores'].get(t, 0.0) for t in topic_cols]
        vectors.append(scores)
        ids.append((s['student_id'], s['student_name']))
    return np.array(vectors), ids

def ClusterStudents(progress_students, topic_cols, num_clusters=3, random_state=42):
    vectors, ids = convertProgressToVectors(progress_students, topic_cols)
    if len(vectors) == 0:
        return {'labels': [], 'centers': [], 'ids': ids}
    kmeans = KMeans(n_clusters=min(num_clusters, max(1, len(vectors))), random_state=random_state)
    kmeans.fit(vectors)
    clusters = {
        'labels': kmeans.labels_.tolist(),
        'centers': kmeans.cluster_centers_.tolist(),
        'ids': ids
    }
    return clusters
