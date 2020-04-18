import esp
esp.osdebug(None)
import network
import gc
import socket
import time

ap_if = network.WLAN(network.AP_IF)
sta_if = network.WLAN(network.STA_IF)
DATA_PORT = 7777
connection_timeout = 10


def save_network(ssid,password, hostname):
    with open("netconfig.txt", 'w') as f:
        f.write(",".join([ssid, password, hostname]))


def get_network():
    with open("netconfig.txt", 'r') as f:
        ssid, password, hostname = f.read().split(',')
        return ssid, password, hostname


def setup_network():
    gc.collect()
    if sta_if.isconnected():
        print("already connected")
        ap_if.active(False)
    else:
        sta_if.active(True)
        ap_if.active(True)
        sta_if.active(True)
        ap_if.config(essid="LedStrip Setup", password="Ruud14_LedStrip")
        s = socket.socket()
        s.bind(("0.0.0.0", DATA_PORT))
        s.listen(3)
        while True:
            client, addr = s.accept()
            print(addr, "connected")
            data = client.recv(1024).decode()
            ssid, password, hostname = data.split(",")
            if connect(ssid, password, hostname):
                client.close()
                s.close()
                ap_if.active(False)
                save_network(ssid, password, hostname)
                break
            else:
                client.close()


def connect(ssid, password, host):
    try:
        sta_if.config(dhcp_hostname=host)
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, password)
        total_time = 0
        while not sta_if.isconnected():
            if total_time > connection_timeout:
                print("Connecting to", ssid, "failed...")
                return False
            time.sleep(0.5)
            total_time+=0.5
        print('network config:', sta_if.ifconfig())
        return True
    except Exception as e:
        print(e)
        print("Connecting to", ssid, "failed...")
        return False


if __name__ == '__main__':
    try:
        ssid, password, hostname = get_network()
        if not connect(ssid, password, hostname):
            setup_network()
    except OSError:
        setup_network()
    gc.collect()