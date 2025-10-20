# cluster_labels: list of ints, same order as ids
# ids: list of tuples (student_id, student_name)
# progress_students: list of student dicts from TrackStudentProgress


from collections import Counter

def identifyCommonWeakTopics(cluster_labels, ids, progress_students):
    cluster_map = {}
    for label, (sid, sname), student in zip(cluster_labels, ids, progress_students):
        cluster_map.setdefault(label, []).append(student)

    recommendations = {}
    for label, students in cluster_map.items():
        all_weak = []
        for s in students:
            all_weak.extend(s['weak_topics'])
        counter = Counter(all_weak)
        common = [t for t, cnt in counter.most_common(5)]  # top 5
        recommendations[label] = common
    return recommendations

def GenerateTutorRecommendations(progress_students, student_clusters, mastery_predictions, topic_cols, masteryThreshold=60):
    """
    For each student/topic where predicted mastery < masteryThreshold create an 'at risk' alert.
    For each cluster, identify common weak topics and suggest group sessions.
    Returns dict with student_alerts and cluster_suggestions.
    """
    alerts = []
    # mastery_predictions is a dict keyed by (student_id, topic) -> predicted_score
    for s in progress_students:
        sid = s['student_id']
        sname = s['student_name']
        for t in topic_cols:
            key = (sid, t)
            pred = mastery_predictions.get(key, None)
            if pred is None:
                continue
            if pred < masteryThreshold:
                alerts.append({
                    'student_id': sid,
                    'student_name': sname,
                    'topic': t,
                    'predicted_score': pred,
                    'message': f"Student at risk in topic '{t}' (predicted {pred:.1f} < {masteryThreshold})"
                })

    cluster_suggestions = {}
    labels = student_clusters.get('labels', [])
    ids = student_clusters.get('ids', [])
    # Reconstruct progress_students order matching ids to call identifyCommonWeakTopics
    # ids contains (student_id, student_name)
    # Map id->student dict
    id_to_student = { (s['student_id'], s['student_name']): s for s in progress_students }
    ordered_students = [id_to_student.get(idpair) for idpair in ids]
    cluster_suggestions = identifyCommonWeakTopics(labels, ids, ordered_students)

    suggestions = []
    for c, topics in cluster_suggestions.items():
        suggestions.append({
            'cluster': c,
            'common_weak_topics': topics,
            'suggestion': f"Group tutoring recommended for topics: {', '.join(topics)}"
        })

    return {
        'alerts': alerts,
        'cluster_suggestions': suggestions
    }
