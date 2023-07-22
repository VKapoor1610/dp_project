
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




