import _thread
from objects import *
import usocket
import machine
import time
import gc
import os

CONFIGURATION_SAVE_FILE = "configurations.save"
NETWORK_CONFIGURATION_SAVE_FILE = "netconfig.txt"
DATA_PORT = 8778


def create_socket():
    s = usocket.socket()
    s.bind(("0.0.0.0",DATA_PORT))
    s.listen(5)
    return s


# Load the last saved configuration if there is one. Otherwise load a red flashing one.
def get_last_configuration():
    try:
        with open(CONFIGURATION_SAVE_FILE, 'r') as file:
            str_loops = file.readlines()
        config = load_configuration(str_loops[-1])
    except (OSError, IndexError, ValueError):
        config = [Color(1023, 0, 0), Wait(0.2), Color(0, 0, 0), Wait(0.2), Color(1023, 0, 0), Wait(0.2),
                      Color(0, 0, 0), Wait(1.0)]
    return config


def main():
    s = create_socket()
    s.settimeout(2)
    start_loop = get_last_configuration()

    c = Configuration(start_loop, CONFIGURATION_SAVE_FILE)
    _thread.start_new_thread(c.play_forever, ())

    while True:
        try:
            client, addr = s.accept()
            message = client.recv(4096).decode()

            # Reboots the chip.
            if message == "restart":
                machine.reset()
                continue
            elif message == "status":
                if c.stopped:
                    client.send('0')
                else:
                    client.send('1')
                time.sleep(0.1)
                continue
            # Resets network settings and configurations.
            elif message == "reset":
                os.remove(NETWORK_CONFIGURATION_SAVE_FILE)
                os.remove(CONFIGURATION_SAVE_FILE)
                c.stop()
                machine.reset()
                continue
            elif message == "off":
                for i in range(10):
                    c.stop()
                    time.sleep(0.1)
                continue
            elif message.startswith('('):
                str_configuration = message
            else:
                continue
        except OSError:
            continue
        # Close the client if there is one.
        finally:
            try:
                client.close()
            except NameError:
                pass
        c.stop()
        gc.collect()
        # Keep the current loop if the new one is invalid.
        try:
            loop = load_configuration(str_configuration)
            c.loop = loop
            c.validity_check()
        except:
            c.loop = get_last_configuration()
        c.save()
        c.restart()


if __name__ == '__main__':
    main()
