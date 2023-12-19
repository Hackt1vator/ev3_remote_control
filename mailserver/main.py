#!/usr/bin/env pybricks-micropython
import os
import threading
from sys import exit
from time import sleep
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.bluetooth import resolve
from messaging import BluetoothMailboxServer, TextMailbox, BluetoothMailboxClient

ev3 = EV3Brick()

def strcut(cut_from, str_to_cut):
    result = ""
    for i in cut_from:
        if not i in str_to_cut:
            result += i
    return result

def choose_opt(options: list):
    print(options); sleep(0.2)
    max_obj = 4; obj_list = options[:]; cogj = 0; from_obj = 0; marked_index = 0
    for i in obj_list: cogj += 1
    ev3.screen.clear()
    obj_list[marked_index] = "->" + obj_list[marked_index]
    if max_obj > cogj: max_obj = cogj
    for i in range(0, max_obj):
        ev3.screen.print(obj_list[i])

    option = ""
    while True:
        if Button.DOWN in ev3.buttons.pressed():
            sleep(0.4)
            obj_list[marked_index] = strcut(obj_list[marked_index], "->")
            if not marked_index >= (cogj -1):marked_index += 1
            print(str(marked_index) + " - " + str(cogj))
            obj_list[marked_index] = "->" + obj_list[marked_index]

            if marked_index >= max_obj and cogj > max_obj and not marked_index >= (cogj):
                from_obj += 1; 
                ev3.screen.clear()
                for i in range(from_obj, (from_obj + max_obj) ):
                    try: ev3.screen.print(obj_list[i])
                    except IndexError: pass
            else:
                ev3.screen.clear()
                for i in range(from_obj, (from_obj + max_obj) ):
                    try: ev3.screen.print(obj_list[i])
                    except IndexError: pass
            
        if Button.UP in ev3.buttons.pressed():
            sleep(0.4)
            obj_list[marked_index] = strcut(obj_list[marked_index], "->")
            if not marked_index <= 0: marked_index -= 1 
            print(str(marked_index) + " - " + str(cogj))
            obj_list[marked_index] = "->" + obj_list[marked_index]

            if marked_index < from_obj: # cogj > max_index, max_indey
                from_obj -= 1; 
                ev3.screen.clear()
                for i in range(from_obj, (from_obj + max_obj) ):
                    try: ev3.screen.print(obj_list[i])
                    except IndexError: pass
            else:
                ev3.screen.clear()
                for i in range(from_obj, (from_obj + max_obj) ):
                    try: ev3.screen.print(obj_list[i])
                    except IndexError: pass
        
        if Button.CENTER in ev3.buttons.pressed():
            option = obj_list[marked_index]; break
    ev3.screen.clear(); print(option)
    return strcut(option, "->")

def get_motor(motor):
    if motor == "A": return Motor(Port.A)
    elif motor == "B": return Motor(Port.B)
    elif motor == "C": return Motor(Port.C)
    elif motor == "D": return Motor(Port.D)
    elif motor == "S1": return Motor(Port.S1)
    elif motor == "S2": return Motor(Port.S2)
    elif motor == "S3": return Motor(Port.S3)
    elif motor == "S4": return Motor(Port.S4)

def change_ports(ports):
    print(ports)
    ports = ports.split("-")
    opt = choose_opt(ports)
    print(ports)
    if opt == "tm" or opt == "sm":
        opt = choose_opt(["tm", "sm"])
        if opt == "sm":
            ports = "sm-" + ports[1]
        elif opt == "tm":
            ports = "tm-A-B"
    elif opt == ports[1]:
            opt = choose_opt(["A", "B", "C", "D", "S1", "S2", "S3", "S4"])
            if ports[0] == "sm":
                ports = ports[0] +"-"+ opt
            else: ports = ports[0] +"-"+ opt +"-"+ ports[2]
    else: print(opt + ports[1])   
    if ports[0] != "sm":
        if opt == ports[2]:
            opt = choose_opt(["A", "B", "C", "D", "S1", "S2", "S3", "S4"])
            ports = ports[0] +"-"+ ports[1] +"-"+ opt
    return ports

def change_speed(speed):
    ev3.screen.clear()
    while True:
        sleep(0.2)
        if Button.UP in ev3.buttons.pressed():
            sleep(0.2)
            speed += 1
            ev3.screen.clear()
            ev3.screen.print("speed: " + str(speed))
        if Button.DOWN in ev3.buttons.pressed():
            sleep(0.2)
            speed -= 1
            if speed <= 0: speed = 1
            ev3.screen.clear()
            ev3.screen.print("speed: " + str(speed))
        if Button.CENTER in ev3.buttons.pressed():
            break
    return speed

def change_dir(direction):
    ev3.screen.clear(); sleep(0.4)
    while True:
        sleep(0.1)
        if Button.UP in ev3.buttons.pressed():
            sleep(0.2)
            direction += 1
            ev3.screen.clear()
            ev3.screen.print("direction: " + str(direction))

        if Button.DOWN in ev3.buttons.pressed():
            sleep(0.2)
            direction -= 1
            if direction <= 0: direction = 1
            ev3.screen.clear()
            ev3.screen.print("direction: " + str(direction))
        if Button.CENTER in ev3.buttons.pressed():
            break
    return direction

def rc_server():
    server = BluetoothMailboxServer()
    mbox = TextMailbox('rcontrol', server)

    ev3.screen.print('waiting...')
    server.wait_for_connection()
    ev3.screen.print('connected!')

    mbox.wait()
    if mbox.read() != "req": exit(2)
    mbox.send('ack')

    return [mbox, server]

def rc_client(addr):
    client_box = BluetoothMailboxClient()
    mbox = TextMailbox('rcontrol', client_box)

    print('establishing connection...')
    client_box.connect(addr)
    print('connected! to ' + addr)
    ev3.screen.print("connected!")
    mbox.send('req')
    mbox.wait()
    if mbox.read() != "ack": exit(2)

    return [mbox, client_box]

def clmotor_control(mbox, direction, speed, ports): #maybe port l/r for driving
    ev3.screen.print("motor control\n[press center\nto continue]")
    while True:
        sleep(0.3)
        if Button.UP in ev3.buttons.pressed():
            mbox.send("rcon-up-" + str(speed) +"-"+ str(ports))
        if Button.LEFT in ev3.buttons.pressed():
            mbox.send("rcon-left-" + str(speed) +"-"+ str(direction) +"-"+ str(ports))
        if Button.RIGHT in ev3.buttons.pressed():
            mbox.send("rcon-right-" + str(speed) +"-"+ str(direction) +"-"+ str(ports))
        if Button.DOWN in ev3.buttons.pressed():
            mbox.send("rcon-down-" + str(speed) +"-"+ str(ports))
        if Button.CENTER in ev3.buttons.pressed():
            break
    ev3.screen.clear()

def svcontrol(mbox):
    old_ports = ""; db = 0; direct = 0
    while True:
        mbox.wait() #wait_new()
        cmd = mbox.read(); print(cmd)
        if "rcon" in cmd:
            print("done 1")
            cmd = cmd.split("-")
            print(cmd)
            if cmd[1] == "up":
                if cmd[3] == "tm": #5,6
                    if old_ports != cmd[3] +"-"+ cmd[4] +"-"+ cmd[5]:
                        left_motor = get_motor(cmd[4]); left_motor.reset_angle(0)
                        right_motor = get_motor(cmd[5]); right_motor.reset_angle(0)
                        db = DriveBase(left_motor, right_motor, 20, 40)
                    db.drive(int(cmd[2]), 0); sleep(1); db.stop()
                    old_ports = cmd[3] +"-"+ cmd[4] +"-"+ cmd[5]
                    #left_motor.run_target(int(cmd[2]), 0, then=Stop.HOLD, wait=False) # wait-> thread/after
                    #right_motor.run_target(int(cmd[2]), 0, then=Stop.HOLD, wait=False) #maybe True
                    #left_motor.run_time(int(cmd[2]), 1000, then=Stop.HOLD, wait=False) # wait-> thread/after
                    #right_motor.run_time(int(cmd[2]), 1000, then=Stop.HOLD, wait=False) #maybe True
                elif cmd[3] == "sm": #5,6
                    left_motor = get_motor(cmd[4]); left_motor.reset_angle(0)
                    
                    left_motor.run_time(int(cmd[2]), 1000, then=Stop.HOLD, wait=False) # wait-> thread/after
                    old_ports = cmd[3] +"-"+ cmd[4]
            elif cmd[1] == "left":
                if cmd[4] == "tm": #5,6
                    if old_ports != cmd[4] +"-"+ cmd[5] +"-"+ cmd[6]:
                        left_motor = get_motor(cmd[5]); left_motor.reset_angle(0)
                        right_motor = get_motor(cmd[6]); right_motor.reset_angle(0)
                        db = DriveBase(left_motor, right_motor, 20, 40)
                    db.turn(int(cmd[3]))
                    
                    #left_motor.run_angle(int(cmd[2]), int(cmd[3]), then=Stop.HOLD, wait=False) # wait-> thread/after
                    #right_motor.run_angle(int(cmd[2]), int(cmd[3]), then=Stop.HOLD, wait=False) #maybe True
                    old_ports = cmd[4] +"-"+ cmd[5] +"-"+ cmd[6]
                elif cmd[4] == "sm": #5,6
                    left_motor = get_motor(cmd[5]); left_motor.reset_angle(0)
                    
                    left_motor.run_time(int(cmd[2]), int(cmd[3]), then=Stop.HOLD, wait=False) # wait-> thread/after
                    old_ports = cmd[4] +"-"+ cmd[5]
            elif cmd[1] == "right":
                if cmd[4] == "tm":
                    print(old_ports); print(cmd[4] +"-"+ cmd[5] +"-"+ cmd[6])
                    if old_ports != cmd[4] +"-"+ cmd[5] +"-"+ cmd[6]:
                        left_motor = get_motor(cmd[5]); left_motor.reset_angle(0)
                        right_motor = get_motor(cmd[6]); right_motor.reset_angle(0)
                    
                        db = DriveBase(left_motor, right_motor, 20, 40)
                    db.turn(-1*int(cmd[3]))
                    #left_motor.run_angle(int(cmd[2]), (-1*int(cmd[3])), then=Stop.HOLD, wait=False) # wait-> thread/after
                    #right_motor.run_angle(int(cmd[2]), (-1*int(cmd[3])), then=Stop.HOLD, wait=False) #maybe True
                    old_ports = cmd[4] +"-"+ cmd[5] +"-"+ cmd[6]
                elif cmd[4] == "sm": #5,6
                    left_motor = get_motor(cmd[5]); left_motor.reset_angle(0)
                    
                    left_motor.run_angle(int(cmd[2]), (-1*int(cmd[3])), then=Stop.HOLD, wait=False) # wait-> thread/after
                    old_ports = cmd[4] +"-"+ cmd[5]
            elif cmd[1] == "down":
                if cmd[3] == "tm": #5,6
                    if old_ports != cmd[3] +"-"+ cmd[4] +"-"+ cmd[5]:
                        left_motor = get_motor(cmd[4]); left_motor.reset_angle(0)
                        right_motor = get_motor(cmd[5]); right_motor.reset_angle(0)
                        db = DriveBase(left_motor, right_motor, 20, 40)
                    db.drive((-1*int(cmd[2])), 0); sleep(1); db.stop()
                    #left_motor = get_motor(cmd[4]); left_motor.reset_angle(0)
                    #right_motor = get_motor(cmd[5]); right_motor.reset_angle(0)
                    #left_motor.run_time((-1*int(cmd[2])), 1000, then=Stop.HOLD, wait=False) # wait-> thread/after
                    #right_motor.run_time((-1*int(cmd[2])), 1000, then=Stop.HOLD, wait=False) #maybe True
                    #left_motor.run_target((-1*int(cmd[2])), 0, then=Stop.HOLD, wait=False) # wait-> thread/after
                    #right_motor.run_target((-1*int(cmd[2])), 0, then=Stop.HOLD, wait=False) #maybe True
                    old_ports = cmd[3] +"-"+ cmd[4] +"-"+ cmd[5]
                elif cmd[3] == "sm": #5,6
                    left_motor = get_motor(cmd[4]); left_motor.reset_angle(0)
                    
                    left_motor.run_target((-1*int(cmd[2])), 1000, then=Stop.HOLD, wait=False) # wait-> thread/after
                    old_ports = cmd[3] +"-"+ cmd[4]

def get_addrs(filename):
    default_names = ["ev3dev", "rcserver", "server"]; new_names = []; result = []
    try:
        print("done")
        with open(filename, "r") as thefile:
            cont = thefile.read(); print("done")
        for name in default_names:
            print("done " + name)
            if resolve(name) in cont or resolve(name) == None: continue
            new_names.append(name)
        with open(filename, "a") as thefile:
            for i in new_names: thefile.write(resolve(i))
    except: 
        print("done, error")
        with open(filename, "a") as thefile:
            thefile.write("")

    with open(filename, "r") as thefile:
        cont = thefile.readlines()

    for i in cont:
        i = i[0:17]; result.append(i)
    print(result)
    return result

def rc_server_handler():
    rc_connections = rc_server()
    svcontrol(rc_connections[0])

def rc_client_handler():
    direction = 10; speed = 50; ports = "tm-A-B"
    saved_addrs = get_addrs("mac_addrs.txt")
    if not saved_addrs: ev3.screen.clear(); ev3.screen.print("no addrs found"); sleep(5); exit(1)
    addr = choose_opt(saved_addrs)
    try: cl_connections = rc_client(addr=addr)
    except: ev3.screen.clear(); ev3.screen.print("error \nwhile connecting"); sleep(5); rc_client_handler()
    #menu for options
    while True:
        sleep(0.4)
        option = choose_opt(["clmotor_control", "change_ports", "change_speed", "change_dir"])
        if option == "clmotor_control":
            ev3.screen.clear(); sleep(0.2)
            clmotor_control(cl_connections[0], direction=direction, speed=speed, ports=ports)
        elif option == "change_ports":
            ports = change_ports(ports=ports)
            ev3.screen.clear()
        elif option == "change_speed":
            ev3.screen.clear()
            speed = change_speed(speed=speed)
        elif option == "change_dir":
            ev3.screen.clear()
            direction = change_dir(direction=direction)
        

if __name__ == "__main__":
    opt = choose_opt(["rcserver", "rcclient"])
    if opt == "rcserver": 
        print("done")
        rc_server_handler()
    elif opt == "rcclient": 
        rc_client_handler()