import pandas as pd
from pathlib import Path

'''
path = Path("data/quiz_results.csv")
if path.exists():
  print('Success')
else:
  print('Failure')
'''

path = Path("data/quiz_results.csv")

def initialize_file(file_path):
  try:
    #question - why '../data/quiz_results.csv' returned failure
    if file_path.exists():
      return True
    else:
      df = pd.DataFrame(columns=['student_id', 'student_name', 'quiz_id', 'quiz_name', 'topic', 'date', 'score', 'max_score'])
      df.to_csv(file_path,index=False)
      return True

  except PermissionError as e:
    print(e)
    return False

  except Exception as e:
    print(e)
    return False

def load_data(file_path):
  try:
    if initialize_file(file_path):
      df = pd.read_csv(file_path)
      # print(df.head())
      return df
    else:
      print('Failure')

  except pd.errors.EmptyDataError as e:
    print(e)
    return pd.DataFrame(columns=['student_id', 'student_name', 'quiz_id', 'quiz_name', 'topic', 'date', 'score', 'max_score'])

  except Exception as e:
    print(e)
    return pd.DataFrame(columns=['student_id', 'student_name', 'quiz_id', 'quiz_name', 'topic', 'date', 'score', 'max_score'])

#save
def save_data(df,file_path): 
  try:
    if initialize_file(file_path):
      df.to_csv(file_path,index=False)
      print("Successfully saved")
    else:
      print("Failure")

  except PermissionError as e:
    print(e)
    return False

  except Exception as e:
    print(e)
    return False

#append
def add_record(file_path,record):
  try:
    if initialize_file(file_path):
      df = load_data(file_path)
      updated_df = pd.concat([df,record],ignore_index=True)
      save_data(updated_df,file_path)
    else:
      print("Failure")

  except Exception as e:
    print(e)
    return False