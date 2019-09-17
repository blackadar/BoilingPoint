"""
Communications and high level shit
"""
from source import logger, alert, sensor

log = logger.tee


def main():
    # First, establish an average baseline.
    alert.setup()
    log("[ ] Establishing a baseline for 10 ticks...")
    baseline_temps = []
    baseline_humids = []
    for i in range(0, 10):
        b_t, b_h = sensor.read()
        if b_t is not None:
            baseline_temps.append(b_t)
        if b_h is not None:
            baseline_humids.append(b_h)
    baseline_temperature = sum(baseline_temps) / len(baseline_temps)
    baseline_humidity = sum(baseline_humids) / len(baseline_humids)
    log("[-] Baseline Temp: " + str(baseline_temperature))
    log("[-] Baseline Humidity: " + str(baseline_humidity))

    # Keep collecting until we get a true done.
    stop = False  # Loop condition
    water_debounce = False  # Last read was 'done'
    water_debounce_count = 0  # Number of ticks we've been 'done'
    water_debounce_threshold = 5  # Number of ticks to actually be 'done'

    while not stop:
        if alert.check_done():
            log("[ ] Exit file detected. Stopping...")
            stop = True
        else:
            try:
                temp, humidity = sensor.read()
                assert temp is not None
                assert humidity is not None
                delta_temp = abs(temp - baseline_temperature)
                delta_humidity = abs(humidity - baseline_humidity)
                log("[-] Temp: " + str(temp) + " (Δ " + str(delta_temp) + ")")
                log("[-] Humidity: " + str(humidity) + " (Δ " + str(delta_humidity) + ")")
                iter_done = check_water_done(delta_temp, delta_humidity)
                if iter_done:
                    log("[*] Done this iteration.")
                if water_debounce and iter_done:
                    # We've been in 'done' state before
                    water_debounce_count += 1
                    log("[-] Debounce: " + str(water_debounce_count) + " of " + str(water_debounce_threshold))
                    if water_debounce_count >= water_debounce_threshold:
                        alert.blink()
                        stop = True
                elif not water_debounce and iter_done:
                    # This is our first 'done'
                    water_debounce = True
                    water_debounce_count = 1
                else:
                    # We weren't done
                    water_debounce = False
                    water_debounce_count = 0

            except AssertionError:
                log('[!] Sensor read error.')
    log("[ ] Timer is done.")


def check_water_done(delta_temp: float, delta_humidity: float):
    """
    Returns bool water is done
    :param delta_temp: Change from Baseline temp
    :param delta_humidity: Change from Baseline humidity
    :return: True/False Water is Done
    """
    t_threshold = 10  # Increase 10C --> 50F
    h_threshold = 20  # Increase 20% Humidity
    return delta_temp > t_threshold and delta_humidity > h_threshold


if __name__ == '__main__':
    main()
