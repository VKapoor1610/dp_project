
import pandas as pd 
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('keys.json', scope)
client = gspread.authorize(creds)

# The ID of the Google Sheet you want to access
sheet_id = '1s_JrcyEhunXEqX0S826gwyZrDNMOfpIm_UGGCswMUb0'

# Open the Google Sheet by ID
sheet = client.open_by_key(sheet_id).sheet1

data = sheet.get_all_values()



#  create a Pandas DataFrame from the data
df = pd.DataFrame(data[1:], columns=data[0])

df['status'] = df['status'].astype(int) - 1

# convert 'status' column to integer values
df['status'] = df['status'].astype(int)

# group by date and calculate the number of correct and incorrect questions
grouped = df.groupby('date')['status'].agg(correct='sum', incorrect='count') 

# calculate the total number of questions per date
grouped['total_questions'] = grouped['correct'] + grouped['incorrect']


