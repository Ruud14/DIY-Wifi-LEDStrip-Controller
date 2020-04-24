# DIY Wi-Fi LEDStrip Controller

Project status: Work in progress.

DIY Wi-Fi LED strip controller based on the ESP32 chip and MicroPython. Contains step-by-step build guide with links to parts. The controller can be controlled via raw sockets or with an android app.

### Parts
- 1x NodeMCU ESP32 : [eBay LINK 1pc](https://www.ebay.com/itm/Espressif-ESP32-WLAN-Dev-Kit-Board-Development-Bluetooth-Wifi-v1-WROOM32-NodeMCU/253059783728?hash=item3aeb89dc30:g:5-8AAOSwAThb3MaZ)
- 3x 1KOhm resistor: [eBay LINK 100pc](https://www.ebay.com/itm/100-pcs-1-4W-0-25W-1-Metal-Film-Resistor-1K-ohm-1Kohm/282033455842?_trksid=p2485497.m4902.l9144)
- 1x 12v Female DC Power Socket: [EBAY LINK 10pc](https://www.ebay.com/itm/10Pcs-5-5-x-2-1mm-12-V-DC-Power-Supply-Jack-Socket-Female-Panel-Mount-Connector/143449192665?_trksid=p2485497.m4902.l9144)
- 1x Female strip connector: [EBAY LINK 5pc](https://www.ebay.com/itm/10Pcs-5-5-x-2-1mm-12-V-DC-Power-Supply-Jack-Socket-Female-Panel-Mount-Connector/143449192665?_trksid=p2485497.m4902.l9144)- 1x RGB LED strip: [eBay LINK 1pc](https://www.ebay.com/itm/184203854470?ViewItem=&item=184203854470)
- 3x Tip31c transistor: [eBay LINK 10pc](https://www.ebay.com/itm/10-x-TIP31C-TIP31-NPN-Transistor-3A-100V-TO-220-FSC/270984720497?hash=item3f17f2b071:g:8hUAAOxyepRRrfsF)
- 1x 12v Power Supply Adapter (2A for a 5M long strip): [eBay LINK 1pc](https://www.ebay.com/itm/AC-TO-DC-5V-12V-24V-1A-2A-3A-5A-10A-0-5A-Power-Supply-Adapter-LED-Strip-Light/254344416209?_trksid=p2485497.m4902.l9144)
- 1x 12v to 5v Converter: [eBay LINK 1pc](https://www.ebay.com/itm/DC-DC-12V-to-5V-6V-9V-2-3A-15W-Converter-Step-Down-2A-3A-15W-Power-Supply-Module/401327863545?_trksid=p2485497.m4902.l9144)
- 1x PCB. Upload the attached Gerber files to jlcpcb.com. (Minimum amount is 5pc)
- 8x M2.5-3.5 bolts&nuts. 20-30 mm long [eBay LINK](https://www.ebay.com/itm/M2-M2-5-M3-304-Stainless-Steel-Allen-Hex-Socket-Countersunk-Head-Screws-Bolts/282935136527?hash=item41e03f910f:m:mKxIf5Qmt5Zi86DIH4-mAoQ)
- 2x Simple 5 cm long wire

### Tools
- Soldering iron
- small pliers (or tiny hands)
- 3d printer (optional, you can make everything except for the case.)
- Windows or Linux PC.

# Makers guide
First order all the necessary parts and make sure you have all the required tools.
While waiting for the parts to arrive you can already install a version of [python](https://www.python.org/) on your PC.
Make sure you install version 3.7 or higher.
After installing python you can connect your esp32 board to your PC using a micro USB cable,
install [esptool](https://pypi.org/project/esptool/) and flash your esp32 with the MicroPython firmware. You can find a great guide for all this
over [here](https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html). **Make sure to hold the "Boot" button on the board while writing and erasing flash or it won't work.**

The last thing we should do before we start soldering is put
the [attached scripts](https://github.com/Ruud14/DIY-Wifi-LEDStrip-Controller/tree/master/to_ESP32) on the board.
You can do this with a tool called [ampy](https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy) .
Simply install ampy by running 'pip3 install adafruit-ampy' in your terminal. After that you can put all the scripts on your board by running:
'ampy --port YOUR_PORT put boot.py',
'ampy --port YOUR_PORT put main.py',
'ampy --port YOUR_PORT put objects.py',

After this you can disconnect your esp32 from your PC and start soldering.
I tried to mark everything on the PCB as good as possible, but you can look at the [pictures](https://github.com/Ruud14/DIY-Wifi-LEDStrip-Controller/tree/master/pictures) if it isn't clear enough.
**One thing you really need to look out for is that the wires of the female strip connector aren't in the correct order.
You need to put the red wire in the hole that says 'R', the green one in the hole that says 'G' and the blue one in the hole that says 'B'.**
**Another thing to note is that the shortest end of the female dc power socket should be connected to the positive end of the board**

*This part is for the ones that are printing the case.
You can download the [attached .stl files](https://github.com/Ruud14/DIY-Wifi-LEDStrip-Controller/tree/master/3d%20models)
convert them to g-code and print them. Make sure you enable support material for the bottom part.*

After everything is done you should check that no soldered connections are touching each other and connect your soldered PCB to power.
Just to check you can scan for nearby Wi-Fi networks on your phone and you should see a network called "LedStrip Setup" if everything is alright.
Now your very own controller is done and you can install the app to control the strip [here](https://github.com/Ruud14/Wifi-LEDStrip-Controller-App).
You can also control the strip by sending raw socket commands in the following format:

(1024,0,0);Fade(0.2);(0,0,0);Wait(0.2)

The string should always start with a RGB color '(r,g,b)'
where the values of r, g and b must be between 0 and 1024.
After a color comes a transition. The two options are 'Fade(x)' and 'Wait(x)' .
A color can only be followed up by a transition and a transition can only be followed up by a color.
Colors and transitions must be separated by a ';'. The string must always end with a transition.

![fully_assembled](https://github.com/Ruud14/DIY-Wifi-LEDStrip-Controller/blob/master/pictures/fully_assembled.jpg)
![inside_case](https://github.com/Ruud14/DIY-Wifi-LEDStrip-Controller/blob/master/pictures/inside_case.jpg)
![soldered_pcb1](https://github.com/Ruud14/DIY-Wifi-LEDStrip-Controller/blob/master/pictures/soldered_pcb1.jpg)

### Additional info.
**What I learned:**
- Working access point networks.
- Working with the esp32 (Had used a esp8266 before).
- Designing a PCB.
