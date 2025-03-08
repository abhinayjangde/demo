from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB (Localhost)
client = MongoClient("mongodb://localhost:27017/")
db = client["BluBeepDB"]  # Database
attendance_collection = db["AttendanceRecords"]  # Collection

def record_attendance(student_name, device_id):
    """Store attendance records in MongoDB"""
    record = {
        "student_name": student_name,
        "device_id": device_id,
        "timestamp": datetime.utcnow()
    }
    attendance_collection.insert_one(record)
    print(f"✅ Attendance recorded for {student_name}")

def fetch_attendance(filter_by=None):
    """Fetch attendance records from MongoDB"""
    query = {}  # Default: Fetch all

    if filter_by:
        query = {"student_name": {"$regex": filter_by, "$options": "i"}}  # Case-insensitive search

    records = attendance_collection.find(query).sort("timestamp", -1)  # Sort by latest
    return list(records)  # Convert cursor to list
