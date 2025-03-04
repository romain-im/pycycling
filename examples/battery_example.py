import asyncio
from bleak import BleakClient

from pycycling.battery_service import BatteryService

from configuration import Configuration

async def run(address):
    async with BleakClient(address) as client:
        battery_service = BatteryService(client)
        battery_level = await battery_service.get_battery_level()
        print(f"Battery is at {battery_level}%")


if __name__ == "__main__":
    import os
    conf = Configuration()
    os.environ["PYTHONASYNCIODEBUG"] = str(1)

    device_address = conf.hr_address
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(device_address))
