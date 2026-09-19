import pandas as pd
import tkinter as tk
from tkinter import ttk,messagebox
import storage
import validation
import analysis
import charts

#functions
def clear():
  id.set("")
  name.set("")
  quizId.set("")
  quizName.set("")
  topic.set("")
  date.set("")
  score.set("")
  maxScore.set("")

def submit_record():
  # ttk.Label(tab1,text="Button Clicked!").pack()
  student_id_val = id.get()
  student_name_val = name.get()
  quiz_id_val = quizId.get()
  quiz_name_val = quizName.get()
  topic_val = topic.get()
  date_val = date.get()
  score_val = score.get()
  max_score_val = maxScore.get()

  #validation for text
  if not (validation.validate_text(student_id_val)) and (validation.validate_text(student_name_val)) and (validation.validate_text(quiz_id_val)) and (validation.validate_text(quiz_name_val)) and (validation.validate_text(topic_val)) and (validation.validate_text(score_val)) and (validation.validate_text(max_score_val)):
    messagebox.showerror("Error","All fields are required")
    return 

  #score validation
  elif not validation.validate_score(score_val,max_score_val):
    messagebox.showerror("Error","Invalid Scores")
    return

  #date validation
  elif not validation.validate_date(date_val):
    messagebox.showerror("Error","Invalid date")
    return

  df = storage.load_data(storage.path)
  if validation.is_duplicate(df,student_id_val,quiz_id_val):
    messagebox.showerror("Error","Student has already taken the quiz")
    return

  record = pd.DataFrame([{
    'student_id':student_id_val,
    'student_name':student_name_val,
    'quiz_id':quiz_id_val,
    'quiz_name':quiz_name_val,
    'topic':topic_val,
    'date':date_val,
    'score':score_val,
    'max_score':max_score_val
  }])

  storage.add_record(storage.path,record)
  clear()
  view_records()
  messagebox.showinfo("Success","Record Added Successfully!")

def view_records():
  for item in tree.get_children():
    tree.delete(item)
  df = storage.load_data(storage.path)
  for row in df.values.tolist():
      tree.insert('',tk.END,values=row)

  tree.pack(fill=tk.BOTH,expand=True)
  Record_status.pack()

def run_analysis():
  df = storage.load_data(storage.path)
  averages = analysis.get_student_averages(df)
  topics = analysis.get_topic_performance(df)
  high_low = analysis.get_high_low_performers(df)

  report = f"--- Student Averages ---\n{averages.to_string()}\n\n"
  report += f"--- Topic Performance ---\n{topics.to_string()}\n\n"
  report += f"--- High/Low Performers ---\nHigh:{', '.join(high_low['high'])}\nLow: {', '.join(high_low['low'])}"

  analysis_text.delete('1.0', tk.END)
  analysis_text.insert(tk.END,report)

def show_quiz_averages():
  df = storage.load_data(storage.path)
  charts.plot_quiz_averages(df)

def show_topic_performance():
  df = storage.load_data(storage.path)
  charts.plot_topic_performance(df)

def show_student_trend():
  df = storage.load_data(storage.path)
  student = search_student_var.get()

  if not student.strip():
    messagebox.showerror("Error","Please enter student name")
    return

  if student not in df['student_name'].values:
    messagebox.showerror("Error","Student not found")
    return
  charts.plot_student_trend(df,student)

  
#main code
root = tk.Tk()
root.title('Quiz Performance Tracker')
root.geometry('800x600')

Notebook = ttk.Notebook(root)
Notebook.pack(expand=True,fill="both")

tab1 = ttk.Frame(Notebook)
tab2 = ttk.Frame(Notebook)
tab3 = ttk.Frame(Notebook)
tab4 = ttk.Frame(Notebook)

Notebook.add(tab1,text="Data Entry")
Notebook.add(tab2,text="View Records")
Notebook.add(tab3,text="Analysis")
Notebook.add(tab4,text="Reports")

#Tab 1
id = tk.StringVar()
ttk.Label(tab1,text="Student Id").pack()
Student_Id = ttk.Entry(tab1, textvariable=id)
Student_Id.pack()

name = tk.StringVar()
ttk.Label(tab1,text="Student Name").pack()
Student_Name = ttk.Entry(tab1, textvariable=name)
Student_Name.pack()

quizId = tk.StringVar()
ttk.Label(tab1,text="Quiz Id").pack()
Quiz_Id = ttk.Entry(tab1, textvariable=quizId)
Quiz_Id.pack()

quizName = tk.StringVar()
ttk.Label(tab1,text="Quiz Name").pack()
Quiz_Name = ttk.Entry(tab1, textvariable=quizName)
Quiz_Name.pack()

topic = tk.StringVar()
ttk.Label(tab1,text="Topic").pack()
Topic = ttk.Entry(tab1, textvariable=topic)
Topic.pack()

date = tk.StringVar()
ttk.Label(tab1,text="Date (YYYY-MM-DD)").pack()
Date_Name = ttk.Entry(tab1, textvariable=date)
Date_Name.pack()

score = tk.StringVar()
ttk.Label(tab1,text="Obtained Score").pack()
Score = ttk.Entry(tab1, textvariable=score)
Score.pack()

maxScore = tk.StringVar()
ttk.Label(tab1,text="Max Score").pack()
Max_Score = ttk.Entry(tab1, textvariable=maxScore)
Max_Score.pack()

ttk.Button(tab1,text="Add Record",command=submit_record).pack()

# Tab 2
ttk.Button(tab2,text="View Records",command=view_records).pack()
Record_status = ttk.Label(tab2,text="Records Refreshed")
columns = ('student_id','student_name','quiz_id','quiz_name','topic','date','score','max_score')

tree = ttk.Treeview(tab2,columns=columns,show='headings')

tree.heading('student_id',text='Id')
tree.heading('student_name',text='Name')
tree.heading('quiz_id',text='Quiz Id')
tree.heading('quiz_name',text='Quiz Name')
tree.heading('topic',text='Topic')
tree.heading('date',text='Date')
tree.heading('score',text='Score')
tree.heading('max_score',text='Max_Score')

tree.column('student_id', width=100, anchor=tk.W)
tree.column('student_name', width=100, anchor=tk.W)
tree.column('quiz_id', width=100, anchor=tk.W)
tree.column('quiz_name', width=100, anchor=tk.W)
tree.column('topic', width=120, anchor=tk.W)
tree.column('date', width=80, anchor=tk.W)
tree.column('score', width=100, anchor=tk.W)
tree.column('max_score', width=100, anchor=tk.W)

view_records()

# Tab 3
analysis_text = tk.Text(tab3,height=20,width=70)
analysis_text.pack()
ttk.Button(tab3,text="Refresh Analysis",command=run_analysis).pack()

# Tab 4
ttk.Label(tab4,text="Class Overview Reports").pack()

ttk.Button(tab4,text="View Average Score Per Quiz",command=show_quiz_averages).pack()
ttk.Button(tab4,text="View Performance by Topic",command=show_topic_performance).pack()

ttk.Label(tab4,text="").pack(pady=10)
ttk.Label(tab4,text="Individual Student Trend").pack()
ttk.Label(tab4,text="Enter Student Name:").pack()
search_student_var = tk.StringVar()
ttk.Entry(tab4,textvariable=search_student_var).pack(pady=5)

ttk.Button(tab4,text="View Student Trend",command=show_student_trend).pack()

root.mainloop()