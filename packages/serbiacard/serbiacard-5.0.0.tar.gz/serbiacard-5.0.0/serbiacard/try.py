import ctypes
import os

# Get current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the DLL
dll_path = os.path.join(script_dir, "eVehicleRegistrationAPI.dll")

# Ensure the path is correct
print(f"Loading DLL from: {dll_path}")

# Load the DLL

my_dll = ctypes.WinDLL(dll_path)


print(my_dll.sdStartup())
