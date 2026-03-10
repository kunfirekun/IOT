import machine
import dht
import time
import network
import BlynkLib

# --- 1. BLYNK CONFIGURATION ---
BLYNK_TEMPLATE_ID = "TMPL23lcFNtXy"
BLYNK_TEMPLATE_NAME = "GROUP 5 FAN AUTOMATION"
BLYNK_AUTH_TOKEN = "F1mCDwjrdT0cQeA3HEOc5rRH5gEf6h7F"

# --- 2.ESP32 AND DHT22 HARDWARE CONFIGURATION ---
sensor = dht.DHT22(machine.Pin(15))
fan = machine.Pin(2, machine.Pin.OUT) # Built-in LED acts as our Fan

# --- 3. GLOBAL VARIABLES ---
TEMP_ON = 30.0   # Upper Threshold
TEMP_OFF = 28.0  # Lower Threshold
last_update = 0
update_interval = 5000 # 5 seconds to prevent -104 errors
manual_fan = 0   # State of the Blynk Switch (V3)
auto_fan = 0     # State calculated by the sensor

# --- 4. WIFI CONNECTION ---
print("Connecting to Wokwi-GUEST...")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("Wokwi-GUEST", "")

while not wlan.isconnected():
    time.sleep(0.5)
    print(".", end="")

print("Group 5 Fan WiFi Connected!")

# --- 5. BLYNK HANDSHAKE CONFRIMATION & VALUE HANDLERS ---
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

@blynk.on("connected")
def blynk_connected():
    print('Successfully Connected to Blynk.')# Handshake to blynk to check if the systems are communicating
    blynk.sync_virtual(3) # Check with Blynk for the current switch state

@blynk.on("V3")
def v3_handler(value):
    global manual_fan
    manual_fan = int(value[0])
    print(f"Manual Overide Switch is: {'ON' if manual_fan else 'OFF'}")

# --- 6. MAIN LOOP ---
print("Group 5 Fan Starting...")

while True:
    try:
        blynk.run() # Maintains the cloud connection
        
        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, last_update) >= update_interval:
            # A.Sensor 
            sensor.measure()
            temp = sensor.temperature()
            
            # B.Hysteresis Logic (Automated Mode)
            if temp >= TEMP_ON:
                auto_fan = 1
            elif temp <= TEMP_OFF:
                auto_fan = 0
            # If the data from the sensor is between 28-30, auto_fan stays at its previous state not snap into an OFF state even at readings like 29.9 leaving the room hot. It cools the room a little more until it gets to 28 and below so that it comes at a halt state
            
            # C. Priority Logic (The "OR" Logic)
            # The fan is ON if either the Sensor says so OR the Manual Switch is ON
            fan_state = 1 if (auto_fan == 1 or manual_fan == 1) else 0
            
            # D.Apply to Hardware; being a
            fan.value(fan_state)
            
            # E. Update Blynk Dashboard
            blynk.virtual_write(1, temp)      # Temperature Gauge DAta
            blynk.virtual_write(2, fan_state) # Fan Status LED Data
            
            print(f"Temp: {temp}C | Manual: {manual_fan} | Fan: {fan_state}")
            last_update = current_time

    except OSError as e:
        if e.args[0] == -104:
            print("Connection Reset (-104). Re-attempting handshake...")
            time.sleep(2)
            # Re-initialize Blynk to recover from connectivity loss
            blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)
        else:
            print("Error encountered:", e)

