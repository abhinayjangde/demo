# BlueBeep: Bluetooth-Based Attendance System

BlueBeep is an automated attendance tracking system that uses **Bluetooth scanning** to mark attendance. It ensures **immutability and transparency** by storing records in **MongoDB**.

---

## 🚀 Features

- 📡 **Bluetooth Scanning** – Detects nearby Bluetooth devices and records attendance.
- 🔍 **Search & Filter** – Quickly find attendance records by name or date.
- 📜 **History View** – Displays past attendance logs.
- 💾 **MongoDB Database** – Stores attendance securely.
- 🎨 **User-Friendly UI** – Built with Kivy for a smooth experience.

---

## 🛠 Installation

### 1️⃣ Clone the Repository

```sh
git clone https://github.com/yourusername/BluBeep.git
cd BluBeep
```

### 2️⃣ Create a Virtual Environment

```sh
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate    # Windows
```

### 3️⃣ Install Dependencies

```sh
pip install -r requirements.txt
```

### 4️⃣ Set Up MongoDB

1. Install MongoDB and start the service.
2. Update `attendance_manager.py` with your MongoDB connection string.

---

## 📌 Usage

### Run the Application

```sh
python main.py
```

### Marking Attendance

- Click **"Scan Bluetooth Devices"** to detect nearby devices.
- Attendance is recorded automatically in MongoDB.

### Searching Attendance

- Use the **search bar** to find attendance by name or date.

---

## 📂 Project Structure

```
BluBeep/
│── main.py               # Main Kivy App
│── bluetooth_scanner.py  # Bluetooth scanning logic
│── attendance_manager.py # Handles MongoDB operations
│── requirements.txt      # Dependencies
│── README.md             # Documentation
```

---

## 👨‍💻 Contributing

Feel free to fork and contribute! Submit a pull request with improvements.

---

