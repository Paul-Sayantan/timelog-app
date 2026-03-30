###
# Json data to handle the counting, grouping, and time totals
###

import csv
import json
from collections import defaultdict
import os
import ollama
from ollama import chat

##filedir  = "E:\\My_Timer_app"

filedir  = os.getcwd()
filename = f"{filedir}\\timelog.csv"
print(filename)


filename = f"{filedir}\\timelog.csv"

grouped_data = defaultdict(list)
with open(filename, "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        grouped_data[row['ProjectandTask']].append(row)

topic_list     =[]
topic_timelist =[]
topic_final_loglist=[]
for k in grouped_data:
    topic_list.append(k)
    total_time      = 0
    topic_logset    = set() #https://codingtechroom.com/question/-unique-values-list-preserve-order
    topic_log       = []
    for i in grouped_data.get(k):
        hh,mm,ss = [int(x) for x in i['Time'].split(':')]
        time_spent = round((hh*3600 + mm*60 + ss)/3600, 2)
        total_time = total_time + time_spent
        if i['Log'] not in topic_logset:
            topic_logset.add(i['Log'])
            topic_log.append(i['Log'])
    topic_timelist.append(total_time)
    topic_final_loglist.append(topic_log)

## Making list that will be converted to json
list_for_json = []
for i in range(len(topic_list)): #https://www.golinuxcloud.com/python-loop-through-lists/
    d = {
  "project_task_subtask": topic_list[i],
  "total_hours": topic_timelist[i],
  "progress_notes": topic_final_loglist[i]
  }
    list_for_json.append(d)
### print the list to verify
##for i in list_for_json:
##    print(i)
##    print('\n')
    topic_logset    = set() #https://codingtechroom.com/question/-unique-values-list-preserve-order
    topic_log       = []
    for i in grouped_data.get(k):
        hh,mm,ss = [int(x) for x in i['Time'].split(':')]
        time_spent = round((hh*3600 + mm*60 + ss)/3600, 2)
        total_time = total_time + time_spent
        if i['Log'] not in topic_logset:
            topic_logset.add(i['Log'])
            topic_log.append(i['Log'])
    topic_timelist.append(total_time)

## dumps to json
model_json = json.dumps(list_for_json)
##print(type(model_json))

##json_loads = json.loads(model_json)
##print(type(json_loads))
#### Convert list to json format
##with open(f'{filedir}/output.json', mode = 'w', encoding= 'utf-8') as jsonfile:
##    json.dump(list_for_json, jsonfile, indent=4)

###
## Creating Model Prompt
###
prompt = f"""
You are analyzing time-tracking progress data.

Data:
{model_json}

Tasks:
Understand the task progress.
From the task progress suggest the best possible next step.
"""

## Call Ollama
response = chat(
    model = 'llama3.2',
    messages = [{'role': 'user', 'content': prompt}]
    )

## print the result from the model
##print(response['message']['content'])
print(response.message.content)




##print(topic_list)
##print(topic_timelist)
##print(topic_final_loglist)
##for k,v in grouped_data.items():
##    for i in v:
##        print(i['Date'])       
##    csvfile = csv.reader(file)
##    next(csvfile, None)
##    for lines in csvfile:
##        date     = lines[0]
##        duration = lines[1]
##        topic    = lines[2] 
##        hh,mm,ss = [int(x) for x in duration.split(':')]
##        if topic not in topicdict:
##            topicdict.append(topic)
##        for topic in topicdict:
##            if date not in datedict:
##                datedict.append(date)
##for key in grouped_data:
##    print(grouped_data(key))
##    break
##print(topicdict)
##print(grouped_data)
##with open(f'{filedir}/output.json', mode = 'w', encoding= 'utf-8') as jsonfile:
##    json.dump(grouped_data, jsonfile, indent=4)
##for k,v in grouped_data.items():
##    print(k,v)
##    break
