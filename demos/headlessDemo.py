
import sys
import time

import cfclient.utils
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.mem import MemoryElement
from cflib.crazyflie.commander import Commander

headless = None

class HeadlessClient():

    def __init__(self):

        cflib.crtp.init_drivers()

        self._cf = Crazyflie(ro_cache=None,
                             rw_cache=cfclient.config_path + "/cache")


        #self._cf.commander.set_client_xmode(xmode=False)

    def connect_crazyflie(self, link_uri):

        self._cf.connection_failed.add_callback(self._connection_failed)
        self._cf.connected.add_callback(self._connected)
        #self._cf.param.add_update_callback(
        #    group="imu_sensors", name="HMC5883L", cb=(
        #        lambda name, found: self._jr.set_alt_hold_available(
        #            eval(found))))
        #self._jr.assisted_control_updated.add_callback(
        #    lambda enabled: self._cf.param.set_value("flightmode.althold",
        #                                             enabled))

        self._cf.open_link(link_uri)
        self._cf.commander.set_client_xmode(True)

        #self._jr.input_updated.add_callback(self._cf.commander.send_setpoint)

    def disconnect_crazyflie(self, link_uri):
    	self._cf.close_link()

    def list_crazyflies(self):
    	cflib.crtp.init_drivers()
    	available = cflib.crtp.scan_interfaces()
    	for i in available:
    		print(i[0])

    def setup_led(self):

    	self._mem = self._cf.mem.get_mems(MemoryElement.TYPE_DRIVER_LED)
    	if len(self._mem) > 0:
    		print("Success obtaining led memory")
    	else:
    		print("Error obtaining led memory")

    	self._cf.param.set_value("ring.effect", str(13))
    	time.sleep(1)

    def update_led(self, lednum, r, g, b):
    	self._mem[0].leds[lednum].set(r,g,b)
    	self._mem[0].write_data(None)

    def _connected(self, link):
        """Callback for a successful Crazyflie connection."""
        print("Connected to {}".format(link))
        self.run_stuff()

    def _connection_failed(self, link, message):
        """Callback for a failed Crazyflie connection"""
        print("Connection failed on {}: {}".format(link, message))
        sys.exit(-1)

    def run_stuff(self):
    	global headless

    	print("Setup leds")
    	headless.setup_led()

    	print("Change led 0")
    	headless.update_led(0, 0, 255, 0)
    	

    	print("fly the drone")
    	#unlock thrust protection
    	self._cf.commander.send_setpoint(0,0,0,0)
    	for i in range(10):
    		self._cf.commander.send_setpoint(0,0,0, 30000)
    		time.sleep(0.1)
    	time.sleep(1)
    	self._cf.commander.send_setpoint(0,0,0,0)
    	time.sleep(0.5)
    	self._cf.commander.send_stop_setpoint()

    	print("disconnect")
    	headless.disconnect_crazyflie(link_uri="radio://0/80/250K")


def main():

	global headless

	headless = HeadlessClient()
	headless.list_crazyflies()

	headless.connect_crazyflie(link_uri="radio://0/80/250K")


if __name__ == "__main__":
    main()
