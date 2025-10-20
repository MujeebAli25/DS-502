# difficulty.py
import pandas as pd

# Calculates difficulty score for each topic:
# difficulty = 100 - mean_score   (higher => harder)
# Returns a sorted list of tuples

def CalculateTopicDifficulty(df, topic_cols):
    means = df[topic_cols].mean()
    difficulty = 100 - means
    difficulty_df = pd.DataFrame({
        'topic': difficulty.index,
        'difficulty_score': difficulty.values,
        'mean_score': means.values
    }).sort_values('difficulty_score', ascending=False).reset_index(drop=True)
    return difficulty_df
