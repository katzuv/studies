#%% md
# # תרגיל בית 5
#%%
import pandas as pd
#%% md
# ### Section 1
#%%
def read_event_data(file_path):
    ## Add your code!
#%% md
# ### Section 2
#%%
def top_athlete(events, event_name):
    ## Add your code!
#%%
# Run - Do not change this cell!
file_path = 'sports_event.csv'
events = read_event_data(file_path)
for event in ["Discus Throw", "Long Jump", "High Jump", "Shot Put"]:
    print(f"{event}: {top_athlete(events, event)}")
#%% md
# ### Section 3
#%%
def event_scores(events, event_name):
    ## Add your code!
#%%
# Run - Do not change this cell!
file_path = 'sports_event.csv'
events = read_event_data(file_path)
for event in ["Discus Throw", "Long Jump", "High Jump", "Shot Put"]:
    print(f"{event}: {sorted(event_scores(events, event))}")
#%% md
# ### Section 4
#%%
def unique_events(events):
    ## Add your code!
#%%
# Run - Do not change this cell!
file_path = 'sports_event.csv'
events = read_event_data(file_path)
print(sorted(unique_events(events)))
#%% md
# ### Section 5
#%%
def count_events(events):
    ## Add your code!
#%%
# Run - Do not change this cell!
file_path = 'sports_event.csv'
events = read_event_data(file_path)
event_type, count = count_events(events)
for event in ["Discus Throw", "Long Jump", "High Jump", "Shot Put"]:
    idx = event_type.index(event)
    print(f"{event}: {count[idx]}")
        
#%% md
# ### Section 6
#%%
def analyze_scores(events, event_name):
    ## Add your code!
#%% md
# ### Section 7
#%%
def analyze_event(file_path, event_name):
    ## Add your code!
    
#%%
# Run - Do not change this cell!
file_path = 'sports_event.csv'
for event in ["Discus Throw", "Long Jump", "High Jump", "Shot Put"]:
    analyze_event(file_path, event)
#%%
# Run on your data
# make sure my_events.csv is in the same directory as this notebook
filename2 = 'my_events.csv'
event = ''# add your event here
analyze_event(file_path, event)
#%% md
# # חלק יבש 
# ניתן למחוק חלק זה ולצרף את החלק היבש באחת הדרכים האחרים שתוארו במסמך
#%%
## To start a new line in answers below use <br>
#%% md
# ## סעיף 5
#%% md
# 1) double click to add answer
#%% md
# 2) double click to add answer
#%% md
# ## סעיף 6
#%% md
# 1) double click to add answer
#%% md
# 2) double click to add answer
#%% md
# 3) double click to add answer
#%%
