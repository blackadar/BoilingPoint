"""
Handles Sensor I/O
"""
import Adafruit_DHT
from source import logger

log = logger.tee
sensor = Adafruit_DHT.DHT11
pin = 14


def read():
    """
    Reads sensor data and returns.
    Will return None if there is a sensor error.
    :return: float, float tuple (temp, humidity) as percentage
    """
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin, retries=5, delay_seconds=1)
    try:
        assert temperature is not None
        assert humidity is not None
    except AssertionError:
        log('[!] Sensor read error.')

    return temperature, humidity
