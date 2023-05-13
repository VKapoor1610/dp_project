import matplotlib.pyplot as plt
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

# Get all the values from the sheet
import matplotlib.pyplot as plt
import pandas as pd

# Read the data from your source (e.g., spreadsheet, CSV file, etc.)
data = sheet.get_all_values()

# Create a Pandas DataFrame from the data
df = pd.DataFrame(data[1:], columns=data[0])

# Convert columns to appropriate data types
df['status'] = df['status'].astype(int)
df['incorrect'] = df['incorrect'].astype(int)

# Filter the DataFrame based on mode = 'lp'
filtered_df = df[df['mode'] == 'lp']

# Group by date and calculate the number of correct and incorrect questions
grouped = filtered_df.groupby('date')['status'].value_counts().unstack().fillna(0)

# Plot the stacked bar chart
ax = grouped.plot.bar(stacked=True, color=['#fc1303', '#03fc30'], width=0.8)

# Add labels and title
ax.set_xlabel('Date')
ax.set_ylabel('Frequency')
ax.set_title('Frequency of Correct and Incorrect Attempts by Date')

# Add legend
ax.legend(['Incorrect', 'Correct'], loc='upper left')

# Show the plot
plt.show()
