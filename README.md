# ev3 remote control

This Project uses micropython to control an ev3 brick using another ev3 brick


Liberys used in this project:

<strong><a href="https://pypi.org/project/python-ev3dev2/">ev3dev2</a></strong>

Donate to developer: <strong><a href="https://www.buymeacoffee.com/Hacktivator">buymeacoffee</a></strong>

# Requirements

- PC with macos or windows
- 2 ev3 bricks
- 2 micro sd cards
- adhesive tape
- VS-Code, the "LEGO® MINDSTORMS® EV3 MicroPython" and "ev3dev-browser" extensions or
          SSH over USB-Ethernet for uploading the program to the Ev3-Bricks
- Mini-USB-Cable

# How to run

    -Download the Micropython-Ev3 image from: https://assets.education.lego.com/v3/assets/blt293eea581807678a/blt9df409c9a182ab9c/5f88191a6ffd1b42dc42b8af/ev3micropythonv200sdcardimage.zip?locale=en-us
    
    -Flash the Micro-SD cards from the image-file (using for example https://etcher.balena.io/)
    
    -Plug the Mini-USB-Cable in and connect your computer with the Ev3-Brick (using for example VS-Code)

    -Download the remote control code and unzip it

    -Open the folder with the code in VS-Code and upload the code to the Ev3-Bricks

    -Leave the hostnames on default or set them to default by running setup_brick.SSH

    -Pair the two Ev3-Bricks using the "Wireless-Connections" and "Bluetooth" option then booting up the Ev3-Bricks

    -Select a server (controlled device) and a client (controlling device)

    -On the client-side, select the mac-address of the server or the only mac-address displayed (you can add mac-address by writing them into the "mac_addrs.txt" file)

    -The connection between the Ev3-Bricks has now been established!

# Common Issues

-using Motors connected to Sensor-Ports(1,2,3,4) may raise errors

-when using single_motor(sm), left and right will only let the ev3 drive forward and backwards
