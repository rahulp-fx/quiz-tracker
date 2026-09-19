from datetime import datetime 

def validate_text(text):
  if text is None or str(text).strip() == "":
    return False
  return True  

def validate_score(score,max_score):
  try:
    score = float(score)
    max_score = float(max_score)
    if score > max_score or score < 0:
      return False
    return True
  except ValueError:
    print("Invalid Data Type Passed")
    return False

def validate_date(date_text):
  try:
    date = datetime.strptime(date_text,"%Y-%m-%d")
    if (date):
      return True
  except ValueError as e:
    return False

def is_duplicate(df,student_id,quiz_id):
  duplicate_rows = df[(df['student_id'] == student_id) & (df['quiz_id'] == quiz_id)]
  if not duplicate_rows.empty:
    return True
  return False

