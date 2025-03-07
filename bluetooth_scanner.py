import asyncio
from bleak import BleakScanner

async def scan_devices():
    devices = await BleakScanner.discover()
    scanned_devices = [(device.name, device.address) for device in devices if device.name]
    return scanned_devices

def get_bluetooth_devices():
    return asyncio.run(scan_devices())
