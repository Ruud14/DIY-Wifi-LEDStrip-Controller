import time
import sys
import machine

RED_CONTROL_PIN = 21
GREEN_CONTROL_PIN = 19
BLUE_CONTROL_PIN = 18


def error(arg):
    raise Exception(arg)


# Converts a (saved or received) configuration from a string to the loop argument of the Configuration class.
def load_configuration(str_conf):
    str_loop = str_conf.split(";")
    loop = []
    for x in str_loop:
        if x.startswith("("):
            loop.append(Color(*[int(y)-1 if int(y)==1024 else int(y) for y in x.replace(")","").replace("(","").split(",")]))
        else:
            class_name, duration = x.split("(")
            duration = float(duration.replace(")",""))
            loop.append(getattr(sys.modules[__name__], class_name)(duration))
    return loop


class Color:
    def __init__(self, R, G, B):
        self.validity_check(R, G, B)
        self.set(R, G, B)

    # Sets the current color of the strip.
    def set(self, R, G, B):
        self.R = int(round(R))
        self.G = int(round(G))
        self.B = int(round(B))
        led_strip.set_color(self)

    # Returns the color as r,g,b values.
    def get(self):
        return self.R, self.G, self.B

    # Checks if the R,G,B values are valid.
    def validity_check(self, R, G, B):
        if not R >= 0 or not R <= 1023 or not G >= 0 or not G <= 1023 or not B >= 0 or not B <= 1023:
            error("The value of R, G and B have to be between 0 and 1023: {},{},{}".format(R, G, B))

    def __str__(self):
        return str((self.R, self.G, self.B))


# ---- Transition parent class ---- #
class Transition:
    def __init__(self, duration):
        self.duration = duration
        self.current_color = Color(0, 0, 0)

    # Returns the current color.
    def get(self):
        return self.current_color

    def __str__(self):
        return str(self.__class__.__name__)+"({})".format(self.duration)


# ---- All transitions ----
# Waits for a specific amount of seconds before changing to the next color.
class Wait(Transition):
    def run(self, current_color, next_color):
        self.current_color = current_color
        time.sleep(self.duration)
        self.current_color.set(*next_color.get())


# Slowly fades from one color to another during a specific amount of seconds.
class Fade(Transition):
    def run(self, current_color, next_color):
        self.current_color = current_color
        differences = [0, 0, 0]
        for i in range(3):
            differences[i] = next_color.get()[i] - self.current_color.get()[i]
        iterations = int(self.duration*1000)
        part = 1/iterations
        start = self.current_color.get()

        for i in range(iterations):
            self.current_color.set(start[0] + part * differences[0] * (i+1), start[1] + part * differences[1] * (i+1), start[2] + part * differences[2] * (i+1))
            time.sleep(0.001)
        self.current_color.set(*next_color.get())


# Class representation of the LED strip.
class LedStrip:
    def __init__(self, r_pin, g_pin, b_pin):
        self.red = machine.PWM(machine.Pin(r_pin), freq=5000)
        self.green = machine.PWM(machine.Pin(g_pin), freq=5000)
        self.blue = machine.PWM(machine.Pin(b_pin), freq=5000)

    # Sets the color of the strip.
    def set_color(self, color):
        r,g,b = color.get()
        self.red.duty(r)
        self.green.duty(g)
        self.blue.duty(b)


# Class representation of the configuration running on the strip.
class Configuration:
    def __init__(self, loop, save_file):
        self.save_file = save_file
        self.loop = loop
        self.validity_check()
        self.save()
        self.current_color = Color(*loop[0].get())
        self.stopped = False

    # Goes through self.loop to play the configuration
    def play(self):
        for i, it in enumerate(self.loop):
            if isinstance(it, Transition):
                if self.stopped:
                    break
                try:
                    if i == len(self.loop)-1:
                        it.run(self.current_color, self.loop[0])
                    else:
                        it.run(self.current_color, self.loop[i+1])
                except IndexError:
                    break

    # Keeps running self.play to play the configuration forever
    def play_forever(self):
        while True:
            if not self.stopped:
                self.play()

    # stops running the configuration and turns off the strip.
    def stop(self):
        self.stopped = True
        self.current_color = Color(0, 0, 0)

    # Continues running the configuration.
    def restart(self):
        self.stopped = False

    # Saves the current configuration to storage so it can be run on the next startup.
    def save(self):
        string = ";".join([str(x) for x in self.loop]) + "\n"
        print(string)

        try:
            with open(self.save_file, 'r+') as file:
                last = file.readlines()[-1]
                # only save if the last save isn't the same as this one.
                if not last == string:
                    file.write(string)
            with open(self.save_file, 'r') as file:
                data = file.readlines()
            # save only 5 configurations.
            if len(data) > 5:
                with open(self.save_file, 'w') as file:
                    for line in data[1:]:
                        file.write(line)
        except (OSError, IndexError):
            with open(self.save_file, 'w') as file:
                file.write(string)

    # Checks if the configuration is valid.
    def validity_check(self):
        if not isinstance(self.loop[0], Color):
            error("First element of loop has to be a color.")
        if not isinstance(self.loop[-1], Transition):
            error("Last element of loop has to be a transition. "
                  "This transition is necessary to go back to the first color.")

        prev = 't'
        for it in self.loop:
            if isinstance(it, Color):
                if not prev == 't':
                    error("A color can't be followed up by another color.")
                prev = 'c'
            elif isinstance(it, Transition):
                if not prev == 'c':
                    error("A Transition can't be followed up by another transition.")
                prev = 't'
            else:
                error("{} isn't a color or a transition.".format(str(it)))


# Global LED strip, which can be accessed by every class.
led_strip = LedStrip(RED_CONTROL_PIN, GREEN_CONTROL_PIN, BLUE_CONTROL_PIN)