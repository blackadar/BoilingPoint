"""
Alerts the User when the water is ready
"""
from phue import Bridge
import time
import os
from source import logger

log = logger.tee
bridge_ip = '192.168.1.13'
room = 'Bedroom'
done_file = 'bp_stop'

group: int = None
bridge: Bridge = None


def setup():
    """
    Connect and setup
    :return: None
    """
    log("[ ] Setting up Hue bridge at " + str(bridge_ip))
    global bridge, group
    bridge = Bridge(bridge_ip)
    # bridge.connect()
    group = bridge.get_group_id_by_name(room)


def blink():
    """
    Blinks a Hue light
    :return:
    """
    log("[ ] Pushing alert perpetually.")
    global bridge, group
    original_color = bridge.get_group(group)['action']['xy']
    bridge.set_group(group, 'xy', [0.675, 0.322])  # Red
    done = False
    count = 0
    while not done:
        if count % 10 == 0:
            bridge.set_group(group, 'alert', 'lselect')
        time.sleep(1)
        count += 1
        done = check_done()
    log("[ ] Restoring original color.")
    bridge.set_group(group, 'alert', 'none')
    bridge.set_group(group, 'xy', original_color)


def check_done():
    """
    Check if the 'done' file was created by Siri/Script
    :return: bool was set
    """
    if os.path.exists(done_file):
        os.remove(done_file)
        return True
    else:
        return False
