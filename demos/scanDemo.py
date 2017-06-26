import cflib.crtp

cflib.crtp.init_drivers(enable_debug_driver=False)

print("Starting to scan for drones")
available = cflib.crtp.scan_interfaces()
print("Crazyflies found:")
for i in available:
	print(i[0])