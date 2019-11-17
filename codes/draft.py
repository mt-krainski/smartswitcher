import machine
import network
import time
import socket
import json

STA_IF = network.WLAN(network.STA_IF)


print("Opening config file...")
with open("config.json") as f:
    CONFIG = json.load(f)
print("Config file read.")
print(CONFIG)


def connect_to_wifi(ssid, password):
    if not STA_IF.isconnected():
        print("connecting to network...")
        STA_IF.active(True)
        STA_IF.connect(ssid, password)
        while not STA_IF.isconnected():
            pass
        print("Connected.")
        print("network config:", STA_IF.ifconfig())


def connect_to_server(host, port):
    print("Connecing to IoT server.")
    while True:
        try:
            print("Trying to connect to: ", host, port, ".")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.setblocking(False)
            print("Connected")
            break
        except Exception:
            print("Connection failed. Retrying.")
            time.sleep(5)
    return s


def run(s, zc_pin, out_pin):
    previous_zero_crossing = 0
    zc = machine.Pin(zc_pin, machine.Pin.IN)
    pin = machine.Pin(out_pin, machine.Pin.OUT)
    try:
        while True:
            zero_crossing = zc.value()
            if previous_zero_crossing == 1 and zero_crossing == 0:
                time.sleep_us(delay)
                pin.off()
            if previous_zero_crossing == 0 and zero_crossing == 1:
                pin.on()
                try:
                    data = s.recv(100)
                    # Signal that the connection has been closed.
                    if data == "":
                        return
                    delay = int(data)
                # Raised when there is no data in buffer.
                except OSError:
                    pass
            previous_zero_crossing = zero_crossing
    except Exception as e:
        print(e)
    finally:
        pin.on()

print("Starting loop...")
while True:
    print("Loop.")
    connect_to_wifi(CONFIG["wifi"]["ssid"], CONFIG["wifi"]["password"])
    server_connection = connect_to_server(
        CONFIG["server"]["host"], CONFIG["server"]["port"]
    )
    run(server_connection, CONFIG["device"]["zc_pin"], CONFIG["device"]["out_pin"])

print("Terminated.")
