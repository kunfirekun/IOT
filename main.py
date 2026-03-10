import machine, dht, time, network
import BlynkLib

# --- BLYNK CONFIG ---
BLYNK_TEMPLATE_ID = "TMPL23lcFNtXy"
BLYNK_TEMPLATE_NAME = "GROUP 5 FAN AUTOMATION"
BLYNK_AUTH_TOKEN = "F1mCDwjrdT0cQeA3HEOc5rRH5gEf6h7F"

# --- HYSTERESIS & TIMERS ---
TEMP_ON = 30.0
TEMP_OFF = 28.0
last_update = 0
update_interval = 5000  # 5 seconds
fan_state = 0

# --- HARDWARE ---
sensor = dht.DHT22(machine.Pin(15))
fan = machine.Pin(2, machine.Pin.OUT)

# --- WIFI CONNECT ---
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("Wokwi-GUEST", "")

while not wlan.isconnected():
    time.sleep(0.5)
    print("Connecting Gropu 5 Fan to WiFi...")

print("WiFi Connected!")

# --- INITIALIZE BLYNK ---
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

while True:
    blynk.run() # Keeps the connection alive
    current_time = time.ticks_ms()

    # Non-blocking Sensor & Logic Task
    if time.ticks_diff(current_time, last_update) >= update_interval:
        try:
            sensor.measure()
            temp = sensor.temperature()
            
            # Hysteresis Logic
            if temp >= TEMP_ON:
                fan_state = 1
            elif temp <= TEMP_OFF:
                fan_state = 0
            
            fan.value(fan_state)

            # --- SEND TO BLYNK ---
            blynk.virtual_write(1, temp)      # Sending to V1
            blynk.virtual_write(2, fan_state) # Sending to V2
            
            print(f"Group 5 Fan Info -> Temp: {temp}C, Fan: {fan_state}")
            last_update = current_time
            
        except Exception as e:
            print("Blynk Error:", e)