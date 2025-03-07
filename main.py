from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListView, ListAdapter
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from bluetooth_scanner import get_bluetooth_devices
from attendance_manager import record_attendance, fetch_attendance

class BluBeepUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        # Search Bar
        self.search_input = TextInput(hint_text="Search by Name or Date", multiline=False)
        self.search_input.bind(text=self.update_search)
        self.add_widget(self.search_input)

        # List View for Attendance
        self.list_view = ListView()
        self.add_widget(self.list_view)

        # Scan Button
        self.scan_button = Button(text="Scan Bluetooth Devices", size_hint=(1, 0.2))
        self.scan_button.bind(on_press=self.scan_and_record)
        self.add_widget(self.scan_button)

        # Load initial attendance data
        self.update_search()

    def scan_and_record(self, instance):
        devices = get_bluetooth_devices()
        for name, address in devices:
            record_attendance(name, address)

        self.update_search()

    def update_search(self, instance=None):
        query = self.search_input.text.strip()
        records = fetch_attendance(query)

        items = [f"{r[0]} | {r[1]} | {r[2]}" for r in records]
        self.list_view.adapter = ListAdapter(data=items, cls=Button)

class BluBeepApp(App):
    def build(self):
        return BluBeepUI()

if __name__ == "__main__":
    BluBeepApp().run()
