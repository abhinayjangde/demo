import asyncio
from bleak import BleakScanner
import threading
from concurrent.futures import ThreadPoolExecutor

async def scan_devices():
    """Scan for Bluetooth devices asynchronously"""
    try:
        devices = await BleakScanner.discover(timeout=10.0)
        scanned_devices = [(device.name, device.address) for device in devices if device.name]
        return scanned_devices
    except Exception as e:
        print(f"Error scanning devices: {e}")
        return []

def get_bluetooth_devices():
    """Get Bluetooth devices using a separate thread to avoid event loop conflicts"""
    def run_in_thread():
        # Create a new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(scan_devices())
        finally:
            loop.close()
    
    # Run the async function in a separate thread
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(run_in_thread)
        try:
            return future.result(timeout=15)  # 15 second timeout
        except Exception as e:
            print(f"Bluetooth scan failed: {e}")
            return []