import machine
import dht
import time

# --- Setup ---
sensor = dht.DHT22(machine.Pin(15))
fan = machine.Pin(2, machine.Pin.OUT)


# Timers (in milliseconds)
last_sensor_read = 0
sensor_interval = 5000  # 5 seconds


print("Group 5 automated fan starting...")

while True:
    current_time = time.ticks_ms()

    # 1. Non-blocking code update
    # Check if 2000ms have passed since the last read
    if time.ticks_diff(current_time, last_sensor_read) >= sensor_interval:
        try:
            sensor.measure()
            temp = sensor.temperature()
            hum = sensor.humidity()
            # Fan logic
            fan.value(1 if temp > 30 else 0)
            
            print(f"Temp: {temp}°C | Humidity: {hum}% | Fan: {'ON' if temp > 30 else 'OFF'}")
            
            # Reset the timer
            last_sensor_read = current_time
            
        except OSError as e:
            print("Sensor error!")
