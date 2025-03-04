import asyncio
from bleak import BleakClient
from pycycling.fitness_machine_service import FitnessMachineService

from configuration import Configuration

async def run(address):
    async with BleakClient(address, timeout=10) as client:
        ftms = FitnessMachineService(client)

        supported_power_range = await ftms.get_supported_power_range()
        print("Supported power range:")
        print(supported_power_range)
        print()
        max_power = supported_power_range.maximum_power

        # Start receiving and printing 'notify' characteristics
        def print_indoor_bike_data(data):
            print("Received indoor bike data:")
            print(data)
            print()

        ftms.set_indoor_bike_data_handler(print_indoor_bike_data)
        await ftms.enable_indoor_bike_data_notify()

        def print_control_point_response(message):
            print("Received control point response:")
            print(message)
            print()

        ftms.set_control_point_response_handler(print_control_point_response)
        await ftms.enable_control_point_indicate()
        # 2. 'write' a request to control the fitness machine
        await ftms.request_control()
        # 3. (recommended) 'write' a reset command
        await ftms.reset()

        # Set target power
        power_level = 100 #4 / 100 * max_power
        print(f"Increasing target power to 4 percent of maximum power ({power_level}W).")
        print("The trainer will automatically adjust resistance based on your leg speed.")
        print(f"Try pedaling above {power_level}W to feel decreasing resistance, and vice versa.")
        await ftms.set_target_power(power_level)

        await asyncio.sleep(300)

        # Reset
        print("Resetting target power...")
        await ftms.reset()

if __name__ == "__main__":
    import os
    conf = Configuration()
    os.environ["PYTHONASYNCIODEBUG"] = str(1)

    device_address = conf.ht_address
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(device_address))