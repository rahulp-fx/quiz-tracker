import pandas as pd
import analysis
import matplotlib.pyplot as plt

def plot_student_trend(df,student_name):
  filtered_df = df[df['student_name'] == student_name]
  sorted_df = filtered_df.sort_values(by='date')
  sorted_df['percentage'] = (sorted_df['score']/sorted_df['max_score'])*100

  plt.plot(sorted_df['date'],sorted_df['percentage'],marker='o')
  plt.title("Student Performance")
  plt.xlabel("Time")
  plt.ylabel("Percentage")
  plt.show()

def plot_quiz_averages(df):
  df['percentage'] = (df['score']/df['max_score'])*100
  grouped_df = df.groupby('quiz_id')['percentage'].mean()

  plt.bar(grouped_df.index,grouped_df.values)
  plt.title("Average Score per Quiz")
  plt.xlabel("Quiz ID")
  plt.ylabel("Average Percentage")
  plt.show()

def plot_topic_performance(df):
  grouped_df = analysis.get_topic_performance(df)
  
  plt.barh(grouped_df.index,grouped_df.valyes)
  plt.title("Performance by Topic")
  plt.xlabel("Average Percentage")
  plt.ylabel("Topic")
  plt.show()

