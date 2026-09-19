import pandas as pd

def get_student_averages(df):
  # df['percentage'] = (df['score']/df['max_score'])*100
  prepare_data(df)
  return df.groupby('student_name')['percentage'].mean()

def get_quiz_stats(df,quiz_id):
  filtered_df = df[df['quiz_id'] == quiz_id]
  mean = filtered_df['score'].mean()
  max = filtered_df['score'].max()
  min = filtered_df['score'].min()
  return {'mean': float(mean),'max':float(max),'min':float(min)}

def get_topic_performance(df):
  # df['percentage'] = (df['score']/df['max_score'])*100
  prepare_data(df)
  return df.groupby('topic')['percentage'].mean()

def get_high_low_performers(df,high_threshold=80,low_threshold=40):
  averages = get_student_averages(df)
  high_performers = averages[averages >= high_threshold].index.tolist()
  low_performers = averages[averages <= low_threshold].index.tolist()
  return {'high':high_performers,'low':low_performers}  

def prepare_data(df):
  df['percentage'] = (df['score']/df['max_score'])*100