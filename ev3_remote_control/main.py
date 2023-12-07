#!/usr/bin/env pybricks-micropython
import socket
import threading
from sys import exit
from time import sleep
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()

def str_cut(cut_from:str, str_to_cut:str):
    result = ""
    for i in cut_from:
        if not i in str_to_cut:
            result += i
    return result


def main_menu():
    max_obj = 0; obj_list = []; cobj = 0; from_obj = 0; marked_index = 0
    for i in obj_list: cogj += 1

    obj_list[marked_index] = "->" + obj_list[marked_index]
    for i in range(0, max_obj):
        ev3.screen.print(obj_list[i])
    
    option = ""
    while True:
        if Button.DOWN in ev3.buttons.pressed():
            sleep(0.4)
            obj_list[marked_index] = str_cut(obj_list[marked_index], "->")
            marked_index += 1
            if marked_index < 0: marked_index = 0
            obj_list[marked_index] = "->" + obj_list[marked_index]

            if marked_index >= max_obj and cobj > max_obj and marked_index != cogj:
                from_obj += 1; 
                ev3.screen.clear()
                for i in range(from_obj, (from_obj + max_obj) ):
                    try: ev3.screen.print(obj_list[i])
                    except IndexError: pass
            else:
                for i in range(from_obj, (from_obj + max_obj) ):
                    try: ev3.screen.print(obj_list[i])
                    except IndexError: pass
            if marked_index == cogj:
                marked_index -= 1

        if Button.UP in ev3.buttons.pressed():
            sleep(0.4)
            obj_list[marked_index] = str_cut(obj_list[marked_index], "->")
            marked_index -= 1
            if marked_index < 0: marked_index = 0
            obj_list[marked_index] = "->" + obj_list[marked_index]

            if marked_index <= max_obj and cogj > max_obj:
                from_obj -= 1; 
                ev3.screen.clear()
                for i in range(from_obj, (from_obj + max_obj) ):
                    try: ev3.screen.print(obj_list[i])
                    except IndexError: pass
            else:
                for i in range(from_obj, (from_obj + max_obj) ):
                    try: ev3.screen.print(obj_list[i])
                    except IndexError: pass
        
        if Button.CENTER in ev3.buttons.pressed():
            option = str_cut(obj_list[marked_index], "->"); break

    if option == "":
    elif option == "":
    elif option == "":
    elif option == "":





def block_connect():
    device_list = ["12:HD:23:12:32...", "123.2345.123", "123434567654323456"]
    marked_index = 0; rdevice = ""

    ev3.screen.print("Hello World\nPress [enter]\nto continue")

    while True: 
        #device_list = bluethouth.scan()
        if Button.CENTER in ev3.buttons.pressed(): ev3.screen.clear(); sleep(2); break

    device_list[marked_index] = "-" + device_list[marked_index]
    for i in device_list:
        ev3.screen.print(i)

    while True:
        #add max and then max achieved marked = 0
        if Button.UP in ev3.buttons.pressed():
            sleep(0.5)
            device_list[marked_index] = str_cut(device_list[marked_index], "-")
            ev3.screen.clear()
            try: marked_index -= 1; device_list[marked_index] = "-" + device_list[marked_index]
            except IndexError: pass
            for i in device_list:
                ev3.screen.print(i)
        if Button.DOWN in ev3.buttons.pressed():
            sleep(0.5)
            print(device_list[marked_index]); print(device_list[0])
            device_list[marked_index] = str_cut(device_list[marked_index], "-")
            marked_index += 1; ev3.screen.clear()
            try:device_list[marked_index] = "-" + device_list[marked_index]
            except IndexError: pass
            for i in device_list:
                ev3.screen.print(i)
        if Button.CENTER in ev3.buttons.pressed():
            rdevive = str_cut(device_list[marked_index], "-")
            ev3.screen.clear(); break
    
    ev3.screen.print(str_cut(device_list[marked_index], "-"))
    sleep(3)
    exit(0)





    #ev3.speaker.say("hi")
menu()
sleep(5)

while True:
    if Button.UP in ev3.buttons.pressed():
        print("up pressed")
        ev3.speaker.beep()
    if Button.DOWN in ev3.buttons.pressed():
        print("down pressed")
        ev3.speaker.beep()
    if Button.RIGHT in ev3.buttons.pressed():
        print("right pressed")
        ev3.speaker.beep()
    if Button.LEFT in ev3.buttons.pressed():
        print("left pressed")
        ev3.speaker.beep()
    if Button.CENTER in ev3.buttons.pressed():
        print("center pressed")
        ev3.speaker.beep()

#print out to pc
#Program ended by stop button
