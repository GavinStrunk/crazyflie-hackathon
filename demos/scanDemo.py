import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.mem import MemoryElement

uri = "radio://0/80/250k"

def connectcf(self):

	mem = cf.mem.get_mems(MemoryElement.TYPE_DRIVER_LED)
	print(mem[0].leds[0])
	if(len(mem) > 0):
		print("try to change led")
		mem[0].leds[1].set(0,255,0)
		mem[0].leds[2].set(0,0,255)
		mem[0].write_data(None)
	else:
		print("nothing found")

	cf.close_link()


cflib.crtp.init_drivers(enable_debug_driver=False)

print("Starting to scan for drones")
available = cflib.crtp.scan_interfaces()
print("Crazyflies found:")
for i in available:
	print(i[0])

print("Create crazyflie object")

cf = Crazyflie()

cf.connected.add_callback(connectcf)
print("open link")
cf.open_link(available[0][0])


