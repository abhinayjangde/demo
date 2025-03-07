import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Authenticate Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Open Google Sheet
SHEET_NAME = "BluBeep_Attendance"
spreadsheet = client.open(SHEET_NAME).sheet1

def record_attendance(student_name, device_address):
    """Logs attendance with timestamp in Google Sheets."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    spreadsheet.append_row([timestamp, student_name, device_address])

def fetch_attendance(search_query=None):
    """Fetches attendance data, filtered by name or date."""
    records = spreadsheet.get_all_values()[1:]  # Skip headers

    if search_query:
        records = [row for row in records if search_query.lower() in row[1].lower() or search_query in row[0]]
    
    return records
