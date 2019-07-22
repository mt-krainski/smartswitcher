
import machine
import time
import socket

def run(delay, loop_limit=100, host='192.168.4.2', port=54322):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.setblocking(False)
    previous_zero_crossing = 0
    zc = machine.Pin(5, machine.Pin.IN)
    pin = machine.Pin(16, machine.Pin.OUT)
    loops = 0
    try:
        while loops<loop_limit:
            zero_crossing = zc.value()
            if previous_zero_crossing==1 and zero_crossing==0:
                time.sleep_us(delay)
                pin.off()
                loops += 1
            if previous_zero_crossing==0 and zero_crossing==1:
                pin.on()
                try:
                    data = s.recv(100)
                    delay = int(data)
                except OSError:
                    pass
            previous_zero_crossing = zero_crossing
    except Exception as e:
        print(e)
    finally:
        pin.on()


for i in range(3):
     for j in range(5500, 6600, 15):
         run(j, 3)
     for j in range(6600, 5500, -15):
         run(j,3)
