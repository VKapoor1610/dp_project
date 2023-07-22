# this is a machine learning model to predict the expected accuracy 
# The data of the student enetered into google sheet will be loaded then prediction will be made on window size as per requirements \

import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np

# real data extraction from spreadsheet 
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# loading the data 

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('keys.json', scope)
client = gspread.authorize(creds)

# The ID of the Google Sheet you want to access
sheet_id = '1s_JrcyEhunXEqX0S826gwyZrDNMOfpIm_UGGCswMUb0'

# Open the Google Sheet by ID
sheet = client.open_by_key(sheet_id).sheet1

data = sheet.get_all_values()

# create a Pandas DataFrame from the data
df = pd.DataFrame(data[1:], columns=data[0])

df['status'] = df['status'].astype(int) - 1

# convert 'status' column to integer values
df['status'] = df['status'].astype(int)

# group by date and calculate the number of correct and incorrect questions
grouped = df.groupby('date')['status'].agg(correct='sum', incorrect='count') 

grouped['accuracy'] = grouped['correct']/grouped['incorrect']*100  # craeting a column for accuracy to make predictions
# Now a new column has been addded to grouped dataframe

from data_file import data
# print(len(data))  
# print(data)


# for Now using a sample data after good no of entries all data will be replaced by actual data 

# Moving Average Model for prediction 
# Current window size = 100 


#wait
data = [ np.random.uniform(50,100) for i in range(2000)]

# Create a pandas DataFrame from the data
df = pd.DataFrame({'value': data})

# Train-test split
train_size = 1800  # Use the first 1800 data points for training
train_data = df.iloc[:train_size]
test_data = df.iloc[train_size:]

# Predict using moving average
window_size = 100
predictions = []
for i in range(len(test_data)):
    start_idx = i - window_size
    end_idx = i
    if start_idx < 0:
        start_idx = 0
    window_data = test_data.iloc[start_idx:end_idx]['value'].values
    prediction = np.mean(window_data)
    predictions.append(prediction)

# Predict the 2001st value
start_idx = len(test_data) - window_size
end_idx = len(test_data)
window_data_2001 = test_data.iloc[start_idx:end_idx]['value'].values
prediction_2001 = np.mean(window_data_2001)

print("Predicted value for 2001st step:", prediction_2001)

# rmse =( np.mean(np.abs(np.array(predictions) - np.array(test_data[1:]))** 2))**0.5





