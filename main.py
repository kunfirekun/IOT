#GROUP 5 PROJECT TO AUTONMATE A FAN
#____________________________________
#+++++++++++++++++++++++++++++++++++
#____________________________________


#v1. of this code need can currently SENSE the tempreture CHANGES from the DHT and turn on and off based on whether the value exceeds the threshhold tempature value. 

#challenges noted, the time.sleep(2) function, which pings after every two seconds pauses the entire program after the two seconds elapses, meaning it turns off the fan completely losing its core function to be automated and it does not have a communication layer 

import machine
import dht
import time

# 1. Setup pins
sensor = dht.DHT22(machine.Pin(15))
fan = machine.Pin(2, machine.Pin.OUT)

# Threshold temperature to turn the fan on
TEMP_THRESHOLD = 30.0

print("Group 5 Automated Fan System Starting...")

while True:
    try:
        # 2. Measure temperature
        time.sleep(2) # DHT22 needs a small delay between readings
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()

        print(f"Temp: {temp}°C | Humidity: {hum}%")

        # 3. Logic to control the fan
        if temp > TEMP_THRESHOLD:
            fan.value(1) # Turn Fan ON
            print("Status: FAN ON (Jua imewaka buana!)")
        else:
            fan.value(0) # Turn Fan OFF
            print("Status: FAN OFF")

    except OSError as e:
        print("Failed to read sensor.")