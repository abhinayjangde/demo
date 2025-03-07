import bluetooth
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import time
import csv
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup

# Step 1: Set up Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("BluBeep_Attendance").sheet1

class BluBeepApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        
        self.label = Label(text="Press 'Scan' to find Bluetooth devices", font_size=20)
        self.layout.add_widget(self.label)
        
        self.scan_button = Button(text="Scan", font_size=20, on_press=self.scan_bluetooth)
        self.layout.add_widget(self.scan_button)
        
        self.history_button = Button(text="Show Attendance History", font_size=20, on_press=self.show_history)
        self.layout.add_widget(self.history_button)
        
        self.search_input = TextInput(hint_text="Search by name", font_size=18, size_hint_y=None, height=50)
        self.layout.add_widget(self.search_input)
        
        self.date_spinner = Spinner(text="Select Date", values=["All"] + self.get_unique_dates(), size_hint_y=None, height=50)
        self.layout.add_widget(self.date_spinner)
        
        self.search_button = Button(text="Search", font_size=20, on_press=self.search_history)
        self.layout.add_widget(self.search_button)
        
        self.export_button = Button(text="Export as CSV", font_size=20, on_press=self.export_to_csv)
        self.layout.add_widget(self.export_button)
        
        self.scroll_view = ScrollView()
        self.result_layout = GridLayout(cols=1, size_hint_y=None)
        self.result_layout.bind(minimum_height=self.result_layout.setter('height'))
        self.scroll_view.add_widget(self.result_layout)
        self.layout.add_widget(self.scroll_view)
        
        return self.layout
    
    def scan_bluetooth(self, instance):
        self.label.text = "Scanning..."
        Clock.schedule_once(lambda dt: self.perform_scan(), 0)
    
    def perform_scan(self):
        self.result_layout.clear_widgets()
        devices = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True, lookup_class=False)
        
        if not devices:
            self.result_layout.add_widget(Label(text="No devices found.", font_size=16))
        else:
            for addr, name in devices:
                device_label = Label(text=f"{name} - {addr}", font_size=16, size_hint_y=None, height=40)
                self.result_layout.add_widget(device_label)
                self.log_attendance(name, addr)
        
        self.label.text = "Scan Complete"
    
    def log_attendance(self, device_name, mac_address):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([device_name, mac_address, timestamp])
        print(f"Attendance recorded: {device_name} ({mac_address}) at {timestamp}")
    
    def show_history(self, instance):
        self.result_layout.clear_widgets()
        self.result_layout.add_widget(Label(text="Attendance History:", font_size=20))
        records = sheet.get_all_values()[-10:]
        
        for record in records:
            history_label = Label(text=f"{record[0]} - {record[1]} at {record[2]}", font_size=16, size_hint_y=None, height=40)
            self.result_layout.add_widget(history_label)
    
    def search_history(self, instance):
        query_name = self.search_input.text.strip()
        query_date = self.date_spinner.text if self.date_spinner.text != "All" else ""
        
        self.result_layout.clear_widgets()
        self.result_layout.add_widget(Label(text="Search Results:", font_size=20))
        
        records = sheet.get_all_values()
        filtered_records = [record for record in records if (query_name in record[0] or not query_name) and (query_date in record[2] or not query_date)]
        
        if not filtered_records:
            self.result_layout.add_widget(Label(text="No matching records found.", font_size=16))
        else:
            for record in filtered_records:
                history_label = Label(text=f"{record[0]} - {record[1]} at {record[2]}", font_size=16, size_hint_y=None, height=40)
                self.result_layout.add_widget(history_label)
    
    def get_unique_dates(self):
        records = sheet.get_all_values()
        unique_dates = sorted(set(record[2].split()[0] for record in records if len(record) > 2), reverse=True)
        return unique_dates
    
    def export_to_csv(self, instance):
        records = sheet.get_all_values()
        filename = "attendance_records.csv"
        
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Device Name", "MAC Address", "Timestamp"])
            writer.writerows(records)
        
        popup = Popup(title="Export Successful", content=Label(text=f"Records saved to {filename}"), size_hint=(0.6, 0.4))
        popup.open()

if __name__ == "__main__":
    BluBeepApp().run()
