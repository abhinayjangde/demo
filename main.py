from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import threading
from attendance_manager import record_attendance, fetch_attendance
from bluetooth_scanner import get_bluetooth_devices

class AttendanceRecycleView(RecycleView):
    """Displays attendance records using RecycleView"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = [{"text": "Loading attendance..."}]

    def update_attendance(self, records):
        """Update UI with fetched attendance records"""
        self.data = [{"text": f"{rec['student_name']} - {rec['timestamp']}"} for rec in records]

class BluBeepUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        # Search Bar
        self.search_input = TextInput(hint_text="🔍 Search by name", multiline=False)
        self.search_input.bind(text=self.update_search_results)
        self.add_widget(self.search_input)

        # Attendance List (Using RecycleView)
        self.attendance_list = AttendanceRecycleView()
        self.add_widget(self.attendance_list)

        # Scan Bluetooth Button
        self.scan_button = Button(text="🔍 Scan Bluetooth Devices")
        self.scan_button.bind(on_press=self.scan_and_record)
        self.add_widget(self.scan_button)

        # Load Attendance Data Initially
        self.update_attendance_list()

    def update_search_results(self, instance, value):
        """Update attendance list based on search input"""
        results = fetch_attendance(filter_by=value)
        self.attendance_list.update_attendance(results)

    def scan_and_record(self, instance):
        """Scan for Bluetooth devices and record attendance"""
        # Disable button during scan
        self.scan_button.text = "🔄 Scanning..."
        self.scan_button.disabled = True
        
        # Run scan in separate thread
        threading.Thread(target=self._perform_scan, daemon=True).start()

    def _perform_scan(self):
        """Perform the actual scan in a separate thread"""
        try:
            devices = get_bluetooth_devices()
            # Schedule UI update on main thread
            Clock.schedule_once(lambda dt: self._on_scan_complete(devices), 0)
        except Exception as e:
            print(f"Scan error: {e}")
            Clock.schedule_once(lambda dt: self._on_scan_error(e), 0)

    def _on_scan_complete(self, devices):
        """Handle scan completion on main thread"""
        if devices:
            for name, addr in devices:
                record_attendance(name, addr)
            self.update_attendance_list()
            self.scan_button.text = f"✅ Found {len(devices)} devices"
        else:
            self.scan_button.text = "❌ No devices found"
        
        # Re-enable button after 2 seconds
        Clock.schedule_once(self._reset_button, 2)

    def _on_scan_error(self, error):
        """Handle scan error on main thread"""
        self.scan_button.text = f"❌ Scan failed"
        Clock.schedule_once(self._reset_button, 2)

    def _reset_button(self, dt):
        """Reset button to original state"""
        self.scan_button.text = "🔍 Scan Bluetooth Devices"
        self.scan_button.disabled = False

    def update_attendance_list(self):
        """Fetch and display attendance records"""
        records = fetch_attendance()
        self.attendance_list.update_attendance(records)

class BluBeepApp(App):
    def build(self):
        return BluBeepUI()

if __name__ == "__main__":
    BluBeepApp().run()