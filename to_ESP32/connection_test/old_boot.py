# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)
import network
import socket
import gc
import time

DATA_PORT = 7777

def main():
    ap_if = network.WLAN(network.AP_IF)


    while True:
        s = socket.socket()
        s.bind(("0.0.0.0", DATA_PORT))
        s.listen(5)
        ap_if.active(True)
        ap_if.config(essid='New LedStrip', authmode=network.AUTH_WPA_WPA2_PSK, password="Ruud14_LedStrip")
        client, addr = s.accept()
        print(str(addr), "Connected")
        msg = client.recv(1024).decode()
        host, pas = msg.split(",")
        s.close()
        del s
        ap_if.active(False)
        do_connect(host,pas)
        break
        # if do_connect(host,pas):
        #     print("success")
        #     break
        # else:
        #     print("failed")
        #     continue


def do_connect(hostname, password):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to', hostname, 'with password', password)
        sta_if.active(True)
        sta_if.connect('Brouwers','Bloempot83')
        while not sta_if.isconnected():
           pass
        print('Network config: ', sta_if.ifconfig())

main()
gc.collect()